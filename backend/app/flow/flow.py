from .logger import logger
from .etl.transform import transform
from .pull import pull_data
from .etl.load_silver import update_silver
from .etl.load_gold import update_goldstock
from .etl.extract import get_json_bronze
from ..database import SessionLocal, PullLog

#@task(retries = 3, retry_delay_seconds = 60)
def bronze_task():
    return pull_data()

#@task
def transform_task(df): 
    return transform(df)

#@task 
def silver_task(ticker, df): 
    update_silver(ticker, df)
    
def gold_task(ticker, df): 
    logger.info(f"[load_gold] Incoming columns for {ticker}: {df.columns.tolist()}")
    update_goldstock(ticker, df)

#@flow(name = "YTrend Pipeline")
def flow_pipeline():
    logger.info("Pipeline starting...")
    response = bronze_task()
    
    pipeline_errors = []

    for t, info in response.items(): 
        if info["success"]: 
            try: 
                df = get_json_bronze(t)
                transformed_df = transform_task(df)
                # load_silver adjusted to also return silver_df to load into gold_df
                silver_task(t, transformed_df)
                logger.info(f"[{t}] Silver updated successfully")
                
                gold_task(t, transformed_df)
                logger.info(f"[{t}] Gold updated successfully")
            except ValueError as e: 
                logger.error(f"[{t}] Extract failed: {e}")
                pipeline_errors.append(f"[{t}] ValueError: {e}")
                
            except Exception as e: 
                logger.error(f"[{t}] Pipeline failed: {type(e).__name__}: {e}")
                pipeline_errors.append(f"[{t}] {type(e).__name__}: {e}")
        else: 
            logger.warning(f"[{t}] Bronze pull unsuccessful - skipping {t}")
            
    if pipeline_errors: 
        with SessionLocal() as session: 
            latest = session.query(PullLog).order_by(PullLog.pulled_at.desc()).first()
            if latest: 
                latest.is_success = False
                latest.error_message = (latest.error_message or "") + "\nPipeline Errors:\n" + "\n".join(pipeline_errors)
                session.commit()
            logger.error(f"Pipeline completed with {len(pipeline_errors)} error(s)")
            
    logger.info("flow_pipeline complete")