import tushare as ts
import pandas as pd
from datetime import datetime
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
# import matplotlib.pyplot as plt
import util
import signal


timeout_duration = 2


# 获取某一只股票,对于今天近n天历史数据
def get_hist_data_from_today(code, days):
    end = datetime.today()
    # date convert to string
    end_str = datetime.today().strftime("%Y-%m-%d")
    start = end - BDay(days)
    # date convert to string
    start_str = start.strftime("%Y-%m-%d")
    result_df = ts.get_hist_data(code, start_str, end_str)
    return result_df


# 获取某一只股票,对于end_date近n天历史数据,
def get_hist_data(code, end_date_str, days):
    # date convert to string
    start_date_str = util.calc_date_str(end_date_str, '%Y-%m-%d', days)
    # 获取历史数据
    print('loading hist data of %s from %s to %s' % (code, start_date_str, end_date_str))
    begin = datetime.now()
    result_df = ts.get_hist_data(code, start=start_date_str, end=end_date_str)
    end = datetime.now()
    print('finish loading hist date, 耗时: %s' % (end - begin))
    return result_df


# 获取某一只股票,近n天历史数据: %分笔买入%-%分笔卖出%
def get_hist_tick_stats_data(code, end_date, days):
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date - BDay(days)
    delta_day = BDay(1)
    # day = timedelta(days=1)
    df_list = list()
    while start_date <= end_date:
        start_date_str = start_date.strftime('%Y-%m-%d')  # convert date to string
        # 获取历史分笔
        print('loading tick stat data of %s on %s ' % (code, start_date_str))
        begin = datetime.now()
        # Register the signal function handler
        signal.signal(signal.SIGALRM, timeout_handler)
        # Define a timeout for your function
        signal.alarm(timeout_duration)
        try:
            df = ts.get_tick_data(code, date=start_date_str)
        except (IOError, FetchDFTimeoutError):
            print('get_hist_tick_stat_data: Error')
            continue
        finally:
            signal.alarm(0)
        end = datetime.now()
        print('finish loading tick stat date, 耗时: %s' % (end - begin))
        s_length = len(df.index)
        if s_length == 3:
            start_date = start_date + delta_day
            continue
        # 创建Series, 内容是date, 大小是df的size
        # 后面代码产生同样效果,这个先注释
        # dateSeries = pd.Series([myDate_start] * sLength, name="date")
        # join dataframe(这里是join, 不是concat)
        df["date"] = pd.Series([start_date_str] * s_length, name="date")
        # group dataframe
        df_type_summary = df.groupby(['date', 'type']).sum()
        # calculate series
        df_type_summary['price_avg'] = (df_type_summary['amount'] / df_type_summary['volume']) / 100
        df_type_summary.price_avg = df_type_summary.price_avg.round(2)
        # delete redundant column
        del df_type_summary['price']
        # calculate certain rows
        df_type_summary_1 = df_type_summary.ix[[(start_date_str, '买盘'), (start_date_str, '卖盘')]]
        df_type_summary_2 = df_type_summary_1.xs(start_date_str, level='date')
        # before substract series, xs index level='date'
        df_type_summary_2.loc['Diff', :] = df_type_summary_2.loc['买盘', :] - df_type_summary_2.loc['卖盘', :]
        df_type_summary_3 = df_type_summary_2.loc['Diff':, :]
        df_type_summary_3.loc[:, 'date'] = start_date_str
        # print(df_type_summary_3)
        df_list.append(df_type_summary_3)
        start_date = start_date + delta_day
    result = pd.concat(df_list)
    # reindex: change index from Diff to Date
    indexed_result = result.set_index(['date'])
    # redefine: columns key name
    indexed_result.columns = ['volume_diff', 'amount_diff', 'price_avg_diff']
    return indexed_result


# 获取某一只股票实时分笔: %分比买入%-%分比卖出%
def get_today_tick_stats_data(code):
    df = ts.get_today_ticks(code)
    s_length = len(df.index)
    if s_length <= 3:
        return
    # group dataframe
    df_type_summary = df.groupby('type').sum()
    # calculate series
    df_type_summary['price_avg'] = (df_type_summary['amount'] / df_type_summary['volume']) / 100
    df_type_summary.price_avg = df_type_summary.price_avg.round(2)
    # delete redundant column
    del df_type_summary['price']
    # calculate certain rows
    # before substract series, xs index level='date'
    df_type_summary.loc['Diff', :] = df_type_summary.loc['买盘', :] - df_type_summary.loc['卖盘', :]
    df_result = df_type_summary.loc['Diff':, :]
    return df_result


def timeout_handler(signum, frame):
    raise FetchDFTimeoutError("timeout_handler invoked")


class FetchDFTimeoutError(Exception):
    pass

