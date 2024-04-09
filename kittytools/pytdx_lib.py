import sys
from datetime import datetime, timedelta, date

import pandas as pd
from mult_thread import mult_thread
import tushare as ts
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from pytdx.exhq import TdxExHq_API

import time
from threading import Thread, Event

#api = TdxExHq_API()
#api.connect('106.14.95.149', 7727)
#
#data = api.get_markets()
#print(data)
#data = api.get_instrument_info(0, 100)
#print(data)
#data = api.get_instrument_count()
#print(data)
#data = api.get_instrument_quote(47, "IF1709")
#print(data)
#data = api.get_minute_time_data(47, "IF1709")
#print(data)
#data = api.get_history_minute_time_data(31, "00020", 20170811)
#print(data)
#data = api.get_transaction_data(31, "00020")
#print(data)
#data = api.get_history_transaction_data(47, "IFL0", 20170810, start=1800)
#print(data)
#data = api.get_history_transaction_data(31, "00020", 20170810)
#print(data)

#data = api.get_markets()
#data = api.get_minute_time_data(47, 'IF1709')
#print(data)

def is_holiday(check_date):
    # 中国法定节假日区间列表（以公历日期表示，可能需要根据每年官方公告进行更新）
    holiday_ranges = [
        # 2020年
        (datetime(2020, 1, 1),  datetime(2020, 1, 1)),    # 元旦
        (datetime(2020, 1, 24), datetime(2020, 1, 30)),  # 春节
        (datetime(2020, 4, 4),  datetime(2020, 4, 6)),    # 清明节
        (datetime(2020, 5, 1),  datetime(2020, 5, 5)),    # 劳动节
        (datetime(2020, 6, 25), datetime(2020, 6, 27)),  # 端午节
        (datetime(2020, 9, 29), datetime(2020, 10, 1)),  # 中秋节
        (datetime(2020, 10, 1), datetime(2020, 10, 8)),  # 国庆节
        # 2021年
        (datetime(2021, 1, 1),  datetime(2021, 1, 3)),    # 元旦
        (datetime(2021, 2, 11), datetime(2021, 2, 17)),  # 春节
        (datetime(2021, 4, 3),  datetime(2021, 4, 5)),    # 清明节
        (datetime(2021, 5, 1),  datetime(2021, 5, 5)),    # 劳动节
        (datetime(2021, 6, 12), datetime(2021, 6, 14)),  # 端午节
        (datetime(2021, 9, 19), datetime(2021, 9, 21)),  # 中秋节
        (datetime(2021, 10, 1), datetime(2021, 10, 7)),  # 国庆节
        # 2022年
        (datetime(2022, 1, 1),  datetime(2022, 1, 3)),    # 元旦
        (datetime(2022, 1, 31), datetime(2022, 2, 6)),  # 春节
        (datetime(2022, 4, 3),  datetime(2022, 4, 5)),    # 清明节
        (datetime(2022, 4, 30), datetime(2022, 5, 4)),    # 劳动节
        (datetime(2022, 6, 3),  datetime(2022, 6, 5)),  # 端午节
        (datetime(2022, 9, 10), datetime(2022, 9, 12)),  # 中秋节
        (datetime(2022, 10, 1), datetime(2022, 10, 7)),  # 国庆节
        # 2023年
        (datetime(2022, 12, 31), datetime(2023, 1, 2)),    # 元旦
        (datetime(2023, 1, 21),  datetime(2023, 1, 27)),  # 春节
        (datetime(2023, 4, 5),   datetime(2023, 4, 5)),    # 清明节
        (datetime(2023, 4, 29),  datetime(2023, 5, 3)),    # 劳动节
        (datetime(2023, 6, 22),  datetime(2023, 6, 24)),  # 端午节
        (datetime(2023, 9, 29),  datetime(2023, 10, 6)),  # 中秋节 国庆节
        # 2024年
        (datetime(2024, 1, 1),  datetime(2024, 1, 1)),    # 元旦
        (datetime(2024, 2, 9), datetime(2024, 2, 17)),  # 春节
        (datetime(2024, 4, 4),  datetime(2024, 4, 6)),    # 清明节
        (datetime(2024, 5, 1),  datetime(2024, 5, 5)),    # 劳动节
        (datetime(2024, 6, 10), datetime(2024, 6, 10)),  # 端午节
        (datetime(2024, 9, 15), datetime(2024, 9, 17)),  # 中秋节
        (datetime(2024, 10, 1), datetime(2024, 10, 7)),  # 国庆节
    ]
    # 检查给定日期是否在任何一个节假日区间内
    in_holiday_range = any(start <= check_date <= end for start, end in holiday_ranges)
    # 检查给定日期是否是周末
    is_weekend = check_date.weekday() in (5, 6)
    return in_holiday_range or is_weekend
    # 检查给定日期是否在任何一个节假日区间内

