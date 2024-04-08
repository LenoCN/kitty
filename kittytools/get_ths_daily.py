import tushare as ts
import time

def get_ths_daily(ts_code, start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    for i in range(100):
        try:
            df = pro.ths_daily(**{
                "ts_code": ts_code,
                "trade_date": "",
                "start_date": start_date,
                "end_date": end_date,
                "limit": "",
                "offset": ""
            }, fields=[
                "ts_code",
                "trade_date",
                "close",
                "open",
                "high",
                "low",
                "pre_close",
                "avg_price",
                "change",
                "pct_change",
                "vol",
                "turnover_rate",
                "total_mv",
                "float_mv",
                "pe_ttm",
                "pb_mrq"
            ])
        except:
            time.sleep(1)
            pass
        else:
            return df
    print('Error: get ths hq error. ts_code: %s' % ts_code)