from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db_session, Watchlist
from ..schema import WatchlistItem as WatchListSchema
from ..flow.logger import logger

router = APIRouter(
    prefix = "/watchlist", 
    tags = ["watchlist"]
)

@router.get("/data", response_model = list[WatchListSchema])
def get_watchlist_data(db: Session = Depends(get_db_session)):
    row = db.query(Watchlist).order_by(Watchlist.date_added.desc()).first()
    
    if row: 
        logger.info(f"Found {row} in watchlist")
        return row
    else: 
        logger.warning(f"No data found for watchlist")
        return {"message": "No data found for watchlist"}
    
@router.post("/add/{ticker}", response_model = list[WatchListSchema])
def add_to_watchlist(ticker: str, db: Session = Depends(get_db_session)):
    new_entry = Watchlist(ticker = ticker, status = "active")
    try: 
        db.add(new_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Error occurred while adding {ticker} to watchlist: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding {ticker} to watchlist: {e}")
    db.refresh(new_entry)
    
    logger.info(f"Added {ticker} to watchlist")
    return new_entry

@router.delete("/remove/{ticker}")
def remove_from_watchlist(ticker: str, db: Session = Depends(get_db_session)):
    entry_to_remove = db.query(Watchlist).filter(Watchlist.ticker == ticker).all()
    
    if entry_to_remove: 
        try: 
            db.delete(entry_to_remove)
            db.commit()
            logger.info(f"{ticker} successfully removed from watchlist")
            return {"message": f"{ticker} successfully removed from watchlist"}
            
        except Exception as e: 
            logger.warning(f"Error occured while attempting to remove {ticker}: \n{e}")
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_500_Internal_Service_Error, 
                detail = f"An unexpected error occured while attempting to remove {ticker} from watchlist"
            )