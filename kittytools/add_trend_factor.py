import pandas as pd
import numpy as np
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.add_boll import add_sma
import matplotlib.pyplot as plt
from kittytools.get_ths_daily import get_ths_daily
from kittytools.get_fund_daily import get_fund_daily
from kittytools.get_daily import get_daily

def add_trend_factor(df, time_period=20,  trend_top=1, plot_en = False):

    history = [] 
    trend_factor_values = [] 
    # 构造列表形式的绘图数据
    for i in range(len(df)):
        if(i>time_period):
            #print(df.iloc[-1 + -1*i].sma20)
            #print(df.iloc[-1*time_period + -1*i].sma20)
            trend_factor = df.iloc[i].sma20 / df.iloc[i - time_period].sma20
            trend_factor_values.append(trend_factor * trend_top)
        else:
            trend_factor_values.append(0)

    # 将计算的数据合并到DataFrame
    df = df.assign(trendfactor=trend_factor_values)

    if plot_en == True:
        # 绘图
        ax = plt.figure()
        # 设定y轴标签
        #ax.ylabel = '%s price in ￥' % (ts_code)
    
        df['close'].plot(color='k', lw=1., legend=True)
        df['sma20'].plot(color='b', lw=1., legend=True)
        df['trendfactor'].plot(color='b', lw=1., legend=True)
    
        #print(df['rate'][0])
        plt.gca().invert_xaxis()
        plt.show()

    return df


if __name__ == '__main__':
    start_date = ''
    end_date = ''
    #ts_code = '885922.TI' #盐湖提锂
    #ts_code = '884014.TI' #煤炭开采
    ts_code = '561120.SH' #家电ETF

    df = get_fund_daily(ts_code, start_date, end_date)
    #df = get_ths_daily(ts_code, start_date, end_date)
    #df = get_daily(ts_code, start_date, end_date)
    #df = df.sort_values(by='trade_date', ascending=False)
    df = add_sma(df)
    df = add_trend_factor(df, time_period=40, trend_top=1, plot_en=False)
    print(df)
    print(df.iloc[-1].trendfactor)