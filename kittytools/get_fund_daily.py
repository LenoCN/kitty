from tokenize import endpats
import tushare as ts


def get_fund_daily(ts_code, start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

    # 拉取数据
    df = pro.fund_daily(**{
        "trade_date": "",
        "start_date": start_date,
        "end_date": end_date,
        "ts_code": ts_code,
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "pre_close",
        "open",
        "high",
        "low",
        "close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])
    return df

if __name__ == '__main__':
    #start_date = [2015, 6, 15]
    #end_date = [2022, 6 , 1]
    start_date = '' 
    end_date = '' 
    ts_code = '510050.SH'
    df  = get_fund_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    print(df)
