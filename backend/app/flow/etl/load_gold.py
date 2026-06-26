import traceback
import torch

from sqlalchemy.dialects.postgresql import insert
from ...database import GoldStock, SessionLocal
from ..logger import logger
from ..model import load_models, create_dataloader, rescale_prediction
from .transform_gold import transform_gold

def update_goldstock(ticker, df, prob_threshold, magnitude_threshold): 
    if df is None or df.empty: 
        logger.error(f"[load_gold] Emtpy dataframe received for {ticker}")
        
    actual_pct_change = (df.loc[0, 'target'] - df.loc[20, 'target']) / df.loc[0, 'target']

    base_df = transform_gold(df)
    pred_model, class_model = load_models

    input_tensor = create_dataloader(df)
    with torch.no_grad(): 
        raw_prediction = pred_model(input_tensor)
        probability = class_model(input_tensor)
        
    prediction_pct = rescale_prediction(raw_prediction) 
    
    if probability > prob_threshold and prediction_pct > magnitude_threshold:
        signal = "BUY"
    elif probability < (1 - prob_threshold) and prediction_pct < -magnitude_threshold:
        signal = "SELL"
    else:
        signal = "HOLD"
    
    gold_data = {
        'ticker':      ticker,
        'magnitude':   f"{(prediction_pct * 100):.2f}%",
        'direction':   'UP' if probability > 0.5 else 'DOWN',
        'confidence':  f"{max(probability, 1-probability) * 100:.2f}%",
        'signal':      signal
    }
        
    with SessionLocal() as session: 
        try: 
            statement = session.insert()