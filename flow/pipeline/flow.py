import logging
from prefect import task, flow

from ..etl.transform import transform
from ..pull import pull_data
from ..etl.load_silver import update_silver
from ..etl.extract import get_json_bronze

@task(retries = 3, retry_delay_seconds = 60)
def bronze_task():
    return pull_data()

@task
def transform_task(df): 
    return transform(df)

@task 
def silver_task(ticker, df): 
    update_silver(ticker, df)

@flow(name = "YTrend Pipeline")
def flow_pipeline():
    response = bronze_task()

    for t, info in response.items(): 
        if info["success"]: 
            df = get_json_bronze(t)
            if df is not None: 
                transformed_df = transform_task(df)
                silver_task(t, transformed_df)
            else: 
                logging.warning(f"{t} returned None from bronze - Skipping")