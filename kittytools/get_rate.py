import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.add_boll import add_boll
from kittytools.get_ths_daily import get_ths_daily

def get_rate(df, ts_code, offset):
    df_out = add_boll(df)
    if len(df_out.rate) == 0:
        print('Length of df_out is 0 , ts_code: ', ts_code)
        return 0
    try:
        rate = df_out.rate[offset]
    except:
        print('Error : ts_code :', ts_code)
        return 0
    return rate

if __name__ == '__main__':
    start_date = '20160602'
    end_date = '20220609'
    #ts_code = '885922.TI' #盐湖提锂
    ts_code = '884014.TI' #煤炭开采

    df = get_ths_daily(ts_code, start_date, end_date)
    df = df.sort_values(by='trade_date', ascending=True)
    offset = 1
    rate = get_rate(df, ts_code=ts_code, offset=offset)
    print(rate)