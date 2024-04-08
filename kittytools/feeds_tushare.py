import datetime
import pandas as pd
import backtrader as bt

class PandasData_Extend(bt.feeds.PandasData):

    lines = ('k','d','j','kdj_jc','kdj_dbl','dif','dea','macd','macd_sc',)
    params = (
        ('k', -1),
        ('d', -1),
        ('j', -1),
        ('kdj_jc', -1),
        ('kdj_dbl', -1),
        ('dif', -1),
        ('dea', -1),
        ('macd', -1),
        ('macd_sc', -1)
    )
    datafields = [
        'k',
        'd',
        'j',
        'kdj_jc',
        'kdj_dbl',
        'dif',
        'dea',
        'macd',
        'macd_sc'
    ]

def feeds_tushare(df, start_date, end_date):
    #Sort acording to trade_date
    df = df.sort_values(by='trade_date', ascending=True)
    #Convert trade_date from string to 
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    data = PandasData_Extend(
        name='leno', 
        dataname=df, 
        fromdate=datetime.datetime(start_date[0], start_date[1], start_date[2]), 
        todate=datetime.datetime(end_date[0], end_date[1], end_date[2]),
        datetime='trade_date',  # 日期行所在列
        open='open',  # 开盘价所在列
        high='high',  # 最高价所在列
        low='low',  # 最低价所在列
        close='close',  # 收盘价价所在列
        volume='vol',  # 成交量所在列
        k='k',
        d='d',
        j='j',
        kdj_jc='kdj_jc',
        kdj_dbl='kdj_dbl',
        dif='dif',
        dea='dea',
        macd='macd',
        macd_sc='macd_sc'
        )
    return data