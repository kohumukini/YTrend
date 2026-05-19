import traceback

from sqlalchemy.dialects.postgresql import insert
from ...backend.app.database import SilverStock, SessionLocal


def load_silver(ticker, df): 
    if df.empty: 
        print(f"No data for {ticker}: Skipping...")
        return
        
    # Standardizing the index name
    df.index.name = "Datetime"

    # Resetting the index to push it as a column
    df = df.reset_index()

    # Adding the ticker name to each column
    df['ticker'] = ticker

    # Adjusting names. Assuming perfect intake from transform.py
    # May adjust at a later date
    nameChange = {
        "Close": "close_price", 
        "Volume": "volume", 
        "Datetime": "timestamp", 
        "RSI_14": "rsi_14", 
        "EWM_RSI_14": "ewm_rsi_14", 
        "SMA_20": "sma_20", 
        "SMA_50": "sma_50", 
        "SMA_100": "sma_100",
        "Volatility_30": "volatility_30", 
        "BBU_30": "bollinger_band_upper_30", 
        "BBL_30": "bollinger_band_lower_30", 
        "SMA_30": "bollinger_band_mid_30", 
        "High": "high", 
        "Low": "low", 
        "Open": "open_price"
    }

    # Rename call
    df = df.rename(columns = nameChange)

    df_mapping = df.to_dict(orient = 'records')

    with SessionLocal() as session: 
        try: 
            # After converting df into a dictionary, import all of the data
            session.bulk_insert_mappings(SilverStock, df_mapping)
            session.commit()
        except Exception as e: 
            print(f"Error: {type(e).__name__}")
            print(f"Error Traceback: {traceback.format_exc()}")
            session.rollback()
    
def update_silver(ticker, df): 
    with SessionLocal() as session: 
        statement = insert(SilverStock).values(
            ticker
        )