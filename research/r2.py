# 突破趋势线后对涨幅的影响
import line_profiler
from re import T
import pandas as pd
import sys
import time
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.mysql import read_data
from kittytools.get_ths_daily import get_ths_daily
from kittytools.mysql import *
from research.r_lib import *

def trend_line_cal(history,trade_date, fh):
    trend_line_l = []

    # 计算这段历史数据对应后市的所有潜在阻挡趋势线
    for j,m in enumerate(history):
        for k,n in enumerate(history):
            mse = 0
            var = 0
            if(k<=j):
                continue
            if n > m:
                continue
            history_mean = sum(history)/len(history)
            slope = (n-m)/(k-j)
            for l,o in enumerate(history):
                #if l == j or l == k:
                #    continue
                th = m + (l-j)*slope
                if o > th:
                    break
                mse += (o-th)**2 #* (0.5+0.0025*l)
                var += (o-history_mean)**2
                #if trade_date == '20200903' and j==17 and k==19:
                #    print(mse, var, o,th,history_mean, )
                if l == len(history) - 1:
                    #mse = mse/len(history)
                    #var = var/len(history)
                    rs = 1-mse/var
                    #if trade_date == '20200903':
                    #    print(mse, var, rs, history_mean)
                    trend_line_l.append([trade_date,m,j,n,k,slope, rs,m+(len(history)-j)*slope])
    return trend_line_l


def r2(df, time_period, next_th_coef, rs_range_l, rs_range_r):

    id_list = []
    # SMA:简单移动平均(Simple Moving Average)
    history = []  # 每个计算周期所需的价格数据
    fh = open('r2.log','a')


    # 计算数据总长度
    l = len(df)
    if(l<=time_period):
        #print('Error: 输入数据的数量过少.')
        return id_list
    # 依次遍历自第time_period之后每一个数据
    df_trend_line_all = None
    for i in range(time_period, l):
        close = df['close'][i]
        high = df['high'][i]
        last_high = df['high'][i-1]
        trade_date = df['trade_date'][i]

        if close < last_high:
            continue
        #fh.write(df['ts_code'][i] + df['trade_date'][i] + '\n')
        # 历史数据为i之前time_period-1个最高价
        history = df['high'][i-time_period:i].to_list()
        trend_line_l = trend_line_cal(history=history, trade_date=trade_date,fh=fh)
        # 没有下降阻挡趋势线则跳过
        if trend_line_l == []:
            continue
        
        #df_trend_line = pd.DataFrame(trend_line_l, columns=['trade_date','start_point', 'start_index','end_point', 'end_index', 'slope', 'rs', 'th'])
        #df_trend_line = df_trend_line[df_trend_line['th'] * 1.01 < close]
        #df_trend_line_all = pd.concat([df_trend_line_all,df_trend_line])
        
        # 判断当天收盘价是否突破下行趋势线
        # 没有突破趋势线则跳过
        trend_line_l = sorted(trend_line_l, key=lambda x: x[7],reverse=False)
        th = None
        rs = None
        next_th = None
        for j,trend_line in enumerate(trend_line_l):
            # close / th > 1.01
            if close/trend_line[7] > 1.01:
                th = trend_line[7]
                rs = trend_line[6]
                if j != len(trend_line_l)-1:
                    next_th = trend_line_l[j+1][7]
        #print(trade_date)
        #print(trend_line_l, next_th, close)
        #time.sleep(1)
        if th is None:
            continue
        #if next_th != None and next_th/th < 1.04:
        #    continue
        if rs_range_l is None or rs_range_r is None:
            pass
        elif rs <rs_range_l or rs > rs_range_r:
            continue

        if next_th == None:
            continue
        if next_th/close < next_th_coef :
            continue

        
        #if (df['close'][i]-df['open'][i])/(df['high'][i]-df['open'][i]) < 0.6:
        #    continue
        #if df['close'][i]/df['close'][i-1] < 1.05:
        #    continue
        


        #if trade_date == '20200903':
        #    df_trend_line = pd.DataFrame(trend_line_l, columns=['trade_date','start_point', 'start_index','end_point', 'end_index', 'slope', 'rs', 'th'])
        #    print(df_trend_line, close)
        #    print(history)
        #    print(close)
        #    print(high)
        #    print(i)
        #    sys.exit()


        #sell_price_l = []
        #for line in trend_line_l:
        #    th = line['start_point'] + ( time_period - line['start_index']) * line['slope'] 
        #    if df['close'][i] / th < 1:
        #        sell_price_l.append(line['start_point'] + ( time_period+1 - line['start_index']) * line['slope'])
        #        sell_price_l.append(line['start_point'] + ( time_period+2 - line['start_index']) * line['slope'])
        #        sell_price_l.append(line['start_point'] + ( time_period+3 - line['start_index']) * line['slope'])
        #        break
        #if len(sell_price_l) != 0:
        #    if df['close'][i] > sell_price_l[0]:
        #        continue
        # 返回所有符合条件的日期在df中的序号i
        #print(df['trade_date'][i])


        id_list.append(i)
        #id_list.append([i,rs,next_th])

    #fh.close()
    #return id_list, df_trend_line_all
    fh.close()
    return id_list