def get_all_tdx_list():
    api = TdxHq_API(multithread=True)
    # 建立连接
    for i in range(100):
        try:
            api.connect('119.147.212.81',7709)
        except:
            time.sleep(1)
        else:
            break
    
    # 获取所有通达信标的代码
    res = []
    for i in range(33):
        data_t = api.get_security_list(0,i*1000)
        if data_t == None:
           continue 
        res = res + data_t
    for i in range(33):
        data_t = api.get_security_list(1,i*1000)
        if data_t == None:
           continue 
        res = res + data_t
    df_res = api.to_df(res)
    df_res = df_res.sort_values(by='code', ascending=True)
    df_res = df_res.reset_index(drop=True)
    #df_res.to_csv('pytdx_lib.lg')
    return df_res
    

def get_latest_hq(code_l):
    api = TdxHq_API(multithread=True)
    api.connect('119.147.212.81',7709)
    data = api.get_security_quotes(code_l)
    df = api.to_df(data)
    return df

def get_all_latest_hq(trade_date):

    # 获取所有股票列表
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    stock_l = pro.stock_basic(exchange='', list_status='L',  fields='ts_code,symbol,name,area,industry,list_date, market')
    stock_l = stock_l[stock_l['name'].str.find('ST') == -1] #去除ST
    stock_l = stock_l[stock_l['market'].str.find('北交所') == -1] #去除北交所

    # 转换为 pytdx接口适用的格式
    code_list = []
    for ts_code in stock_l['ts_code']:
        stock_code,market = ts_code.split('.')
        if market == 'SZ':
            market = 0
        elif market == 'SH':
            market = 1
        code_list.append([market,stock_code])
    
    # 由于限制为每次80个股票，多线程获取最新行情数据
    thread_l = []
    df = None
    for i in range( int(len(code_list)/80) + 1):
        try:
            tmp_l = code_list[i*80:i*80+80] 
        except:
            tmp_l = code_list[i*80:]
        T = mult_thread(get_latest_hq,([tmp_l]))
        thread_l.append(T)
        thread_l[-1].start()
    ret_l = []
    for thread in thread_l:
        thread.join()
        ret = thread.get_result()
        ret_l.append(ret)
    df = pd.concat(ret_l)

    # 转换为tushare格式
    df = df.reset_index()
    df_o = pd.DataFrame(columns=['ts_code','market','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount'])
    df_o['ts_code']  = df['code']
    df_o['market']  = df['market']
    df_o['trade_date'] = trade_date
    df_o['open']  = df['open']
    df_o['close'] = df['price']
    df_o['high']  = df['high']
    df_o['low']   = df['low']
    df_o['amount']   = df['amount']/1000

    for i in range(len(df_o)):
        if df_o['market'][i] == 0:
            df_o['ts_code'][i] = df_o['ts_code'][i] +'.SZ'
        elif df['market'][i] == 1:
            df_o['ts_code'][i] = df_o['ts_code'][i] +'.SH'
    df_o = df_o.drop(columns='market')
    return df_o


def get_today_data(ts_code,trade_date):
    stock_code,market = ts_code.split('.')
    if market == 'SZ':
        market = 0
    elif market == 'SH':
        market = 1
    #print(stock_code,market)
    api = TdxHq_API(multithread=True)
    for _ in range(10):
        try:
            api.connect('119.147.212.81',7709)
            data = api.get_security_bars(9, market, stock_code, 0, 1)
            df = api.to_df(data)
            datetime = str(df['year'][0]) + str(df['month'][0]) + str(df['day'][0])
            if datetime != trade_date:
                return None
            tmp_l = [[ts_code, trade_date, df['open'][0], df['high'][0], df['low'][0], df['close'][0],0,0,0,0,df['amount'][0]/1000]]
        except:
            time.sleep(1)
        else:
            break
    df = pd.DataFrame(tmp_l, columns=['ts_code','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount'])
    return df

def get_market(s):
    if s.startswith(('68', '60')):
        return TDXParams.MARKET_SH
    elif s.startswith(('00', '30')):
        return TDXParams.MARKET_SZ
    else:
        print('Error: 未识别市场的股票代码: '+ s)

