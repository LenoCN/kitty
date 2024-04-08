
# 导入tushare
import tushare as ts

def get_ths_index():
    # 初始化pro接口
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    # 拉取数据
    df = pro.ths_index(**{
        "ts_code": "",
        "exchange": "A",
        "type": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "name",
        "count",
        "exchange",
        "list_date",
        "type"
    ])
    return df

if __name__ == '__main__':
    df = get_ths_index()
    print(df)