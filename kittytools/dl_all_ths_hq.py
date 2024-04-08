from ast import arg
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
# 导入tushare
import tushare as ts
# 初始化pro接口
import pandas as pd
from kittytools.get_ths_daily import get_ths_daily
from kittytools.get_ths_index import get_ths_index
from kittytools.mult_thread import mult_thread
from kittytools.mysql import write_data,read_data 
import time
import pyarrow.parquet as pp
import pyarrow as pa


def dl_all_ths_hq():
    df_ths_index = get_ths_index()
    ths_index_l = df_ths_index['ts_code'].to_list()


    res_l = []
    thread_l = []
    for ths_index in ths_index_l:
        print(ths_index)
        thread = mult_thread(func=get_ths_daily,args=[ths_index,'',''])
        thread_l.append(thread)
        thread_l[-1].start()
    for thread in thread_l:
        thread.join()
        res = thread.get_result()
        res_l.append(res)
    if res_l == []:
        print('Error: No object.')
        return None
    df_all_ths = pd.concat(res_l)
    df_all_ths = df_all_ths.reset_index(drop=True)
    print(df_all_ths)
    pp.write_table(pa.Table.from_pandas(df_all_ths), 'df_ths_all_hq.parquet')
    return df_all_ths


if __name__ == '__main__':
    
    #res = get_ths_daily('','','')
    #print(res)
    #dl_all_ths_hq()
    
    df_all_ths = pp.read_table('df_ths_all_hq.parquet').to_pandas()
    print(df_all_ths)
    #pp.write_table(pa.Table.from_pandas(df_all_ths), 'df_ths_all_hq.parquet')