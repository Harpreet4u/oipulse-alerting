from enum import Enum

import math
from datetime import datetime, timedelta


class DataType(Enum):
    TRENDING_OI = "TRENDING_OI"
    FUTURES_OI = "FUTURES_OI"


def get_timestamp(d_date):
    epoch = datetime(1970, 1, 1)
    return int((datetime.combine(d_date, datetime.min.time()) - epoch).total_seconds())


def next_weekday(dt, weekday):
    if dt.weekday() == 3:
        return dt
    days_ahead = weekday - dt.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return dt + timedelta(days_ahead)


def round_value(value, round_to=100):
    try:
        return int(math.ceil(value / round_to) * round_to)
    except ValueError:
        return 0
