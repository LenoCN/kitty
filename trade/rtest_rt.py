from sqlite3 import DateFromTicks
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
import pyarrow.parquet as pp
import pandas as pd
import numpy as np
import tushare as ts
import time
import schedule
from kittytools.get_stock_basic import get_stock_basic
from kittytools.send_mail import send_mail
from kittytools.mult_thread import mult_thread
from kittytools.pytdx_lib import add_today_data, get_all_latest_hq,get_today_data
from research.r2 import trend_line_cal
from research.r4 import boll_cal


def rtest_rt(df_today, df, ts_code, today_date):

    fh=open('rt.log','w')
    #print(ts_code)

    if len(df[df['trade_date']==today_date]) == 0:
        df = pd.concat([df,df_today])
    #print(df)

    if(len(df) < 60):
        return [ts_code, 'N']
    #else:
    #    print('ERROR : Exist this trade_date: %s' % today_date)

    # 计算趋势阻挡位
    time_period = 20
    # 历史数据为i之前time_period-1个最高价
    history = df['high'][-1*time_period-1:-1].to_list()
    trend_line_l = trend_line_cal(history=history,trade_date=today_date,fh=fh)
    if trend_line_l == []:
        return [ts_code, 'N']
    trend_line_l = sorted(trend_line_l, key=lambda x: x[7],reverse=False)
    th = trend_line_l[0][7]


    # 计算当日布林线
    time_period = 20
    history = df['high'][-1*time_period:].to_list()
    lower_band,upper_band =  boll_cal(history=history)

    # 计算均线
    time_period_a, time_period_b, time_period_c = 5,10,60
    history_a = df['close'][-1 * time_period_a : ].to_list()
    history_b = df['close'][-1 * time_period_b : ].to_list()
    history_c = df['close'][-1 * time_period_c : ].to_list()
    # SMA:简单移动平均(Simple Moving Average)
    sma_a = sum(history_a)/len(history_a)
    sma_b = sum(history_b)/len(history_b)
    sma_c = sum(history_c)/len(history_c)

    con_1 = df.iloc[-1]['close'] > th # 突破短期下行趋势线
    con_2 = df.iloc[-1]['high'] < upper_band # 最高价小于布林线上轨
    con_3 = df.iloc[-1]['amount'] > 5 * 100000 # 成交额大于2亿
    con_4 = df.iloc[-1]['close'] / df.iloc[-2]['close'] < 1.095# 不涨停
    con_5 = sma_a >= sma_c # 5日线在60日线上方
    #con_5 = True
    con_6 = df.iloc[-1]['close'] > df.iloc[-2]['high'] # 收盘价高于昨日最高价
    

    #if ts_code == '002685.SZ':
    #    print(con_1, con_2, con_3, con_4, con_5, con_6)
    
    if con_1 and con_2 and con_3 and con_4 and con_5 and con_6:
        return [ts_code, 'Y']
    else:
        return [ts_code, 'N']
        
def job(hq_dict, today_date):
    

    # 获取当日最新行情
    df_all_hq = get_all_latest_hq(today_date)

    # 按照股票代码，获取历史行情数据，以及当日最新行情数据, 分析符合要求的标的
    o_list = []
    threads = []
    for ts_code in hq_dict.keys():
        df = hq_dict[ts_code]
        df_today = df_all_hq[df_all_hq['ts_code']==ts_code]
        threads.append(mult_thread(rtest_rt,(df_today, df, ts_code, today_date)))
        threads[-1].start()
    for thread in threads:
        thread.join()
        o_list.append(thread.get_result())

    df_stock_basic = get_stock_basic()
    # 收集选股结果
    df = pd.DataFrame(o_list, columns=['ts_code', 'status'])
    df = df[df['status'] == 'Y']
    res_l = []
    for i in range(len(df)):
        df_tmp = df_stock_basic[df_stock_basic['ts_code'] == df.iloc[i]['ts_code']]
        res_l.append(df_tmp)
    df_res = pd.concat(res_l)
    df_res = df_res.reset_index(drop=True)
    df_res = df_res.sort_values(by='industry', ascending=False)
    df_res.to_csv('rtest_rt.lg')
    stock_str = ''
    for s in df_res.values:
        stock_str = stock_str + str(s) + '\n'
    #print(stock_str)
    #send_mail(stock_str)




if __name__ == '__main__':
    #print(rtest_rt(ts_code='002246.SZ',today_date='20221017'))
    
    # 设置回测区间
    start_date = '20220800'
    today_date = '20221205'

    # 获取回测区间内的历史数据，并按ts_code分别存入dict
    df_all_h = pp.read_table('df_parquet.parquet').to_pandas()
    df_all_h = df_all_h[df_all_h['trade_date'] >= start_date]

    df_all_h_g = df_all_h.groupby('ts_code')
    hq_dict = {}

    a = time.time()
    # 将所有今天之前的行情数据读入hq_dict中
    hq_dict = {}
    num = 10
    for ts_code,df_h in df_all_h_g:
        #if '600938' not in ts_code:
        #    continue
        print(ts_code)
        df_h = df_h.reset_index(drop=True)
        hq_dict[ts_code] = df_h
        num = num - 1
        #if num == 0:
        #    break
    b = time.time()


    job(hq_dict, today_date)
    c = time.time()
    print(b-a, c-b)
    sys.exit()

    
    # 定时执行job 
    #schedule.every(10).seconds.do(job, hq_dict, today_date)
    schedule.every().day.at("09:45").do(job, hq_dict, today_date)
    schedule.every().day.at("10:00").do(job, hq_dict, today_date)
    schedule.every().day.at("10:30").do(job, hq_dict, today_date)
    schedule.every().day.at("11:00").do(job, hq_dict, today_date)
    schedule.every().day.at("11:15").do(job, hq_dict, today_date)
    schedule.every().day.at("13:50").do(job, hq_dict, today_date)
    schedule.every().day.at("14:20").do(job, hq_dict, today_date)
    schedule.every().day.at("14:40").do(job, hq_dict, today_date)
    schedule.every().day.at("14:53").do(job, hq_dict, today_date)
    while True:
        schedule.run_pending()
        time.sleep(1)