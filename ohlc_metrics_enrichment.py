import pandas as pd


def aggregate_by_periods_with_vwap(df: pd.DataFrame, period: str):
    "Aggregates OHLC data by time window (5 minute, 30 minute, 1 day)."
    df['price_x_volume'] = df['typical_price'] * df['volume']
    df = df.resample(period).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'price_x_volume': 'sum'
    }).dropna()
    df.index.name = 'dt'
    df.index.freq = period
    df['vwap'] = df['price_x_volume'] / df['volume']
    df.drop(columns=['price_x_volume'], inplace=True)
    return df


def agg_to_5min(df: pd.DataFrame):
    "Aggregates OHLC data to 5 minute intervals."
    return aggregate_by_periods_with_vwap(df, '5min')


def agg_to_30min(df: pd.DataFrame):
    "Aggregates OHLC data to 30 minute intervals."
    return aggregate_by_periods_with_vwap(df, '30min')


def agg_to_1day(df: pd.DataFrame):
    "Aggregates OHLC data to 1 day intervals."
    return aggregate_by_periods_with_vwap(df, '1D')


def calculate_bar_window(window_size_minutes: int, bar_interval_minutes: int):
    """Calculates the number of bars for a given window size and bar interval."""
    if bar_interval_minutes == 0:
        raise ValueError("Bar interval cannot be zero.")
    return max(1, window_size_minutes // bar_interval_minutes)

def add_moving_average(df: pd.DataFrame, window_size_minutes: int, bar_interval_minutes: int):
    "Adds a moving average column to the DataFrame using a calculated window size."
    window = calculate_bar_window(window_size_minutes, bar_interval_minutes)
    df[f'ma_{window_size_minutes}min'] = df['close'].rolling(window=window).mean()
    return df

def add_moving_median(df: pd.DataFrame, window_size_minutes: int, bar_interval_minutes: int):
    "Adds a moving median column to the DataFrame using a calculated window size."
    window = calculate_bar_window(window_size_minutes, bar_interval_minutes)
    df[f'median_{window_size_minutes}min'] = df['close'].rolling(window=window).median()
    return df