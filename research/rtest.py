from collections import abc
import itertools
from multiprocessing.dummy import Pool
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
import time
import pyarrow.parquet as pp
import pyarrow as pa
from kittytools.pytdx_lib import add_today_data
from kittytools.mysql import *
from kittytools.mult_thread import mult_thread
from research.r_lib import *
from research.r2 import r2, trend_line_cal
from research.r3 import r3
from research.r4 import r4
from research.r5 import r5
from research.r6 import r6
from research.r7 import r7
import multiprocessing as mp
import numpy as np
import cProfile
from line_profiler import LineProfiler

def analysis_single(df, q, a,b,c):
    id_list = []
    id_list_1 = []
    id_list_2 = []
    id_list_3 = []
    id_list_4 = []
    id_list_5 = []

    id_list_2 = r2(df, time_period=a, next_th_coef=b, rs_range_l=c[0], rs_range_r=c[1]) # 突破短期下行趋势线
    #id_list_4 = r4(df, time_period=20) # 最高价小于布林线上轨
    #id_list_5 = r5(df, 8)                 # 成交额大于1亿
    #                                   # 不涨停
    #id_list_7 = r7(df, time_period_a=10, time_period_b=20, time_period_c=30) # 均线多头排列 a>b>c
    #id_list_3 = r3(df, time_period=20, slope=1)# 20日日线向上
    #id_list_3 = list(set(r3(df, time_period=120, slope=1)) & set(r3(df, time_period=60, slope=1))) # 120日与60日日线向上
    #id_list_6 = r6(df, time_period=20) # 收盘价小于布林线下轨

    id_list = id_list_2
    #id_list = list(set(id_list_4)  & set(id_list_5))
    #id_list = list(set(id_list_2) & set(id_list_4) & set(id_list_5) & set(id_list_7))
    
    #print(id_list_2, id_list_4,id_list_5, id_list)

    win = True
    o_list = []
    for i in id_list:
        try:
            next_close = df['close'][i+1]
            next_high = 0
            for j in range(1,4):
                if df['high'][i+j] > next_high:
                    next_high = df['high'][i+j]
            next_low   = df['low'][i+1]
        except:
            o_list.append([df['ts_code'][i], df['trade_date'][i],0,0, win])
            continue
        else:
            o_list.append([df['ts_code'][i], df['trade_date'][i],next_high/df['close'][i], next_low/df['close'][i], win])
    #    if sell_price_l == []:
    #        win = 'Other'
    #    else:
    #        win = sell_price_l[0]<next_high
    #print(o_list)
    q.put(o_list)

def rtest(a,b,c):
    tz = time.time()
    q = mp.Manager().Queue()
    p = mp.Pool(4)

    # 设置回测区间
    start_date = '20220700'
    end_date = '99999999'

    # 获取回测区间内的历史数据，并按ts_code分别存入dict
    df_all_h = pp.read_table('df_parquet.parquet').to_pandas()

    df_all_h = df_all_h[df_all_h['trade_date'] >= start_date]
    df_all_h = df_all_h[df_all_h['trade_date'] <= end_date]

    df_all_h_g = df_all_h.groupby('ts_code')
    hq_dict = {}

    ta = time.time()
    # 将所有今天之前的行情数据读入hq_dict中
    num = 9999
    for ts_code,df_h in df_all_h_g:
        #print(ts_code)
        df_h = df_h.reset_index(drop=True)
        df_h = df_h.sort_values(by='trade_date', ascending=True)
        hq_dict[ts_code] = df_h
        num = num - 1
        if num == 0:
            break
    tb = time.time()

    # 采用多进程分别对每个ts_code对应的历史行情进行分析, 并收集符合选股策略的标的
    o_list = []
    for ts_code,df_h in hq_dict.items():
        p.apply_async(analysis_single,(df_h,q,a,b,c))
    p.close()
    p.join()
    for i in range(q.qsize()):
        o_list.extend(q.get())

    da = pd.DataFrame(o_list,columns=['ts_code', 'trade_date', 'increase', 'decrease', 'win'])
    da = da.sort_values(by='trade_date', ascending=True)
    res = inc_dist(da)
    #write_data(da, 'test1011')
    #da = da.loc[da['increase'] < 1.02]
    da.to_csv('rtest.lg')
    tc = time.time()
    #print(ta-tz, tb-ta, tc-tb)
    return res

if __name__ == '__main__':
    #res = rtest(30,1.8,[-100,-20])

    #sys.exit()

    a_l = list(np.arange(5,40,5))
    b_l = list(np.arange(1,2.1,0.2))
    c_l = [[-1000,-100],[-100,-50],[-50,-20],[-20,2]]
    abc_l = list(itertools.product(a_l, b_l, c_l))
    #print(abc_l, len(abc_l))
    #abc_l = [[5,1,[-1000,-100]]]
    print(abc_l, len(abc_l))
    res_l = []

    ta = time.time()
    for i in abc_l:
        tb = time.time()
        a,b,c = i
        print(a,b,c)
        res = list(rtest(a,b,c))
        c = c_l.index(c)
        res.extend([a,b,c])
        res_l.append(res)
        tc = time.time()
        print((tc-tb)/60)
    td = time.time()
    df_res = pd.DataFrame(res_l,columns=['len_all', 'ic1','ic2','ic3','ic4','ic5','ic6','ic7','a','b','c',])
    print(df_res)
    write_data(df=df_res,name='rtestpa')
    pp.write_table(pa.Table.from_pandas(df_res), 'df_rtest_param_analysis20220700.parquet')
    print((td-ta)/60)






    ''' 性能分析 

    df_all_h = pp.read_table('df_parquet.parquet').to_pandas()
    df_all_h_g = df_all_h.groupby('ts_code')
    df_h = df_all_h_g.get_group('000001.SZ')
    df_h = df_h.reset_index(drop=True)
    
    p = LineProfiler()
    p.add_function(trend_line_cal)
    p_wrap = p(analysis_single)
    p_wrap(df_h)
    p.print_stats()
    p.dump_stats('as.lprof')
    #analysis_single(df_h)
    #cProfile.run('analysis_single(df_h)','test_status')

    '''