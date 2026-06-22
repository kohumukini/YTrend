import pandas as pd

from sqlalchemy import select
from ...database import SessionLocal, BronzeStock
from ..logger import logger
from io import StringIO

def get_json_bronze(ticker):
    with SessionLocal() as session: 
        statement = select(BronzeStock.raw_json).filter_by(ticker = ticker)
        json_data = session.scalar(statement)

        if json_data is None:
            raise ValueError(f"No bronze data found for ticker: {ticker}")
        
        # If the json data received is a string 
        try:
            if isinstance(json_data, str): 
                df = pd.read_json(StringIO(json_data))
            elif isinstance(json_data, dict): 
                df = pd.DataFrame(json_data)
            else: 
                raise ValueError(f"Unexpected json_data type for {ticker}: {type(json_data)}")
        except Exception as e:
            raise ValueError(f"Failed to parse bronze data for {ticker}: {type(e).__name__}") from None


        logger.info(f"[extract] Columns for {ticker}: {df.columns.tolist()}")
        logger.info(f"[extract] Shape for {ticker}: {df.shape}")
        
        return df

def update_dataframe(ticker, dataframe): 
    try: 
        bronze_df = get_json_bronze(ticker)
    except ValueError as e: 
        logger.warning(f"[extract] No existing data for {ticker}. Using new data only: {e}")
        return dataframe

    compiled_df = (pd.concat([bronze_df, dataframe])
        .reset_index(names = 'timestamp')
        .drop_duplicates(subset = 'timestamp')
        .set_index('timestamp')
        .sort_index()
    )   
    
    return compiled_df