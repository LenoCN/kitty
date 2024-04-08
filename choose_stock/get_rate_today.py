import sys
import time
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.get_ths_index import get_ths_index
from kittytools.get_ths_daily import get_ths_daily
from kittytools.get_rate import get_rate
import pandas as pd
import datetime as dt


def get_rate_today():
    d = dt.datetime.now()
    year = d.year
    month = d.month
    day = d.day
    hour = d.hour
    if hour < 21:
        day = day - 1
    #start_date = [2016, 6, 2]
    start_date = [2021, 6, 2]
    end_date = [year , month , day]
    print('time :', year, month, day)
    offset = 0
    rate = []

    df_ths_index = get_ths_index()
    print('lenth of ts_code : ', len(df_ths_index.ts_code))
    for i,ts_code in enumerate(df_ths_index.ts_code):
        df_ths_daily = get_ths_daily(ts_code, start_date, end_date)
        df_ths_daily = df_ths_daily.sort_values(by='trade_date', ascending=True)
        rate_lastday = get_rate(df_ths_daily, ts_code=ts_code, offset=1)
        rate_today = get_rate(df_ths_daily,  ts_code=ts_code, offset=0)
        try:
            rate.append([ts_code, df_ths_index['name'][i], rate_lastday, rate_today])
        except:
            print('[Exception] : ts_code: ', ts_code, df_ths_index['name'][i])
        if i % 100 == 0:
            print('Notify : ',i)
        #if i == 10:
        #    break

    return rate

if __name__ == '__main__':

    rate = get_rate_today()
    df = pd.DataFrame(rate, columns=['ts_code','name', 'rate_lastday', 'rate_today'])
    df.to_csv('choose_stock/rate_today', sep='\t')

    df = pd.read_csv('choose_stock/rate_today', sep='\t')
    #df = df.sort_values(by='rate_lastday', ascending=True)
    for i,ts_code in enumerate(df.ts_code):
        if df.rate_lastday[i] < df.rate_today[i] and df.rate_today[i] > 0.65 and df.rate_today[i] < 0.85:
            print(ts_code, df.name[i], df.rate_lastday[i], df.rate_today[i])
