from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AppBase(BaseModel):
    model_config = ConfigDict(from_attributes = True)

class WatchlistItem(AppBase): 
    ticker: str
    date_added: datetime
    status: str
    
class PullLogItem(AppBase):
    pulled_at: datetime
    tickers_pulled: list[str]
    error_message: str | None
    is_success: bool
    
class BronzeDataItem(AppBase): 
    ticker: str
    raw_json: dict
    ingested_at: datetime
    
class SilverDataItem(AppBase):
    ticker: str
    timestamp: datetime
    close_price: float
    open_price: float
    high: float
    low: float
    volume: float

    rsi_14: float | None
    ewm_rsi_14: float | None
    sma_20: float | None
    sma_50: float | None
    sma_100: float | None
    volatility_30: float | None
    bollinger_band_upper_30: float | None
    bollinger_band_lower_30: float | None
    bollinger_band_mid_30: float | None
    
class GoldDataItem(AppBase):
    ticker: str
    timestamp: datetime
    last_month_pct_change: float
    predicted_pct_change: float | None
    direction: str | None
    signal: str | None
    confidence: float | None
    