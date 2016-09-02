import time
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay
import signal


def calc_date_str(date_str, date_str_format, bdays):
    date_obj0 = datetime.strptime(date_str, date_str_format)
    date_obj0 = date_obj0 - BDay(bdays)
    return date_obj0.strftime(date_str_format)

# print(calc_date_str('2016-08-14', '%Y-%m-%d', -1))
