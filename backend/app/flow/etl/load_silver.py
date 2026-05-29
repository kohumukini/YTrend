import traceback

from sqlalchemy.dialects.postgresql import insert
from ...database import SilverStock, SessionLocal
    
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