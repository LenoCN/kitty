# 导入tushare
import tushare as ts
# 初始化pro接口

def get_ths_member(ts_code):
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

    # 拉取数据
    df = pro.ths_member(**{
        "ts_code": ts_code,
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "code",
        "name",
    ])
    return df

if __name__ == '__main__':
    ts_code = '885692.TI'
    df = get_ths_member(ts_code)
    print(df)