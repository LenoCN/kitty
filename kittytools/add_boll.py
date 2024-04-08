import pandas as pd
import numpy as np
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
import matplotlib.pyplot as plt
from kittytools.get_ths_daily import get_ths_daily

def add_boll(df):

    # SMA:简单移动平均(Simple Moving Average)
    df = df.sort_values(by='trade_date', ascending=True)
    time_period = 20  # SMA的计算周期，默认为20
    stdev_factor = 2  # 上下频带的标准偏差比例因子
    history = []  # 每个计算周期所需的价格数据
    sma_values = []  # 初始化SMA值
    upper_band = []  # 初始化阻力线价格
    lower_band = []  # 初始化支撑线价格
    value_rate = []  # 初始化支撑线价格

    # 构造列表形式的绘图数据
    for close_price in df['close']:
        # 
        history.append(close_price)

        # 计算移动平均时先确保时间周期不大于20
        if len(history) > time_period:
            del (history[0])

        # 将计算的SMA值存入列表
        sma = np.mean(history)
        sma_values.append(sma)  
        # 计算标准差
        stdev = np.sqrt(np.sum((history - sma) ** 2) / len(history))  
        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)
        if stdev == 0:
            value_rate.append(0)
        else:
            value_rate.append( 2* ( (close_price - (sma - stdev_factor * stdev))/(2 * stdev_factor * stdev) - 0.5))

    # 将计算的数据合并到DataFrame
    #df = df.assign(sma20=pd.Series(sma_values, index=df.index))
    #df = df.assign(top=pd.Series(upper_band, index=df.index))
    #df = df.assign(bot=pd.Series(lower_band, index=df.index))
    #df = df.assign(rate=pd.Series(value_rate, index=df.index))
    #df = df.assign(sma20=sma_values)
    df = df.assign(top=upper_band)
    df = df.assign(bot=lower_band)
    df = df.assign(rate=value_rate)

    return df

    ## 绘图
    #ax = plt.figure()
    ## 设定y轴标签
    #ax.ylabel = '%s price in ￥' % (ts_code)
    #
    #df['close'].plot(color='k', lw=1., legend=True)
    #df['sma20'].plot(color='b', lw=1., legend=True)
    #df['top'].plot(color='r', lw=1., legend=True)
    #df['bot'].plot(color='g', lw=1., legend=True)
    #df['rate'].plot(color='b', lw=1., legend=True)
    #
    ##print(df['rate'][0])
    #plt.gca().invert_xaxis()
    #plt.show()

def add_sma(df):

    # SMA:简单移动平均(Simple Moving Average)
    df = df.sort_values(by='trade_date', ascending=True)
    history = []  # 每个计算周期所需的价格数据
    sma_values_q = []  # 初始化SMA值
    time_period = [5,20,60]

    # 构造列表形式的绘图数据
    for i,tp in enumerate(time_period):
        sma_values = []  # 初始化
        for close_price in df['close']:
            history.append(close_price)
            if len(history) > tp:
                del (history[0])
            sma = np.mean(history)
            sma_values.append(sma)  
        sma_values_q.append(sma_values)

    df = df.assign(sma5=sma_values_q[0])
    df = df.assign(sma20=sma_values_q[1])
    df = df.assign(sma60=sma_values_q[2])

    return df

    ## 绘图
    #ax = plt.figure()
    ## 设定y轴标签
    #ax.ylabel = '%s price in ￥' % (ts_code)
    #
    #df['close'].plot(color='k', lw=1., legend=True)
    #df['sma20'].plot(color='b', lw=1., legend=True)
    #df['top'].plot(color='r', lw=1., legend=True)
    #df['bot'].plot(color='g', lw=1., legend=True)
    #df['rate'].plot(color='b', lw=1., legend=True)
    #
    ##print(df['rate'][0])
    #plt.gca().invert_xaxis()
    #plt.show()

if __name__ == '__main__':
    start_date = [2016, 6, 2]
    end_date = [2022, 6 , 7]
    #ts_code = '885922.TI' #盐湖提锂
    ts_code = '884014.TI' #煤炭开采

    df = get_ths_daily(ts_code, start_date, end_date)
    #df = df.sort_values(by='trade_date', ascending=True)
    df_out = add_boll(df)
    print(df_out)