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

        if exists: 
            merged = update_dataframe(ticker, dataframe)
            exists.raw_json = merged.to_json()
            exists.ingested_at = func.now()
        else:
            new_entry = BronzeStock(
                ticker = ticker, 
                raw_json = dataframe.to_json()
            )

            session.add(new_entry)
        session.commit()
        print(f"Saved {ticker} data")

def data_backfill(): 
    active_tickers = get_active_watchlist()

    for t in active_tickers: 
        with SessionLocal() as session:
            exists = session.query(BronzeStock).filter(BronzeStock.ticker == t).first()

            if exists: 
                ticker_data = yf.download(t, period="1h", interval="1m")
            else: 
                ticker_data = yf.download(t, period="5y", interval="1d")

            save_raw_data(t, ticker_data)
        
def pull_data(ticker, backfill = False) {
    for t in active_tickers: 
        if backfill: 
            ticker_data = yf.download(t, period = "5y", interval = "1d")
        else: 
            ticker_data = yf.download(t, period = "1h", interval = "1m")
        
        save_raw_data(t, ticker_data)
}