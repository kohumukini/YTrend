import traceback
import torch

from sqlalchemy.dialects.postgresql import insert
from ...database import GoldStock, SessionLocal
from ..logger import logger
from ..model import load_models, WINqDOW_SIZE
from .transform_gold import transform_gold

PROB_THRESHOLD = 0.65
MAGNITUDE_THRESHOLD = 0.03

def update_goldstock(ticker, df):
    if df is None or df.empty:
        logger.warning(f"[load_gold] Empty dataframe received for {ticker} — skipping")
        return

    if len(df) < 22:
        logger.warning(f"[load_gold] Not enough rows for {ticker} to calculate actual_pct_change")
        return

    # Calculate actual pct change before transform_gold drops Close
    last_close = df['Close'].iloc[-1]
    close_21_ago = df['Close'].iloc[-22]
    last_month_pct_change = float((last_close - close_21_ago) / close_21_ago * 100)

    # Transform to gold feature space — needs full history for rolling calcs
    gold_df = transform_gold(df)
    if gold_df is None or gold_df.empty:
        logger.error(f"[load_gold] transform_gold failed for {ticker}")
        return

    if len(gold_df) < WINDOW_SIZE:
        logger.warning(f"[load_gold] Not enough rows after transform for {ticker}: {len(gold_df)} < {WINDOW_SIZE}")
        return

    # Load models and artifacts
    pred_model, class_model, scaler, y_mean, y_std = load_models()

    # Build input tensor from last WINDOW_SIZE rows
    feature_cols = [c for c in gold_df.columns if c not in ('target', 'ticker', 'timestamp')]
    last_window = gold_df[feature_cols].tail(WINDOW_SIZE).values
    last_window_scaled = scaler.transform(last_window)
    tensor = torch.tensor(last_window_scaled, dtype=torch.float32).unsqueeze(0)

    # Run inference
    with torch.no_grad():
        raw_prediction = pred_model(tensor).squeeze().item()
        probability = torch.sigmoid(class_model(tensor).squeeze()).item()

    # Rescale from standardized space back to pct change
    prediction_pct = float((raw_prediction * y_std) + y_mean)

    # Generate signal
    if probability > PROB_THRESHOLD and prediction_pct > MAGNITUDE_THRESHOLD:
        signal = "BUY"
    elif probability < (1 - PROB_THRESHOLD) and prediction_pct < -MAGNITUDE_THRESHOLD:
        signal = "SELL"
    else:
        signal = "HOLD"

    gold_data = {
        'ticker': ticker,
        'predicted_pct_change': prediction_pct * 100,
        'direction': 'UP' if probability > 0.5 else 'DOWN',
        'confidence': float(max(probability, 1 - probability)),
        'signal': signal,
        'last_month_pct_change': last_month_pct_change,
    }

    logger.info(f"[load_gold] {ticker} — signal: {signal}, pred: {prediction_pct*100:.2f}%, actual: {last_month_pct_change:.2f}%, confidence: {probability:.2%}")

    with SessionLocal() as session:
        try:
            statement = insert(GoldStock).values(gold_data)
            statement = statement.on_conflict_do_update(
                index_elements=['ticker', 'timestamp'],
                set_={c.key: c for c in statement.excluded if c.key not in ('ticker', 'timestamp')}
            )
            session.execute(statement)
            session.commit()
            logger.info(f"[load_gold] Successfully upserted gold data for {ticker}")
        except Exception as e:
            logger.error(f"[load_gold] Error: {type(e).__name__}")
            logger.error(f"[load_gold] Traceback: {traceback.format_exc()}")
            session.rollback()
            raise