import tushare as ts
import pandas as pd
import data


my_code = '600115'
my_end_str = '2016-08-29'
my_days = 4


# get initial data: history tick & history data
df0 = data.get_hist_tick_stats_data(my_code, my_end_str, my_days)
df1 = data.get_hist_data(my_code, my_end_str, my_days)
# print(df0)
# print(df0.index)
# print(df1)
# print(df1.index)
# get first result: history tick * history data
result0 = pd.concat([df0, df1], axis=1, join='inner')
result0.loc[:, 'volume_diff_per'] = result0.loc[:, 'volume_diff'] / result0.loc[:, 'volume'] * 100
result0.loc[:, 'price_avg_diff_per'] = result0.loc[:, 'price_avg_diff'] / result0.loc[:, 'close'] * 100
print(result0)
# filter data: price_avg_diff_per<0 & volume_diff_per>0
result1 = result0[(result0.price_avg_diff_per < 0) & (result0.volume_diff_per > 0)]
print(result1)
# test realtime tick
print(data.get_today_tick_stats_data(my_code))
