import datetime
import random
import yaml
from pandas import DataFrame

_CONFIG = None


def read_config(path):
    """Reads configuration settings from a file."""
    config = yaml.safe_load(open(path, 'r'))
    global _CONFIG
    _CONFIG = config
    return config


def apply_surge(base_value, surge_probability=0, surge_limit=0.5):
    """Applies a surge to the base value based on the given probability and limit."""
    if surge_probability > 0 and random.random() < surge_probability:
        surge = random.uniform(0, surge_limit)
        base_value *= surge if surge > 1 else 1 + surge
    return base_value


def generate_ohlc_data_by_date(date=None, prev_day_close_value=None):
    """Generates OHLC data for a specific date. Uses current date if not provided."""
    read_config('trading_settings.yaml')
    date = date or datetime.datetime.now()
    trading_start = datetime.datetime.combine(date, datetime.datetime.strptime(_CONFIG['trading_day_start'], '%H:%M').time())
    trading_end = datetime.datetime.combine(date, datetime.datetime.strptime(_CONFIG['trading_day_end'], '%H:%M').time())
    minutes_count = int((trading_end - trading_start).total_seconds() / 60)

    prev_close_value = _CONFIG['base_value'] if prev_day_close_value is None else \
        generate_tick(
            prev_day_close_value,
            _CONFIG['daily_shift_min'],
            _CONFIG['daily_shift_max'],
            _CONFIG['daily_surge_probability'],
            _CONFIG['daily_surge_limit']
        )
    
    daily_ohlc = []
    for minute in range(minutes_count):
        dt = trading_start + datetime.timedelta(minutes=minute)

        minute_ticks = generate_minute_ticks(
            base_value=prev_close_value,
            num_ticks=random.randint(5, 20),
            shift_min=_CONFIG['minute_shift_min'],
            shift_max=_CONFIG['minute_shift_max'],
            surge_probability=_CONFIG['minute_surge_probability'],
            surge_limit=_CONFIG['minute_surge_limit']
        )

        ohlc = get_ohlc_from_ticks(minute_ticks)
        ohlc['dt'] = dt
        daily_ohlc.append(ohlc)
        prev_close_value = ohlc['close']
    return DataFrame(daily_ohlc, index=[ohlc['dt'] for ohlc in daily_ohlc])


def generate_tick(base_value, shift_min, shift_max, surge_probability, surge_limit):
    """Generates a random tick value based on a base value and a range."""
    shift = random.uniform(shift_min, shift_max)
    sign = random.choice([-1, 1])
    base_value += sign * shift * base_value
    return apply_surge(base_value, surge_probability, surge_limit)


def generate_minute_ticks(base_value, num_ticks=None, shift_min=-0, shift_max=0.01, surge_probability=0, surge_limit=0.5):
    """Generates a list of random tick values based on a base value."""
    if num_ticks is None:
        num_ticks = random.randint(_CONFIG.get('ticks_per_minute_min', 0), _CONFIG.get('ticks_per_minute_max', 5))
    ticks = []
    for _ in range(num_ticks):
        ticks.append(generate_tick(base_value, shift_min, shift_max, surge_probability, surge_limit))
        base_value = ticks[-1]
    return ticks


def generate_volume():
    """Generates a random volume value based on the configuration."""
    return random.randint(_CONFIG.get('volume_min', 1), _CONFIG.get('volume_max', 1000))


def get_ohlc_from_ticks(ticks):
    """Calculates OHLC values from a list of ticks."""
    if not ticks:
        return None
    round_precision = _CONFIG.get('round_precision', 0)
    ohlc =  {
        'open': round(ticks[0], round_precision),
        'high': round(max(ticks), round_precision),
        'low': round(min(ticks), round_precision),
        'close': round(ticks[-1], round_precision),
        'volume': generate_volume() if ticks else 0
    }
    ohlc['typical_price'] = round((ohlc['high'] + ohlc['low'] + ohlc['close']) / 3, round_precision)
    return ohlc


def save_ohlc_data_to_file(ohlc_data, filename):
    """Saves OHLC data to a csv file."""
    ohlc_data.to_csv(filename, index=False)
    print(f"OHLC data saved to {filename}")
