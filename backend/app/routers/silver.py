from fastapi import APIRouter, Depends
from ..database import get_db_session, SilverStock
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/silver",
    tags = ["silver"]
)

@router.get("/{ticker}/data", response_model = list[SilverStock], limit = 365)
def get_silver_data(ticker: str, db: Session = Depends(get_db_session)):
    rows = db.query(SilverStock).filter(SilverStock.ticker == ticker).order_by(SilverStock.date.desc()).limit(365).all()
    
    if rows: 
        print(f"Found {len(rows)} rows for {ticker} in silver")
        
        return rows
    else: 
        print(f"No data found for {ticker} in silver")
        return {"message": f"No data found for {ticker} in silver"}