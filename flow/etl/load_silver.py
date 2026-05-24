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
        "Datetime": "timestamp", 
        "Close": "close_price", 
        "Volume": "volume",  
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
    df.index.name = "timestamp"
    df = df.reset_index()
    df['ticker'] = ticker
    df = df.rename(columns={"Close": "close_price", "Volume": "volume", "High": "high", "Low": "low", "Open": "open_price", "Datetime": "timestamp"})
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

        except Exception as e: 
            print(f"Error: {type(e).__name__}")
            print(f"Error Traceback: {traceback.format_exc()}")
            session.rollback()