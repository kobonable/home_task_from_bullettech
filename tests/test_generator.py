from ohlc_generator import get_ohlc_from_ticks, read_config, _CONFIG 
import pytest

read_config('trading_settings.yaml')

@pytest.mark.parametrize("ticks, expected_ohlc", [
    ([100, 101, 102, 103, 104], {
        'open': 100,
        'high': 104,
        'low': 100,
        'close': 104,
        'typical_price': 102.0,
    }),
    ([50, 55, 53, 52, 54], {
        'open': 50,
        'high': 55,
        'low': 50,
        'close': 54,
        'typical_price': 53.0,
    }),
    ([200, 198, 202, 202], {
        'open': 200,
        'high': 202,
        'low': 198,
        'close': 202,
        'typical_price': 200.0,
    }),
    ([100], {
        'open': 100,
        'high': 100,
        'low': 100,
        'close': 100,
        'typical_price': 100.0,
    }),
    ([], None),
])
def test_get_ohlc_from_ticks(ticks, expected_ohlc):
    """Test the get_ohlc_from_ticks function with various tick inputs."""
    if expected_ohlc is None:
        ohlc = get_ohlc_from_ticks(ticks)
        assert ohlc is None
    else:
        ohlc = get_ohlc_from_ticks(ticks)
        assert ohlc['open'] == expected_ohlc['open']
        assert ohlc['high'] == expected_ohlc['high']
        assert ohlc['low'] == expected_ohlc['low']
        assert ohlc['close'] == expected_ohlc['close']
        assert ohlc['typical_price'] == pytest.approx(expected_ohlc['typical_price'])
        assert isinstance(ohlc['volume'], int)
        assert _CONFIG['volume_min'] <= ohlc['volume'] <= _CONFIG['volume_max']

