
# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('06e94cac4f4e03d170ca18f20d2e2ba7bbe2b6f7b5c328db0167ae26')

# 拉取数据
df = pro.index_basic(**{
    "ts_code": "",
    "market": "SW",
    "publisher": "",
    "category": "二级行业指数",
    "name": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "name",
    "market",
    "publisher",
    "category",
    "base_date",
    "base_point",
    "list_date"
])

df.to_csv('index_basic_sw',sep='\t')

        