import tushare as ts
import pandas as pd
import data

my_end_str = '2016-08-30'
my_days = 0
output_file = 'run2_result.csv'

# 获取全部股票code
df_codes = ts.get_stock_basics()
total_count = len(df_codes.index)
current_count = 0

# f = open('run2_result', 'w')
for my_code in df_codes.index:
    current_count += 1
    print('run %d/%d' % (current_count, total_count))
    try:
        # get initial data: history tick & history data
        df0 = data.get_hist_tick_stats_data(my_code, my_end_str, my_days)
        df1 = data.get_hist_data(my_code, my_end_str, my_days)
        # get first result: history tick * history data
        result0 = pd.concat([df0, df1], axis=1, join='inner')
        result0.loc[:, 'volume_diff_per'] = result0.loc[:, 'volume_diff'] / result0.loc[:, 'volume'] * 100
        result0.loc[:, 'price_avg_diff_per'] = result0.loc[:, 'price_avg_diff'] / result0.loc[:, 'close'] * 100
        # filter data:  volume_diff_per>0 & price_avg_diff_per<0  & price_change<0
        # 买入盘多,买入均价小,收盘价格跌
        result1 = result0[(result0.price_avg_diff_per < 0) & (result0.volume_diff_per > 0) & (result0.price_change < 0)]
        result1.loc[:, 'code'] = my_code
        if len(result1.index) > 0:
            print(result1)
            with open(output_file, 'a') as f:
                if current_count == 1:
                    result1.to_csv(f, sep='\t', encoding='utf-8', header=True)
                else:
                    result1.to_csv(f, sep='\t', encoding='utf-8', header=False)
                    # f.write(result1)
                    # f.write('\n')
        else:
            print('no result data')
    except (IOError, ValueError, KeyError, TypeError, data.FetchDFTimeoutError):
        continue
# f.close()

