import numpy as np
from ..logger import logger

def transform_gold(dataframe): 
    df = dataframe.copy()
    
    df = df.drop(['High', 'Low', 'Open'], axis=1, errors="ignore")
    
    # Assest that values match
    expected_columns = {
        'Close', 'Volume', 'sma_20', 'sma_50', 'sma_100',
        'rsi_14', 'ewm_rsi_14', 'volatility_30',
        'bollinger_band_upper_30', 'bollinger_band_lower_30', 'bollinger_band_mid_30'
    }
    
    featured_cols = set(df.columns) - {'ticker', 'timestamp'}
    
    if featured_cols != expected_columns: 
        missing = expected_columns - featured_cols
        extra = featured_cols - expected_columns
        logger.error(f"[transform_gold] Column mismatch: Missing - {missing}, Extra - {extra}") 
        return None
    
    columns_to_drop = ['Close', 'Volume', 'sma_20', 'sma_50', 'sma_100', 'volatility_30', 
                        'day_of_week']
    
    # Calculating target
    
    df['target'] = df['Close'].pct_change(21)
    
    target_lower = df["target"].quantile(0.01)
    target_upper = df["target"].quantile(0.99)
    
    df["target"] = df["target"].clip(lower=target_lower, upper=target_upper)
    
    # Calculating Price Relative MA's
    df['close_to_sma_20'] = (df['Close'] / df['sma_20']) - 1
    df['close_to_sma_50'] = (df['Close'] / df['sma_50']) - 1
    
    # Calculating Bollinger Bands
    df["pc_b"] = (df['Close'] - df["bollinger_band_lower_30"]) / (df['bollinger_band_upper_30'] - df['bollinger_band_lower_30'])
    df["pc_b"] = df["pc_b"].clip(lower=0, upper=1)
    
    df['bb_width'] = (df['bollinger_band_upper_30'] - df['bollinger_band_lower_30']) / df['bollinger_band_mid_30']
    df = df.drop(columns=['bollinger_band_upper_30', 'bollinger_band_lower_30', 'bollinger_band_mid_30'])
    
    # Calculating RSI
    threshold = 0.85
    correlation = df[['rsi_14', 'ewm_rsi_14']].corr()
    
    corr_value = correlation.iloc[0, 1]
    
    if abs(corr_value) > threshold: 
        columns_to_drop.append('ewm_rsi_14')
        logger.info(f"RSI Correlation: {corr_value:.3f} - Dropping ewm_rsi_14 {abs(corr_value)} > threshold (0.85)")
        
    # Calculating Volatility
    pct_returns_series = df['Close'].pct_change()
    df['pct_volatility_30'] = pct_returns_series.rolling(window=30, min_periods=30).std()
    
    # Calculating Volume
    volume_pct_change = df["Volume"].pct_change()
    df['volume_pct_change'] = volume_pct_change
    
    vol_lower = df['volume_pct_change'].quantile(0.01)
    vol_upper = df['volume_pct_change'].quantile(0.99)
    
    df['volume_pct_change'] = df['volume_pct_change'].clip(lower=vol_lower, upper=vol_upper)
    
    # Calculating Cyclical Day of the Week
    df['day_of_week'] = df.index.dayofweek
    
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 5)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 5)
    
    # Cleaning up 
    processed_df = df.drop(columns=columns_to_drop)
    
    processed_df = processed_df.dropna()
    logger.info("[transform_gold] Process Complete! Gold Complete")
    
    return processed_df