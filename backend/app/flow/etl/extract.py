import pandas as pd

from sqlalchemy import select
from ...database import SessionLocal, BronzeStock

def get_json_bronze(ticker):
    with SessionLocal() as session: 
        statement = select(BronzeStock.raw_json).filter_by(ticker = ticker)
        json_data = session.scalar(statement)

        if json_data is None:
            raise ValueError(f"No bronze data found for ticker: {ticker}")


        df = pd.read_json(json_data)

        return df

def update_dataframe(ticker, dataframe): 
    bronze_df = get_json_bronze(ticker)

    if bronze_df is None: 
        return dataframe

    compiled_df = (pd.concat([bronze_df, dataframe])
        .reset_index(names = 'timestamp')
        .drop_duplicates(subset = 'timestamp')
        .set_index('timestamp')
        .sort_index()
    )   
    
    return compiled_df