'''
def get_first_n_data_elements(stock_id, num, date):
    sleep_time = 1
    timeout_duration = 1  # 设置超时时间为3秒
    retry = 0
    while True:
        try:
            api = TdxHq_API(multithread=True)
            api.connect('119.147.212.81', 7709)
            index = 2800
            data_chunk = None
            done_event = Event()

            def fetch_data():
                nonlocal data_chunk
                print(get_market(stock_id), stock_id, index, 2000, date)
                data_chunk = api.get_history_transaction_data(get_market(stock_id), stock_id, index, 2000, date)
                done_event.set()

            fetch_thread = Thread(target=fetch_data)
            fetch_thread.start()
            fetch_thread.join(timeout=timeout_duration)
            index = max(0, index - 2000)  # 减少步长逼近
            if not done_event.is_set():
                raise TimeoutError("Fetching data timed out")
            if data_chunk:
                api.disconnect()
                #time.sleep(sleep_time)  # 在每次重试之后添加延迟
                return data_chunk[:num], date
        except Exception as e:
            retry = retry + 1
            print(f"Error fetching data for {stock_id} on {date}: {e}, Retrying... ({retry + 1})\n")
            api.disconnect()
            time.sleep(sleep_time)  # 在每次重试之后添加延迟

'''
# 返回从该索引到末尾的数据，最多2000个
def get_first_n_data_elements(stock_id, num, date):
    max_retries = 100;
    retries = 0;
    sleep_time = 1;
    while retries < max_retries:
        try:
            retries = retries + 1
            # 从中间值开始，以较大的步长逼近
            api = TdxHq_API(multithread=True)
            api.connect('119.147.212.81',7709)
            index = 2800
            step = 2000  # 初始步长设置为大约数据长度范围的1/4
            collected_data = []
            while True:
                # 获取数据块
                # print(get_market(stock_id), stock_id, index, 2000, date)
                data_chunk = api.get_history_transaction_data(get_market(stock_id), stock_id , index, 2000, date);
                # 如果获取到的数据块为空，说明实际数据长度小于当前索引
                if not data_chunk:
                    # 如果获取不到数据，进入外层循环重试
                    if index == 0:
                        break
                    # 减少步长逼近，但保持步长不小于1
                    index = max(0, index - step)
                    continue
                # 如果已经收集到足够的数据
                else:
                    # 返回前num个数据
                    api.disconnect()
                    return data_chunk[:num], date
        except Exception as e:
            print(f"Error fetching data for {stock_id} on {date}: {e}")
            print(f"Retrying... ({retries+1}/{max_retries})")
            retries += 1
            #time.sleep(sleep_time)  # 在每次重试之后添加延迟
    print(f"Failed to fetch data for {stock_id} on {date} after {max_retries} attempts.")
    return None
            
def workdays_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    day_count = (end - start).days + 1
    workdays = [
        (start + timedelta(days=i))
        for i in range(day_count)
        if (start + timedelta(days=i)).weekday() < 5 and not is_holiday(start + timedelta(days=i))
    ]
    return [day.strftime("%Y%m%d") for day in workdays]


        
if __name__ == "__main__":
    api = TdxHq_API(multithread=True)
    api.connect('119.147.212.81',7709)
    #get_all_tdx_list()

    
    #data = api.get_security_quotes([[1,'880761']])
    #data = api.get_security_quotes([[0,'000099']])
    
    data_l = []
    start_date = '2024-04-01'
    end_date   = '2024-04-03'
    stock_id = '000737'
    date_s_l = workdays_list(start_date=start_date, end_date=end_date)
    date_l = [int(date) for date in date_s_l]
    print(date_l)
    for date in date_l:
        data_l.append(get_first_n_data_elements(stock_id=stock_id, num=3, date=date))
    
    for data,date in data_l:
        df = api.to_df(data)
        print(date)
        print(df)
        
    #data = api.get_history_transaction_data(TDXParams.MARKET_SZ, '000628', 0, 10, 20240207)
    #df = api.to_df(data)
    #print(df)
    #data = api.get_history_transaction_data(TDXParams.MARKET_SZ, '000628', 0, 10, 20240208)
    #df = api.to_df(data)
    #print(df)
    #data = api.get_transaction_data(TDXParams.MARKET_SZ, '000099', 4720, 100)
    
    
    #data = api.get_security_count(0)
    #df = api.to_df(data)
    #data = api.get_security_list(0,4000)
    #df = api.to_df(data)

    #BLOCK_SZ = "block_zs.dat"
    #BLOCK_FG = "block_fg.dat"
    #BLOCK_GN = "block_gn.dat"
    #BLOCK_DEFAULT = "block.dat"
    #data = api.get_and_parse_block_info(TDXParams.BLOCK_DEFAULT)

    #df = api.to_df(data)
    #df.to_csv('pytdx_lib.lg')
    #print(df)
