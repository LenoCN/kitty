# 收盘价小于日线布林下轨对次日涨幅的影响

import numpy as np
import tushare as ts
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")

from kittytools.mysql import *
from research.r_lib import *

def r6(df, time_period):

    id_list = []
    # SMA:简单移动平均(Simple Moving Average)
    df = df.sort_values(by='trade_date', ascending=True)
    history = []  # 每个计算周期所需的价格数据
    fh = open('r6.log','a')

    # 计算数据总长度
    l = len(df)
    if(time_period>=l):
        print('Error: 输入数据的数量过少.')
        return id_list
    # 依次遍历自第time_period之后每一个数据
    for i in range(time_period, l):
        # history为今日time_period日均线的计算窗口
        history = df['close'][i-time_period+1:i+1].to_list()
        #print(history)

        # SMA:简单移动平均(Simple Moving Average)
        sma = np.mean(history)
        #print(sma)

        # 计算布林上轨下轨
        stdev = np.sqrt(np.sum((history - sma) ** 2) / len(history))  
        upper_band = sma + 2 * stdev
        lower_band = sma - 2 * stdev

        # 判断今日收盘价是否小于布林下轨
        if df['close'][i] < lower_band:
            #print(df['trade_date'][i], upper_band)

            # 返回所有符合条件的日期在df中的序号i
            fh.write(df['trade_date'][i] + '\n')
            #print(df['trade_date'][i])
            id_list.append(i)
    fh.close()
    return id_list

if __name__ == '__main__':

    #查询当前所有正常上市交易的股票列表
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    data = pro.stock_basic(exchange='', list_status='L',  fields='ts_code,symbol,name,area,industry,list_date, market')
    data = data[data['name'].str.find('ST') == -1]
    data = data[data['market'].str.find('北交所') == -1]

    num = 1
    time_period = 20
    o_list = []
    for name in data['ts_code']:
        name = rename(name)
        print(name)
        try:
            df = read_data(name)
        except:
            continue
        id_list = r6(df, time_period=time_period)
        for i in id_list:
            try:
                next_close = df['close'][i+1]
                next_high  = df['high'][i+1]
                next_low   = df['low'][i+1]
            except:
                continue
            o_list.append([df['ts_code'][i], df['trade_date'][i],next_high/df['close'][i], next_low/df['close'][i]])
        num=num-1
        if num ==0:
            break

    da = inc_dist(o_list=o_list)

    da = da.loc[da['trade_date']>'20220901']
    da.to_csv('tmp1003r6')
