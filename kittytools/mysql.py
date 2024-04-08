import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 
 
# 初始化数据库连接，使用pymysql模块
db_info = {
    'user': 'root',
    'password': '1234',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'trade_data'
}


def read_data(name):
    engine = create_engine(
        'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info,
        encoding='utf-8',pool_size=1000,pool_timeout=1000
    )
    engine_con = engine.connect()
    sql = """SELECT * FROM %s""" % name
    df = pd.read_sql_query(sql, engine_con)
    engine_con.close()
    return df


def write_data(df, name):
    engine = create_engine(
        'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info,
        encoding='utf-8',pool_size=1000,pool_timeout=1000
    )
    engine_con = engine.connect()
    #res = df.to_sql(name, engine, index=False, if_exists='append', chunksize=5000)
    res = df.to_sql(name, engine_con, index=False, if_exists='replace', chunksize=5000)
    engine_con.close()
    if res is not None:
        print(res)

def rename(name):
    return  name.split('.')[0] + 'DOT' + name.split('.')[1]


if __name__ == '__main__':
#     df = read_data()
    name = 'stock_basic'
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    df = pro.stock_basic()
    write_data(df=df, name=name)
    df = read_data(name=name)
    print(df)