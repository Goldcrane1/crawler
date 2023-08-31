# 引入需要的模块
import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import lxml
import json

# 引入url地址
url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"

# UA伪装
headers = {

    "Cookie": """apache=bbfde8c184f3e1c6074ffab28a313c87; _ulta_id.ECM-Prod.ccc4=6724f780a0907292; lss=fd9e664ef34511dcdc4a51a4e8d84abc; _ulta_id.CM-Prod.ccc4=c540c3de0d31b873; _ulta_ses.ECM-Prod.ccc4=708e67ee0de188d5; AlteonP10=AnnuFCw/F6wHJb0++uJ/MQ$$""",
    "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"""
}

for page in range(1, 6):
    data = {
        "pageNo": str(page),
        # "pageNo": "1",
        "pageSize": "15",
        "isin": "",
        "bondCode": "",
        "issueEnty": "",
        "bondType": "100001",
        "couponType": "",
        "issueYear": "2023",
        "rtngShrt": "",
        "bondSpclPrjctVrty": ""
    }
    # 发起post请求
    resp = requests.post(url, headers=headers, data=data)
    # 头部编码为utf-8
    resp.encoding = "utf-8"
    # data是ajax技术发送的请求
    dic_obj = resp.json()
    # 数据序列化json，获取data
    data = dic_obj['data']
    # 拿键
    result = data['resultList']
    # 测试
    print(result)

    # 将数据转换为pandas中的DataFrame
    df = pd.DataFrame(result)
    print(f"正在爬取第{page}页数据")
    # # 将DataFrame写入CSV文件  不需要索引
    df.to_csv('data.csv', index=False)
