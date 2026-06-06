# Imports
import os
import math
import yfinance as yf
import pandas as pd

from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from ..database import SessionLocal, BronzeStock, Watchlist, PullLog
from .etl.extract import update_dataframe

def get_active_watchlist(): 
    with SessionLocal() as session: 
        tickers = session.query(Watchlist).filter(Watchlist.status == 'active').all()
        return [t.ticker for t in tickers]
    
def save_raw_data(ticker, dataframe): 
    if dataframe.empty: 
        print(f"No data for {ticker}: Skipping... ")
        return
    # Start the session -> Connect to server
    with SessionLocal() as session: 
        # Dataframe as argument
        dataframe = dataframe.copy()
        dataframe.columns = dataframe.columns.droplevel(1)
        # Dataframe that exists
        exists = session.query(BronzeStock).filter_by(ticker = ticker).first()
        merged = update_dataframe(ticker, dataframe)

        if exists: 
            exists.raw_json = merged.to_json() # type: ignore
        else:
            new_entry = BronzeStock(
                ticker = ticker, 
                raw_json = merged.to_json(),
                ingested_at = func.now()
            )

            session.add(new_entry)

        session.commit()
        print(f"Saved {ticker} data")
        
def pull_data():
    active_tickers = get_active_watchlist()
    today = datetime.now(tz = timezone.utc)

    results = {}

    errors = []
    backfill = []

    overall_success = True
    time_delta = "5y"

    with SessionLocal() as session: 
        exists = session.query(PullLog).filter(PullLog.is_success == True).order_by(PullLog.pulled_at.desc()).first()

        if exists: 
            last_pull = exists.pulled_at
            delta = today - last_pull
            time_delta = f"{math.ceil(1, delta.days)}d"

            pulled_tickers = exists.tickers_pulled
            backfill = list(set(active_tickers) - set(pulled_tickers)) # type: ignore 
        else: 
            backfill = active_tickers


    for t in active_tickers: 
        info = {}

        if t in backfill: 
            time_period = "5y"
        else: 
            time_period = time_delta


        try: 
            ticker_data = yf.download(t, period = time_period,  interval = "1d")
            save_raw_data(t, ticker_data)

            info["success"] = True
            info["period"] = time_period
        except Exception as e: 
            print(f"Error: {e}")
            overall_success = False
            errors.append(str(e))

            info["success"] = False
            info["error"] = str(e)

            continue
        finally: 
            results[t] = info

    with SessionLocal() as session: 
        new_entry = PullLog(
            tickers_pulled = active_tickers, 
            is_success = overall_success, 
            error_message = "\n\n".join(errors) if errors else None
        )

        session.add(new_entry)
        session.commit()

    return results