import tushare as ts

def get_sw_daily(ts_code, start_date, end_date):
  # 导入tushare
  # 初始化pro接口
  pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')
  start_date_str = str(start_date[0]) + str(start_date[0]) + str(start_date[0])
  end_date_str = str(end_date[0]) + str(end_date[0]) + str(end_date[0])

  # 拉取数据
  df = pro.sw_daily(**{
      "ts_code": ts_code,
      "trade_date": "",
      "start_date": start_date_str,
      "end_date": end_date_str,
      "limit": "",
      "offset": ""
  }, fields=[
      "ts_code",
      "trade_date",
      "close",
      "open",
      "high",
      "low",
      "change",
      "vol",
      "amount"
  ])
  return df


if __name__ == '__main__':
    start_date = [2015, 6, 15]
    end_date = [2022, 6 , 1]
    ts_code = '850543.SI'
    df = get_sw_daily(ts_code, start_date, end_date)
    print(df)