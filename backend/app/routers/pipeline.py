from fastapi import APIRouter, BackgroundTasks
from ..flow.logger import logger
from ..flow.flow import flow_pipeline

router = APIRouter(
    prefix = "/pipeline",
    tags = ["pipeline"]
)

@router.post("/run")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    logger.info("Pipeline starting (API) ...")
    background_tasks.add_task(flow_pipeline)
    return {"message": "Pipeline triggered successfully"}