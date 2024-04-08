# 导入tushare
from concurrent.futures import thread
from ctypes import resize
import tushare as ts
# 初始化pro接口
import pandas as pd
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")

from kittytools.mult_thread import mult_thread
from kittytools.get_daily import get_daily
from kittytools.mysql import rename, write_data,read_data 

def func(df_add_all, ts_code, start_date):
    # 从全部新增行情信息中筛选ts_code对应的行情信息
    df_add = df_add_all.loc[df_add_all['ts_code']==ts_code]
    print(ts_code)

    # 获取ts_code对应的历史行情信息
    name = rename(ts_code)
    try:
        df_orig = read_data(name.lower())
    except:
        print('WARN : data not exist, ts_code: %s . ' % ts_code)
        write_data(df_add, name.lower())
        return
    # 如果日期重叠 报错并返回
    dt = df_orig[df_orig['trade_date'] >= start_date]
    if len(dt) != 0:
        print('ERROR : 已包含区间[start_date,end_date]内的数据, ts_code: %s .' % ts_code)
        return 
    # 拼接后写回数据库
    df_new = pd.concat([df_orig,df_add])
    df_new = df_new.reset_index(drop=True)
    write_data(df_new, name.lower())

def update_data(start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

    # 获取期间所有交易日期
    df = pro.trade_cal(exchange='SSE', is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
    cal_date_l = df['cal_date'].tolist()

    # 获取期间所有股票的日线行情信息
    df_add_all=None
    for i in cal_date_l:
        print(i)
        df_tmp = get_daily('',i,i)
        df_add_all = pd.concat([df_add_all,df_tmp])

    # 获取以上所有行情信息对应的股票代码列表
    ts_code_l = []
    for i in list(df_add_all.ts_code):
        if '.BJ' not in i:
            if i not in ts_code_l:
                ts_code_l.append(i)

    # 将start_date-end_date期间所有更新的行情数据，按股票代码依次更新到以前保存的行情数据中
    thread_l = []
    for ts_code in ts_code_l:
        thread_l.append(mult_thread(func,(df_add_all, ts_code, start_date)))
        thread_l[-1].start()
    for thread in thread_l:
        thread.join()

if __name__ == '__main__':
    start_date = '20221018'
    end_date = '20221018'
    update_data(start_date=start_date, end_date=end_date)
    #df4 = read_data('601388dotsh')
    #df4 = read_data('000001dotsz')
    #print('df4:',df4)