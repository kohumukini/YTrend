from .logger import logger

from .etl.transform import transform
from .pull import pull_data
from .etl.load_silver import update_silver
from .etl.extract import get_json_bronze

#@task(retries = 3, retry_delay_seconds = 60)
def bronze_task():
    return pull_data()

#@task
def transform_task(df): 
    return transform(df)

#@task 
def silver_task(ticker, df): 
    update_silver(ticker, df)

#@flow(name = "YTrend Pipeline")
def flow_pipeline():
    logger.info("Pipeline starting...")
    response = bronze_task()

    for t, info in response.items(): 
        if info["success"]: 
            try: 
                df = get_json_bronze(t)
                transformed_df = transform_task(df)
                silver_task(t, transformed_df)
                logger.info(f"[{t}] Silver updated successfully")
            except ValueError as e: 
                logger.error(f"[{t}] Error: {e}")
                
            except Exception as e: 
                logger.error(f"[{t}] Pipeline failed: {type(e).__name__}: {e}")
                
        else: 
            logger.warning(f"[{t}] Bronze pull unsuccessful - skipping {t}")
            
    logger.info("flow_pipeline complete")