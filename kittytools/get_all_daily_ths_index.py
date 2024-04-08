# 导入tushare
import py_compile
from sys import getallocatedblocks
from tracemalloc import start
import tushare as ts
from kittytools.get_daily import get_daily
from kittytools.get_ths_member import get_ths_member
from kittytools.add_boll import add_boll
from kittytools.mysql import read_data, write_data
# 初始化pro接口

def get_all_daily_ths_index(ths_index_code, start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    ths_member = get_ths_member(ths_index_code)
    for ts_code in ths_member.code:
        df = get_daily(ts_code, start_date=start_date, end_date=end_date)
        df = df.sort_values(by='trade_date', ascending=True)
        df = add_boll(df)
        name = ts_code.split('.')[0] + 'DOT' + ts_code.split('.')[1]
        write_data(df, name.lower())


if __name__ == "__main__":
    start_date = '20160602'
    end_date = '20220609'
    ths_index_code = '885692.TI'

    get_all_daily_ths_index(ths_index_code=ths_index_code, start_date=start_date, end_date=end_date) 

    ts_code = '000407dotsz'
    df = read_data(ts_code)