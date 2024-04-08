# time_period周期日线向上对次日涨幅的影响

import numpy as np
import tushare as ts
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")

from kittytools.mysql import *
from research.r_lib import *

def r3(df, time_period, slope):

    id_list = []
    # SMA:简单移动平均(Simple Moving Average)
    df = df.sort_values(by='trade_date', ascending=True)
    history = []  # 每个计算周期所需的价格数据
    fh = open('r3.log','a')
    sma_values_q = []  # 初始化SMA值

    # 计算数据总长度
    l = len(df)
    if(l<=time_period+5):
        print('Error: 输入数据的数量过少.')
        return id_list
    # 依次遍历自第time_period之后每一个数据
    for i in range(time_period+4, l):
        # history_a为昨日20日均线的计算窗口，history_b为今日20日均线的计算窗口
        history_y = df['close'][i-time_period-4:i-4].to_list()
        history_t = df['close'][i-time_period+1:i+1].to_list()
        #print(history_y)
        #print(history_t)

        # SMA:简单移动平均(Simple Moving Average)
        sma_y = np.mean(history_y)
        sma_t = np.mean(history_t)
        #print(sma_y)
        #print(sma_t)

        # 判断今日20均线是否大于昨日20日均线
        #o_list.append([df['ts_code'][i-1], df['trade_date'][i-1],df['high'][i]/df['close'][i-1], df['low'][i]/df['close'][i-1]])
        if sma_t / sma_y > slope:
            #print(df['trade_date'][i-1],sma_t, sma_y)
            #o_list.append([df['ts_code'][i-1], df['trade_date'][i-1],df['high'][i]/df['close'][i-1], df['low'][i]/df['close'][i-1]])

            # 返回所有符合条件的日期在df中的序号i
            fh.write(df['trade_date'][i] + '\n')
            #print(df['trade_date'][i])
            id_list.append(i)
    fh.close()
    return id_list

if __name__ == '__main__':
    df = read_data('000002dotsz')
    #df = df.loc[df['trade_date'] > '20220906']
    #df = df.reset_index(drop=True)
    #r2(df=df, time_period=time_period, o_list=o_list)

    #查询当前所有正常上市交易的股票列表
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    data = pro.stock_basic(exchange='', list_status='L',  fields='ts_code,symbol,name,area,industry,list_date, market')
    data = data[data['name'].str.find('ST') == -1]
    data = data[data['market'].str.find('北交所') == -1]

    num = 1
    time_period = 20
    slope = 0.01
    o_list = []
    for name in data['ts_code']:
        name = rename(name)
        print(name)
        try:
            df = read_data(name)
        except:
            continue
        id_list = r3(df, time_period=time_period, slope=slope)
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

    inc_dist(o_list=o_list)
    #da = da.loc[da['trade_date']>'20220920']
    #da.to_csv('tmp1003r3')
