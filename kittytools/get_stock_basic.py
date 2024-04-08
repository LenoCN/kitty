# 导入tushare
import tushare as ts
# 初始化pro接口

def get_stock_basic():
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
    return df


if __name__ == '__main__':
    df = get_stock_basic()
    print(df)
        