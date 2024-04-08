import pandas as pd
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.get_fund_basic import get_fund_basic
from kittytools.get_fund_daily import get_fund_daily
from kittytools.mysql import read_data, write_data
from get_all_fund_daily import get_all_fund_daily


def find_fund():
    #get_all_fund_daily()
    result_l = []
    df_fund_basic = get_fund_basic()
    print('Length of df_fund_basic : %d' % len(df_fund_basic))
    for i, ts_code in enumerate(df_fund_basic.ts_code):
        name = ts_code.split('.')[0] + 'DOT' + ts_code.split('.')[1]
        df_fund_daily = read_data(name.lower())
        #if df_fund_daily.iloc[-1].amount > 50000:
        if df_fund_daily.iloc[-1].amount > 50000:
            length = len(df_fund_daily)
            if length <2 :
                continue
            rate_lastday = df_fund_daily.rate[length-2]
            rate_today = df_fund_daily.rate[length-1]
            close_lastday = df_fund_daily.close[length-2]
            close_today = df_fund_daily.close[length-1]
            low_today = df_fund_daily.low[length-1]
            #if  rate_today > 0.55 and rate_today < 0.9:
                #if low_today < close_lastday and close_today/low_today > 1.02:
                #    result_l.append([ts_code, df_fund_basic.name[i], rate_lastday, rate_today, df_fund_daily.amount[0], close_today/low_today])
                #elif rate_lastday < rate_today and close_today/close_lastday > 1.02:
                #    result_l.append([ts_code, df_fund_basic.name[i], rate_lastday, rate_today, df_fund_daily.amount[0], close_today/low_today])
            result_l.append([ts_code, df_fund_basic.name[i], rate_lastday, rate_today, df_fund_daily.iloc[-1].amount, df_fund_daily.iloc[-1].trendfactor])
            #result_l.append([ts_code, df_fund_basic.name[i], rate_lastday, rate_today, df_fund_daily.amount[0], close_today/low_today])
        if i == 50:
            break
        if i % 50 == 0:
            print('Current index: %d' %i)
    df = pd.DataFrame(result_l, columns=['ts_code','name', 'rate_lastday', 'rate_today', 'amount', 'trendfactor'])
    return df

if __name__ == '__main__':
    df = find_fund()
    write_data(df, 'find_fund')
    #df = read_data('find_fund')
    df = df.sort_values(by='trendfactor', ascending=False)
    df.to_csv('tmp',sep='\t')