// Raw API Output

export interface RawSilverItem {
    ticker: string;
    timestamp: string;
    close_price: number;
    open_price: number;
    high: number;
    low: number;
    volume: number;

    rsi_14?: number;
    ewm_rsi_14?: number; 
    sma_20?: number; 
    sma_50?: number;
    sma_100?: number; 
    volatility_30?: number; 
    bollinger_band_upper_30?: number;
    bollinger_band_lower_30?: number;
    bollinger_band_mid_30?: number;
}

export interface RawGoldItem {
    ticker: string; 
    timestamp: string; 
    actual_price: number;
    lstm_prediction?: number;
    buy_signal?: string; 
    confidence_score: number;
}

export interface RawWatchListItem {
    ticker: string;
    date_added: string; 
    status: string;
}

export interface ChartDataPoint {
    date: number; 
    close: number; 
    rsi?: number; 
    sma_20?: number; 
    sma_50?: number; 
    sma_100?: number; 
    bb_upper_30?: number; 
    bb_mid_30?: number; 
    bb_lower_30?: number; 
}

export interface SidebarStats {
    currentPrice: number; 
    volume: number; 
    yearlyHigh: number; 
    yearlyLow: number; 
    volatility: number; 
}

export interface PredictionData {
    forecast?: number; 
    signal?: string;
    confidence?: number; 
}