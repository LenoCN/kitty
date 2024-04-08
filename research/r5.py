# 成交额大于1亿对次日涨幅的影响
# 不涨停

import numpy as np
import tushare as ts
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")

from kittytools.mysql import *
from research.r_lib import *

def r5(df, val):

    id_list = []
    # SMA:简单移动平均(Simple Moving Average)
    df = df.sort_values(by='trade_date', ascending=True)
    fh = open('r5.log','a')

    # 计算数据总长度
    l = len(df)
    if(l<=1):
        print('Error: 输入数据的数量过少.')
        return id_list
    # 依次遍历自第time_period之后每一个数据
    for i in range(1,l):
        # 判断今日成交额大于1亿
        if df['amount'][i] < val * 100000:
            continue
        # 不涨停
        if df['close'][i]/df['close'][i-1] > 1.095 :
            continue
        # 涨幅大于5%
        #if df['close'][i]/df['close'][i-1] < 1.055 :
        #    continue
        #收盘接近最高价
        #if (df['close'][i]-df['close'][i-1])/(df['high'][i]-df['close'][i-1]) < 0.9:
        #    continue
        # 返回所有符合条件的日期在df中的序号
        #print(df['trade_date'][i])
        fh.write(df['ts_code'][i] + ' ' +df['trade_date'][i] + '\n')
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
    o_list = []
    for name in data['ts_code']:
        name = rename(name)
        print(name)
        try:
            df = read_data(name)
        except:
            continue
        id_list = r5(df)
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
    da.to_csv('tmp1003r5')
