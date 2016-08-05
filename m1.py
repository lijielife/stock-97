import tushare as ts
from datetime import date
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay


def get_h_data(code, days):
    end = date.today()
    end_str = date.today().strftime("%Y-%m-%d")
    start = end - BDay(days)
    start_str = start.strftime("%Y-%m-%d")
    result_df = ts.get_h_data(code, start_str, end_str)
    return result_df


df = get_h_data('600820', 4)

print(df)
