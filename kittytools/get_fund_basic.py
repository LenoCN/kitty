# 导入tushare
import tushare as ts

def get_fund_basic():
    pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
    # 拉取数据
    df = pro.fund_basic(**{
        "ts_code": "",
        "market": "E",
        "update_flag": "",
        "offset": "",
        "limit": "",
        "status": "L",
        "name": ""
    }, fields=[
        "ts_code",
        "name",
        "management",
        "custodian",
        "fund_type",
        "found_date",
        "due_date",
        "list_date",
        "issue_date",
        "delist_date",
        "issue_amount",
        "m_fee",
        "c_fee",
        "duration_year",
        "p_value",
        "min_amount",
        "exp_return",
        "benchmark",
        "status",
        "invest_type",
        "type",
        "trustee",
        "purc_startdate",
        "redm_startdate",
        "market"
    ])
    return df


if __name__ == '__main__':
    df = get_fund_basic()
    print(df)

        