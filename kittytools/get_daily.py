# 导入tushare
import tushare as ts
# 初始化pro接口
import pandas as pd
import time

def get_daily(ts_code, start_date, end_date):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    # 拉取数据
    for _ in range(3):
        try:
            df = pro.daily(**{
                "ts_code": ts_code,
                "trade_date": "",
                "start_date": start_date,
                "end_date": end_date,
                "offset": "",
                "limit": ""
            }, fields=[
                "ts_code",
                "trade_date",
                "open",
                "high",
                "low",
                "close",
                "pre_close",
                "change",
                "pct_chg",
                "vol",
                "amount"
            ])
        except:
            time.sleep(1)
        else:
            return df


if __name__ == '__main__':
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    df = pro.trade_cal(exchange='SSE', is_open='1', 
                        start_date='20200101', 
                        end_date='20200115', 
                        fields='cal_date')
    #print(df.loc[58])
    cl = df['cal_date'].tolist()

    dfo=None
    for i in cl:
        print(type(i))
        df_tmp = get_daily('',i,i)
        dfo = pd.concat([dfo,df_tmp])
    dfo.to_csv('tmp1001')
    print(dfo)
    
    
    