import sys
from time import time
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.get_fund_basic import get_fund_basic
from kittytools.get_fund_daily import get_fund_daily
from kittytools.add_boll import add_boll
from kittytools.add_boll import add_sma
from kittytools.add_trend_factor import add_trend_factor
from kittytools.mysql import read_data, write_data

def get_all_fund_daily():

    df_fund_basic = get_fund_basic()
    print(df_fund_basic)
    print('Length of df_fund_basic : %d' % len(df_fund_basic))
    for i, ts_code in enumerate(df_fund_basic.ts_code):
        #df_fund_daily = get_fund_daily(ts_code=ts_code, start_date='', end_date='')
        #df_fund_daily = add_boll(df_fund_daily)
        #df_fund_daily = add_sma(df_fund_daily)
        #df_fund_daily = add_trend_factor(df_fund_daily, time_period=40)
        name = ts_code.split('.')[0] + 'DOT' + ts_code.split('.')[1]
        try:
            df_fund_daily = read_data(name.lower())
        except:
            print('Get data from SQL Error.')
        df_fund_daily = add_trend_factor(df_fund_daily, time_period=40)
        write_data(df_fund_daily, name.lower())
        if i % 50 == 0:
            print('Current index: %d' %i)

if __name__ == '__main__':
    get_all_fund_daily()