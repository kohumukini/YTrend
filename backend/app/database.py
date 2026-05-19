import os
from sqlalchemy import Column, BigInteger, Integer, String, Float, Boolean, DateTime, ARRAY, JSON, func, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

# Loading the environment file
load_dotenv()

# Getting the database information from the .env file
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")
PORT = os.getenv("DB_PORT")

# Checking which host to use
if os.getenv("IS_DOCKER") == "true": 
    HOST = "db"
else: 
    HOST = "localhost"

URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
ENGINE = create_engine(URL)

#Create the sessionmaker
# Autocommit = False: Makes user responsible for committing the work - Finalizes and saves changes. Like git push
# Autoflush = False: Makes user responsible for flushing the work - Synchromizes work. Sends the "draft" to be commited. Like git commit
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = ENGINE)

class Base(DeclarativeBase): 
    pass

# Creates the raw data table after importing data from yfinance
class BronzeStock(Base):
    __tablename__ = "bronze_yfinance_raw"

    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    raw_json = Column(JSON)
    ingested_at = Column(DateTime, server_default=func.now())

# Creates the cleaned table after feature engineering and data laundering
class SilverStock(Base):
    __tablename__ = "silver_ticker_features"

    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    timestamp = Column(DateTime)
    close_price = Column(Float)
    open_price = Column(Float)
    high = column(Float)
    low = column(Float)
    volume = Column(Float)

    rsi_14 = Column(Float)
    ewm_rsi_14 = Column(Float)
    sma_20 = Column(Float)
    sma_50 = Column(Float)
    sma_100 = Column(Float)
    volatility_30 = Column(Float)
    bollinger_band_upper_30 = Column(Float)
    bollinger_band_lower_30 = Column(Float)
    bollinger_band_mid_30 = Column(Float)

    __table_args__ = (
        UniqueConstraint('ticker', 'timestamp', name = 'uq_ticker_timestamp')
    )

# Creates the final table where we output predictive data
class GoldStock(Base): 
    __tablename__ = "gold_stock_price"

    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    timestamp = Column(DateTime)
    actual_price = Column(Float)
    lstm_prediction = Column(Float, nullable = True)
    buy_signal = Column(String, nullable = True)
    confidence_score = Column(Float)

class Watchlist(Base): 
    __tablename__ = "stock_watch_list"

    id = Column(Integer, primary_key = True)
    ticker = Column(String)
    date_added = Column(DateTime)
    status = Column(String)

class PullLog(Base): 
    __tablename__ = "yfinance_pull_log"

    id = Column(BigInteger, primary_key = True, autoincrement = True)
    pulled_at = Column(DateTime(timezone = True), server_default = func.now())
    tickers_pulled = Column(ARRAY(Text))
    is_success = Column(Boolean, default = True)
    error_message = Column(Text, nullable = True)

    

def init_db(): 
    Base.metadata.create_all(bind = ENGINE)

def get_db_session(): 
    db = SessionLocal()
    
    try: 
        yield db
    finally: 
        db.close()

if __name__ == "__main__": 
    init_db()
    print("Database tables initialized")