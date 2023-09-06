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

bondDefinedCodes = []
for page in range(1, 6):
    data = {
        "pageNo": str(page),
        # "pageNo": "1",
        "pageSize": 15,
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
    results = data['resultList']
    # 测试
    # print(results)

    # 循环拿到的主页中的url返回
    for result in results:
        bondDefinedCode = result['bondDefinedCode']

        # 拿到bondDefinedCode对应的url，查看返回，发现不需要进行进一步的数据处理
        # print(bondDefinedCode)
        # 添加到定义的列表中，用于后续循环拿去数据进行请求
        bondDefinedCodes.append(bondDefinedCode)

# 拿到了所有params中的url并使用列表存储
# print(bondDefinedCodes)

# 循环刚刚保存的url列表
all_data=[]
n = 0
for i in bondDefinedCodes:
    url = 'https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondDetailInfoEN'

    # print(i)

    # 通过抓包判断出可以是GET可以是POST，我采取GET方法，使用url传参的形式进行请求
    params = {
        "bondDefinedCode": i
    }
    # 发送每一个GET请求
    resps = requests.get(url, headers=headers, params=params)
    # 处理编码
    resps.encoding = "utf-8"
    # 返回的响应为JSON格式，进行序列化拿值
    datas = resps.json()

    result_data = datas['data']['bondBaseInfo']
    all_data.append(result_data)
    print(result_data)

bond_data = []
# 循环获取到的json数据，然后使用pandas来保存数据为CSV文件
for result_data in all_data:
    bond_data.append({
        'bondCode': result_data['bondCode'],
        'bondPeriod': result_data['bondPeriod'],
        'couponFrqncy': result_data['couponFrqncy'],
        'couponType': result_data['couponType'],
        'frstValueDate': result_data['frstValueDate'],
        'isinCode': result_data['isinCode'],
        'issueAmnt': result_data['issueAmnt'],
        'issueDate': result_data['issueDate'],
        'issuePrice': result_data['issuePrice'],
        'lstngDate': result_data['lstngDate'],
        'mrtyDate': result_data['mrtyDate'],
        'parValue': result_data['parValue'],
        'plndIssueAmnt': result_data['plndIssueAmnt']
    })

df = pd.DataFrame(bond_data)
df.to_csv('bond_data.csv', index=False, encoding='utf-8-sig')