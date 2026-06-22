import traceback

from sqlalchemy.dialects.postgresql import insert
from ...database import SilverStock, SessionLocal
from ..logger import logger
    
def update_silver(ticker, df): 
    if df is None or df.empty: 
        logger.warning(f"[load_silver] Empty dataframe received for {ticker} - skipping")
        return
    
    df.index.name = "timestamp"
    df = df.reset_index()
    df['ticker'] = ticker
    
    logger.info(f"[load_silver] Columns before rename for {ticker}: {df.columns.tolist()}")
    
    df = df.rename(columns={
        "Close": "close_price",
        "Volume": "volume",
        "High": "high",
        "Low": "low",
        "Open": "open_price",
    })
    
    valid_cols = {
        "ticker", "timestamp", "close_price", "open_price", "high", "low", "volume",
        "rsi_14", "ewm_rsi_14", "sma_20", "sma_50", "sma_100",
        "volatility_30", "bollinger_band_upper_30", "bollinger_band_lower_30", "bollinger_band_mid_30"

    }
    
    missing_cols = valid_cols - set(df.columns)
    if missing_cols: 
        logger.warning(f"[load_silver] Missing expected columns for {ticker}: {missing_cols}")
    
    df = df[[col for col in df.columns if col in valid_cols]]
    logger.info(f"[load_silver] Columns after rename/filter: {df.columns.tolist()}")
    
    if df.empty: 
        logger.warning(f"[load_silver] No valid columns remaining for {ticker} after filter - skipping")

    df_mapping = df.to_dict(orient = 'records')

    with SessionLocal() as session: 
        try: 
            statement = insert(SilverStock).values(df_mapping)
            statement = statement.on_conflict_do_update(
                index_elements = ['ticker', 'timestamp'], 
                set_ = {c.key: c for c in statement.excluded if c.key not in ('ticker', 'timestamp')}
            )

            session.execute(statement)
            session.commit()
            logger.info(f"[load_silver] Successfully upserted {len(df_mapping)} rows for {ticker}")

        except Exception as e: 
            logger.error(f"[load_silver] Error: {type(e).__name__}")
            logger.error(f"[load_silver] Error Traceback: {traceback.format_exc()}")
            session.rollback()
            raise