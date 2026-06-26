# Imports server session & Watchlist class
from .database import SessionLocal, Watchlist

# Default tickers to test
TICKERS_TO_TRACK = ["AAPL", "TSLA", "NVDA", "MSFT"]

def seed_watchlist(): 
    # `with` opens and closes the session while allowing the use of session with an alias
    with SessionLocal() as session: 

        # For each ticker within 
        for t in TICKERS_TO_TRACK:
            # Check if the ticker exists  
            exists = session.query(Watchlist).filter_by(ticker = t).first()

            # Otherwise add it to the watchlist and commit it
            if not exists: 
                new_ticker = Watchlist(
                    ticker = t, 
                    status = "active"
                )

                session.add(new_ticker)

        session.commit()
        print("Watchlist seeded successfully")

if __name__ == "__main__": 
    seed_watchlist()