#前一天收盘价等于最高价时，第二天涨幅分布

import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
# 导入tushare
import tushare as ts
# 初始化pro接口
import pandas as pd
from kittytools.dl_all_data import dl_all_data
from kittytools.mysql import *
import time

from kittytools.dl_all_data import dl_all_data
from kittytools.mysql import read_data
from r2 import r2

def r1(df):
    l = len(df)
    for i in range(l-1):
        #if df['close'][i]/df['high'][i] == 1:
        #    #print(df['trade_date'][i])
        #    #print(df['high'][i+1]/df['close'][i])
        #    o_list.append([df['ts_code'][i], df['trade_date'][i],df['high'][i+1]/df['close'][i], df['low'][i+1]/df['close'][i]])
        o_list.append([df['ts_code'][i], df['trade_date'][i],df['high'][i+1]/df['close'][i], df['low'][i+1]/df['close'][i]])


pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

o_list = []
#查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', market='主板', fields='ts_code,symbol,name,area,industry,list_date')
i = 100
for name in data['ts_code']:
    name = rename(name)
    print(name)
    df = read_data(name)
    #r1(df)
    r2(df, 10, o_list)
    i=i-1
    if i ==0:
        break

da = pd.DataFrame(o_list,columns=['ts_code', 'trade_date', 'increase', 'decrease'])
#print(da)
len_all = len(da)
len_1 = len(da[da['increase']>1.0])
len_2 = len(da[da['increase']>1.005])
len_3 = len(da[da['increase']>1.01])
len_4 = len(da[da['increase']>1.02])
len_5 = len(da[da['increase']>1.05])

len_6 = len(da[da['decrease']>0.9])
len_7 = len(da[da['decrease']>0.95])
len_8 = len(da[da['decrease']>0.98])
len_9 = len(da[da['decrease']>0.99])
len_a = len(da[da['decrease']>0.995])
#print('len_all : ' , len_all, '>1 :', len_a/len_all, '>1.005 :' , len_b/len_all, '>1.01 :' , len_c/len_all, '>1.02 :' , len_d/len_all, '>1.05 :' , len_e/len_all)
print('len_all : ' , len_all)
print('>1.000 :' , len_1/len_all)
print('>1.005 :' , len_2/len_all)
print('>1.010 :' , len_3/len_all)
print('>1.020 :' , len_4/len_all)
print('>1.050 :' , len_5/len_all)

print('>0.900 :' , len_6/len_all)
print('>0.950 :' , len_7/len_all)
print('>0.980 :' , len_8/len_all)
print('>0.990 :' , len_9/len_all)
print('>0.995 :' , len_a/len_all)