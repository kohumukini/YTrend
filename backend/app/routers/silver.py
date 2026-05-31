from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db_session, SilverStock
from ..schema import SilverDataItem as SilverSchema
from ..flow.logger import logger

router = APIRouter(
    prefix = "/silver",
    tags = ["silver"]
)

@router.get("/{ticker}/data", response_model = list[SilverSchema])
def get_silver_data(ticker: str, limit: int = 365,  db: Session = Depends(get_db_session)):
    rows = db.query(SilverStock).filter(SilverStock.ticker == ticker).order_by(SilverStock.timestamp.desc()).limit(limit).all()
    
    if rows: 
        logger.info(f"Found {len(rows)} rows for {ticker} in silver")
        
        return rows
    else: 
        logger.warning(f"No data found for {ticker} in silver")
        return {"message": f"No data found for {ticker} in silver"}