if __name__ == '__main__':
    #p = line_profiler.LineProfiler()
    #p.add_function(trend_line_cal)
    #p_wrap = p(r2)
    
    
    name = '600809DOTSH'
    df = read_data(name)
    #df = df.loc[df['trade_date'] > '20140000']
    df = df.reset_index(drop=True)
    id_list,df_trend_line_all = r2(df, time_period=60, next_th_coef=1.2, rs_range_l=None, rs_range_r=None)
    #id_list,df_trend_line_all = r2(df, time_period=60, next_th_coef=1.6, rs_range_l=-100, rs_range_r=-50)

    win = True
    o_list = []
    for i,rs,next_th in id_list:
        try:
            next_close = df['close'][i+1]
            next_high = 0
            for j in range(1,4):
                if df['high'][i+j] > next_high:
                    next_high = df['high'][i+j]
            next_low   = df['low'][i+1]
        except:
            o_list.append([df['ts_code'][i], df['trade_date'][i],0, rs, next_th, 0, win])
            continue
        else:
            o_list.append([df['ts_code'][i], df['trade_date'][i],next_high/df['close'][i], rs, next_th, next_low/df['close'][i], win])


    da = pd.DataFrame(o_list,columns=['ts_code', 'trade_date', 'increase', 'rs', 'next_th', 'decrease', 'win'])
    #da = da.sort_values(by='rs', ascending=False)
    #da = da.sort_values(by='trade_date', ascending=False)
    da = da.sort_values(by='increase', ascending=True)
    #da = da.loc[da['increase'] < 1.03]
    da = da.reset_index(drop=True)
    da.to_csv('tmp1023')
    da1 = da[da['rs'] >-20]
    da2 = da[da['rs'] <-20]
    da2 = da2[da2['rs'] >-50]
    da3 = da[da['rs'] >-100]
    da3 = da3[da3['rs'] <-50]
    da4 = da[da['rs'] <-100]
    #print(da['increase'].mean())
    inc_dist(da)
    #inc_dist(da1)
    #inc_dist(da2)
    #inc_dist(da3)
    #inc_dist(da4)
    #with pd.option_context('display.max_rows', None): 
    #    print(da)


    #with pd.option_context('display.max_rows', None): 
    #    print(da2)
    #df_trend_line_all = df_trend_line_all.sort_values(by='rs', ascending=False)
    #df_trend_line_all = df_trend_line_all.reset_index(drop=True)
    #with pd.option_context('display.max_rows', None): 
    #    print(df_trend_line_all)
    #    print(len(df_trend_line_all))
    #p.print_stats()
    #p.dump_stats('as.lprof')