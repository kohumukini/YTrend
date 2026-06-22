import yfinance as yf
import pandas as pd
from sqlalchemy import func
from datetime import datetime, timezone
from ..database import SessionLocal, BronzeStock, Watchlist, PullLog
from .etl.extract import update_dataframe
from .logger import logger

def get_active_watchlist():
    with SessionLocal() as session:
        tickers = session.query(Watchlist).filter(Watchlist.status == 'active').all()
        return [t.ticker for t in tickers]

def save_raw_data(ticker, dataframe):
    if dataframe is None or dataframe.empty:
        logger.warning(f"[pull] No data for {ticker} — skipping")
        return

    with SessionLocal() as session:
        try:
            dataframe = dataframe.copy()
            # Drop the multi-level column index yFinance adds
            if isinstance(dataframe.columns, pd.MultiIndex):
                dataframe.columns = dataframe.columns.droplevel(1)

            exists = session.query(BronzeStock).filter_by(ticker=ticker).first()
            merged = update_dataframe(ticker, dataframe)

            json_str = merged.to_json()

            if exists:
                exists.raw_json = json_str
            else:
                new_entry = BronzeStock(
                    ticker=ticker,
                    raw_json=json_str,
                    ingested_at=func.now()
                )
                session.add(new_entry)

            session.commit()
            logger.info(f"[pull] Saved {ticker} data successfully")

        except Exception as e:
            logger.error(f"[pull] Failed to save {ticker}: {type(e).__name__}: {e}")
            session.rollback()
            raise

def pull_data():
    active_tickers = get_active_watchlist()
    today = datetime.now(tz=timezone.utc)
    results = {}
    errors = []
    backfill = []
    overall_success = True
    time_delta = "5y"

    with SessionLocal() as session:
        exists = session.query(PullLog).filter(
            PullLog.is_success == True
        ).order_by(PullLog.pulled_at.desc()).first()

        if exists:
            last_pull = exists.pulled_at
            # Make last_pull timezone aware if it isn't
            if last_pull.tzinfo is None:
                last_pull = last_pull.replace(tzinfo=timezone.utc)
            delta = today - last_pull
            time_delta = f"{delta.days if delta.days > 0 else 1}d"
            pulled_tickers = exists.tickers_pulled
            backfill = list(set(active_tickers) - set(pulled_tickers or []))
            logger.info(f"[pull] Last pull: {last_pull}, delta: {time_delta}, backfill: {backfill}")
        else:
            backfill = active_tickers
            logger.info(f"[pull] No previous pull found — full backfill for all tickers")

    for t in active_tickers:
        info = {}
        time_period = "5y" if t in backfill else time_delta
        logger.info(f"[pull] Pulling {t} with period={time_period}")

        try:
            ticker_data = yf.download(t, period=time_period, interval="1d", progress=False)
            save_raw_data(t, ticker_data)
            info["success"] = True
            info["period"] = time_period
            logger.info(f"[pull] {t} pulled successfully")

        except Exception as e:
            logger.error(f"[pull] Error pulling {t}: {type(e).__name__}: {e}")
            overall_success = False
            errors.append(f"[{t}] {type(e).__name__}: {e}")
            info["success"] = False
            info["error"] = str(e)

        finally:
            results[t] = info

    # Truncate error message to prevent DB black screen
    error_message = "\n\n".join(errors)[:2000] if errors else None

    with SessionLocal() as session:
        try:
            new_entry = PullLog(
                tickers_pulled=active_tickers,
                is_success=overall_success,
                error_message=error_message
            )
            session.add(new_entry)
            session.commit()
            logger.info(f"[pull] PullLog written — success={overall_success}")
        except Exception as e:
            logger.error(f"[pull] Failed to write PullLog: {type(e).__name__}: {e}")
            session.rollback()

    return results