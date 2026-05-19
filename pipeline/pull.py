# Imports
import os
import yfinance as yf

from sqlalchemy import func
from ..backend.app.database import SessionLocal, BronzeStock, Watchlist
from .etl.extract import get_json_bronze, update_dataframe

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
            exists.raw_json = merged.to_json()
            exists.ingested_at = func.now()
        else:
            new_entry = BronzeStock(
                ticker = ticker, 
                raw_json = merged.to_json()
                ingested_at = func.now()
            )

            session.add(new_entry)

        session.commit()
        print(f"Saved {ticker} data")
        
def pull_data(backfill = False):
    active_tickers = get_active_watchlist()

    for t in active_tickers: 
        if backfill: 
            ticker_data = yf.download(t, period = "5y", interval = "1d")
        else: 
            ticker_data = yf.download(t, period = "1h", interval = "1m")
        
        save_raw_data(t, ticker_data)