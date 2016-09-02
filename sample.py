import tushare as ts
import pandas as pd
import data

# import matplotlib.pyplot as plt

my_code = '600848'
my_date = '2016-08-04'
my_days = 30


# # 获取历史分笔
# df = ts.get_tick_data(myCode, date=myDate)
# sLength = len(df.index)
# # print(sLength)
# # print(df.shape)
# # print(df.head(10))
#
# # 创建Series, 内容是date, 大小是df的size
# dateSeries = pd.Series([myDate] * sLength, name="date")
# # print(dateSeries.size)
# # print(len(dateSeries))
# # print(dateSeries)
#
# # join dataframe(这里是join, 不是concat)
# df["date"] = pd.Series([myDate] * sLength, name="date")
# # df1 = pd.concat([dateSeries, df], axis=1)
# # print(len(df.index))
# # print(df.tail(10))
#
# # group dataframe
# dfTypeSummary = df.groupby(['date', 'type']).sum()
# # 这句话用于比较成交量, 确认成交量是双向还是单向
# # print(ts.get_hist_data('600848', start='2016-08-08', end='2016-08-09'))
# # print(dfTypeSummary)
#
# # calculate series
# dfTypeSummary['price_avg'] = (dfTypeSummary['amount'] / dfTypeSummary['volume']) / 100
# dfTypeSummary.price_avg = dfTypeSummary.price_avg.round(2)
# # print(dfTypeSummary)
#
# # delete redundant column
# del dfTypeSummary['price']
# # print(dfTypeSummary.dtypes)
#
# # calculate certain rows
# # print(dfTypeSummary.index)
# # print(dfTypeSummary['date'])
# dfTypeSummary_1 = dfTypeSummary.ix[[(myDate, '买盘'), (myDate, '卖盘')]]
# dfTypeSummary_2 = dfTypeSummary_1.xs(myDate, level='date')
# dfTypeSummary_2.loc['Diff'] = dfTypeSummary_2.loc['买盘'] - dfTypeSummary_2.loc['卖盘']
# dfTypeSummary_3 = dfTypeSummary_2.loc['Diff':]
# print(myDate)
# print(dfTypeSummary_3)


# 获取全部股票code
df = ts.get_stock_basics()
print(df.index)
for code in df.index:
    print(code)

