# 导入tushare
import tushare as ts
# 初始化pro接口
import pandas as pd
from kittytools.get_daily import get_daily
from kittytools.mysql import write_data,read_data 
import time

def dl_all_data():
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    #start_data = '20220929'
    start_data = '19970428'
    end_data = '20221001'
    df = pro.trade_cal(exchange='SSE', is_open='1', 
                        start_date=start_data, 
                        end_date=end_data, 
                        fields='cal_date')
    #print(df.loc[58])
    cl = df['cal_date'].tolist()

    dfo=None
    for i in cl:
        print(i)
        df_tmp = get_daily('',i,i)
        dfo = pd.concat([dfo,df_tmp])
    #dfo.to_csv('tmp1002')
    write_data(dfo,'alldata')

    newl = []
    for i in list(dfo.ts_code):
        if i not in newl:
            newl.append(i)
    print(len(newl))
    for name in newl:
        print(name)
        df3 = dfo.loc[dfo['ts_code']==name]
        #print('df3:',df3)
        name = name.split('.')[0] + 'DOT' + name.split('.')[1]
        write_data(df3, name.lower())
        df4 = read_data(name.lower())
        #print('df4:',df4)
        #time.sleep(3)


if __name__ == '__main__':
    #dl_all_data()
    df4 = read_data('000001dotsz')
    print('df4:',df4)