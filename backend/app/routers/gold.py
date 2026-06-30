from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db_session, GoldStock
from ..schema import GoldDataItem as GoldSchema
from ..flow.logger import logger

router = APIRouter(
    prefix= "/gold", 
    tags = ["gold"]
)

@router.get("/{ticker}", response_model = GoldSchema)
def get_gold_data(ticker: str, db: Session = Depends(get_db_session)): 
    row = db.query(GoldStock).filter(GoldStock.ticker == ticker).order_by(GoldStock.timestamp.desc()).first()
    
    if row: 
        logger.info(f"Found gold data for {ticker}")
        return row
    else: 
        logger.warning(f"Gold data for {ticker} not found")
        raise HTTPException(
            status_code = 404, 
            detail = f'No gold data found for {ticker}'
        )