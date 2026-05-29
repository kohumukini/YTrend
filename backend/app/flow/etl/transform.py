import pandas as pd


# Simple Moving Average

def calculate_moving_average(dataframe, window):
    dataframe = dataframe.sort_index()

    col_name = "".join(filter(str.isdigit, str(window)))

    dataframe[f"sma_{col_name}"] = (
        dataframe['Close']
        .rolling(window = window, min_periods = 1)
        .mean()
    )

    return dataframe; 

# RSI Calculations

def calculate_rsi(dataframe, window_size): 
    temp_df = pd.DataFrame({'Difference': dataframe['Close'].diff()})

    temp_df['Gain'] = temp_df['Difference'].clip(lower = 0)
    temp_df['Loss'] = temp_df['Difference'].clip(upper = 0).abs()

    temp_df['Avg_Gain'] = temp_df['Gain'].rolling(window = window_size, min_periods = 1).mean()
    temp_df['Avg_Loss'] = temp_df['Loss'].rolling(window = window_size, min_periods = 1).mean()

    rs = temp_df['Avg_Gain'] / temp_df['Avg_Loss']

    col_name = "".join(filter(str.isdigit, str(window_size)))

    dataframe[f'rsi_{col_name}'] = 100 - (100 / (1 - rs))

    return dataframe

def calculate_ewm_rsi(dataframe, window_size): 
    temp_df = pd.DataFrame({'Difference': dataframe['Close'].diff()})

    temp_df['Gain'] = temp_df['Difference'].clip(lower = 0)
    temp_df['Loss'] = temp_df['Difference'].clip(upper = 0).abs()

    temp_df['Avg_Gain'] = temp_df['Gain'].ewm(span = window_size, adjust = False).mean()
    
    temp_df['Avg_Loss'] = temp_df['Loss'].ewm(span = window_size, adjust = False).mean()

    rs = temp_df['Avg_Gain'] / temp_df['Avg_Loss']

    col_name = "".join(filter(str.isdigit, str(window_size)))

    dataframe[f'ewm_rsi_{col_name}'] = 100 - (100 / (1 - rs))

    return dataframe

# Volatility & Bollinger Bands
def calculate_volatility(dataframe, window_size): 
    col_name = "".join(filter(str.isdigit, str(window_size)))

    dataframe[f'volatility_{col_name}'] = dataframe['Close'].rolling(window = window_size).std()

    return dataframe

def calculate_bollinger_bands(dataframe, window_size, num_std): 
    roll_window = dataframe['Close'].rolling(window = window_size)

    mid_band = roll_window.mean()
    std_dev = roll_window.std()

    col_id = "".join(filter(str.isdigit, str(window_size)))

    dataframe[f'bollinger_band_mid_{col_id}'] = mid_band
    dataframe[f'bollinger_band_upper_{col_id}'] = mid_band + (num_std * std_dev)
    dataframe[f'bollinger_band_lower_{col_id}'] = mid_band - (num_std * std_dev)

    return dataframe

def transform(dataframe): 
    dataframe = calculate_moving_average(dataframe, "20D")
    dataframe = calculate_moving_average(dataframe, "50D")
    dataframe = calculate_moving_average(dataframe, "100D")

    dataframe = calculate_rsi(dataframe, "14D")
    dataframe = calculate_ewm_rsi(dataframe, 14)

    dataframe = calculate_volatility(dataframe, "30D")
    dataframe = calculate_bollinger_bands(dataframe, "30D", 2)

    return dataframe