from ..database import get_db_session, PullLog
from ..schema import PullLogItem
from ..flow.logger import logger
from ..flow.flow import flow_pipeline
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/pipeline",
    tags = ["pipeline"]
)

@router.post("/run")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    logger.info("Pipeline starting (API) ...")
    background_tasks.add_task(flow_pipeline)
    logger.info("Pipeline successfully run (API)!")
    return {"message": "Pipeline triggered successfully"}

@router.get("/status", response_model = PullLogItem)
def get_pipeline_status(db: Session = Depends(get_db_session)):
    latest = db.query(PullLog).order_by(PullLog.pulled_at.desc()).first()
    
    if not latest: 
        raise HTTPException(status_code = 404, detail = "No pipeline runs found")
    return latest