import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.get_ths_member import get_ths_member
from kittytools.mysql import read_data
from kittytools.get_all_daily_ths_index import get_all_daily_ths_index

if __name__ == '__main__':

    start_date = '20160602'
    end_date = '20220609'
    #ths_index_code = '885692.TI' #地下管网 
    #ths_index_code = '885810.TI' #大豆
    #ths_index_code = '885811.TI' #玉米
    #ths_index_code = '885877.TI' #转基因
    #ths_index_code = '883962.TI' #国家队增持
    #ths_index_code = '884007.TI' #畜禽养殖 
    #ths_index_code = '884012.TI' #农业综合 
    ths_index_code = '884067.TI' #基础建设 
    #df = pd.read_csv('choose_stock/rate_today', sep='\t')
    ##df = df.sort_values(by='rate_lastday', ascending=True)
    #for i,ths_index_code in enumerate(df.ts_code):
    #    if ths_index_code == '883401.TI' or ths_index_code == '864018.TI' or ths_index_code == '864027.TI' or ths_index_code == '864028.TI':
    #        continue
    #    try:
    #        if df.rate_lastday[i] < df.rate_today[i] and df.rate_today[i] > 0.65 and df.rate_today[i] < 0.85:
    #            print(ths_index_code, df.name[i], df.rate_lastday[i], df.rate_today[i])
    #            name = df.name[i]
    get_all_daily_ths_index(ths_index_code=ths_index_code, start_date=start_date, end_date=end_date) 
    ths_member = get_ths_member(ths_index_code)
    for i,ts_code in enumerate(ths_member.code):
        name = ts_code.split('.')[0] + 'DOT' + ts_code.split('.')[1]
        df = read_data(name.lower())
        #df = df.sort_values(by='trade_date', ascending=True)
        df = df.sort_values(by='trade_date', ascending=True)
        length = len(df)
        if length <2 :
            continue
        rate_lastday = df.rate[length-2]
        rate_today = df.rate[length-1]
        #if rate_lastday < rate_today and rate_today > 0.6 and rate_today < 0.85:
        if rate_lastday < rate_today and rate_today < 0.6 and rate_today > 0.5:
            print(ts_code, ths_member.name[i], rate_lastday, rate_today)
    #except:
    #        print(df)
