# Imports
import os
import math
import yfinance as yf
import pandas as pd

from sqlalchemy import func
from datetime import datetime, timedelta
from ..backend.app.database import SessionLocal, BronzeStock, Watchlist, PullLog
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
            exists.raw_json = merged.to_json()
            exists.ingested_at = func.now()
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
    with SessionLocal() as session: 
        exists = session.query(PullLog).filter(PullLog.is_success == True).order_by(PullLog.pulled_at.desc()).first()

    if not exists: 
        time_period = "5y"

    else: 
        today = datetime.now()
        last_pull = exists.pulled_at
        delta = today - last_pull
        time_period = f"{math.ceil(delta.days)}d"

    active_tickers = get_active_watchlist()
    
    for t in active_tickers: 
        ticker_data = yf.download(t, period = time_period, interval = "1d")
        save_raw_data(ticker_data)