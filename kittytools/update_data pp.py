# 导入tushare
import tushare as ts
import time
import pyarrow.parquet as pp
import pyarrow as pa
# 初始化pro接口
import pandas as pd
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.get_ths_daily import get_ths_daily
from kittytools.get_daily import get_daily

def update_ths_index_hq(start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

    # 获取期间所有交易日期
    df = pro.trade_cal(exchange='SSE', is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
    cal_date_l = df['cal_date'].tolist()
    
    # 获取期间所有股票的日线行情信息
    df_add_all=None
    for i in cal_date_l:
        print(i)
        df_tmp = get_ths_daily('',i,i)
        df_add_all = pd.concat([df_add_all,df_tmp])
    
    # 将start_date-end_date期间所有更新的行情数据, 与历史行情数据合并，并重新保存
    df = pp.read_table('df_ths_all_hq.parquet').to_pandas()
    df = pd.concat([df, df_add_all])
    df = df.reset_index(drop=True)
    df = df.sort_values(by='trade_date')
    pp.write_table(pa.Table.from_pandas(df), 'df_parquet.parquet')


def update_stock_hq(start_date, end_date):
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
    
    df_add_all = df_add_all[df_add_all['ts_code'].str.find('.BJ') == -1]


    # 将start_date-end_date期间所有更新的行情数据, 与历史行情数据合并，并重新保存
    df = pp.read_table('df_parquet.parquet').to_pandas()
    df = pd.concat([df, df_add_all])
    df = df.reset_index(drop=True)
    df = df.sort_values(by='trade_date')
    pp.write_table(pa.Table.from_pandas(df), 'df_parquet.parquet')

if __name__ == '__main__':
    #start_date = '20221205'
    #end_date   = '20230416'
    #update_stock_hq(start_date=start_date, end_date=end_date)
    
    df = pp.read_table('df_parquet.parquet').to_pandas()
    df = df[df['ts_code'] == '002685.SZ']
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    print('start')
    print(df)
