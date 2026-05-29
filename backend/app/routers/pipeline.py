import subprocess
from fastapi import APIRouter

router = APIRouter(
    prefix = "/pipeline",
    tags = ["pipeline"]
)

@router.post("/run")
async def trigger_pipeline():
    try: 
        