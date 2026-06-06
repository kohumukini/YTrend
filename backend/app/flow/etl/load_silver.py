import traceback

from sqlalchemy.dialects.postgresql import insert
from ...database import SilverStock, SessionLocal
    
def update_silver(ticker, df): 
    df.index.name = "timestamp"
    df = df.reset_index()
    df['ticker'] = ticker
    
    print(f"[load_silver] Columns before rename: {df.columns.tolist()}")
    
    df = df.rename(columns={
        "Close": "close_price",
        "Volume": "volume",
        "High": "high",
        "Low": "low",
        "Open": "open_price",
    })
    
    used_columns = {
        "ticker", "timestamp", "close_price", "open_price", "high", "low", "volume",
        "rsi_14", "ewm_rsi_14", "sma_20", "sma_50", "sma_100",
        "volatility_30", "bollinger_band_upper_30", "bollinger_band_lower_30", "bollinger_band_mid_30"

    }
    
    df = df[[col for col in df.columns if col in used_columns]]
    print(f"[load_silver] Columns after rename/filter: {df.columns.tolist()}")

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
            print(f"[load_silver] successfully upserted {len(df_mapping)} rows for {ticker}")

        except Exception as e: 
            print(f"[load_silver] Error: {type(e).__name__}")
            print(f"[load_silver] Error Traceback: {traceback.format_exc()}")
            session.rollback()
            raise