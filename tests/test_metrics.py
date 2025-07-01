from ohlc_metrics_enrichment import aggregate_by_periods_with_vwap, add_moving_average, add_moving_median, calculate_bar_window
import pandas as pd
import pytest

@pytest.fixture
def sample_df():
    """Creates a sample DataFrame for testing."""
    data = {
        'open': [100, 102, 104],
        'high': [105, 107, 109],
        'low': [95, 97, 99],
        'close': [102, 106, 108],
        'volume': [1000, 1500, 2000],
        'typical_price': [100.67, 103.33, 104.67]
    }
    return pd.DataFrame(data, index=pd.date_range('2025-01-01', periods=3, freq='D'))

@pytest.mark.parametrize("period, expected_freq", [
    ('5min', '5T'),
    ('30min', '30T'),
    ('1D', 'D')
])
def test_aggregate_by_periods_with_vwap(sample_df, period, expected_freq):
    """Tests the aggregation of OHLC data by different time periods."""
    df = sample_df.copy()
    df.index.name = 'dt'
    df.index.freq = 'D'
    aggregated_df = aggregate_by_periods_with_vwap(df, period)
    assert aggregated_df.index.freqstr == expected_freq
    assert 'vwap' in aggregated_df.columns


@pytest.mark.parametrize("window_size_minutes, bar_interval_minutes, expected_window_bars, expected_ma, expected_median", [
    (30, 5, 6, 
     [None, None, None, None, None, 103.0, 104.333333, 106.0, 107.666667, 109.0, 110.333333, 112.0, 113.666667, 115.0, 116.333333], 
     [None, None, None, None, None, 103.0, 104.0, 106.0, 107.0, 109.0, 110.0, 112.0, 113.0, 115.0, 116.0]
    ),
    (30, 30, 1, [100, 102, 104], [100, 102, 104]), # For 30min bar, 30min MA/Median means current bar only
])
def test_add_moving_average_and_median(window_size_minutes, bar_interval_minutes, expected_window_bars, expected_ma, expected_median):
    """Tests the addition of moving average and median columns with dynamic window calculation."""
    # Create a dummy DataFrame with more data to test rolling window
    dates = pd.date_range('2025-01-01 09:30', periods=15, freq=f'{bar_interval_minutes}min')
    data = {
        'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
    }
    df = pd.DataFrame(data, index=dates)
    df.index.name = 'dt'
    df.index.freq = f'{bar_interval_minutes}min'

    df_with_ma = add_moving_average(df.copy(), window_size_minutes, bar_interval_minutes)
    df_with_median = add_moving_median(df.copy(), window_size_minutes, bar_interval_minutes)
    
    ma_col_name = f'ma_{window_size_minutes}min'
    median_col_name = f'median_{window_size_minutes}min'

    assert ma_col_name in df_with_ma.columns
    assert median_col_name in df_with_median.columns

    # Check expected NaN values at the beginning
    assert df_with_ma[ma_col_name].isnull().sum() == expected_window_bars - 1
    assert df_with_median[median_col_name].isnull().sum() == expected_window_bars - 1

    # Check the calculated values (approximate for floats)
    expected_ma_series = pd.Series(expected_ma, index=dates)
    expected_median_series = pd.Series(expected_median, index=dates)

    pd.testing.assert_series_equal(df_with_ma[ma_col_name].fillna(0), expected_ma_series.fillna(0), check_dtype=False, check_less_precise=True)
    pd.testing.assert_series_equal(df_with_median[median_col_name].fillna(0), expected_median_series.fillna(0), check_dtype=False, check_less_precise=True)

def test_calculate_bar_window():
    assert calculate_bar_window(30, 5) == 6
    assert calculate_bar_window(30, 30) == 1
    assert calculate_bar_window(60, 15) == 4
    assert calculate_bar_window(10, 1) == 10
    with pytest.raises(ValueError):
        calculate_bar_window(30, 0)