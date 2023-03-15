# from asyncio import current_task
import pandas as pd
import requests

url = "https://www.pdmarket.cn/ocrm/receiptAdd?\
        applyAt=1677204737150&\
        companyName=汉洋分公司0005&\
        currencyName=人民币&\
        customName=John+Hancock+Financial+Services&\
        receiptRate=1&\
        shipName=GEORGE+WASHINGTON+BRIDGE&\
        voyagesName=VOYAGE_6350052&receiptTable={\"cells\":[{\"content\":\"测试摘要\",\"fundCategory\":\"5501.07船船管理费用Ship+management+fee\",\"orgGathered\":50000,\"orgPay\":0,\"usdGathered\":\"50000\",\"usdPay\":\"0\"},{\"content\":\"测试摘要\",\"fundCategory\":\"5501.04修理和维护Repair+and+maintenance\",\"orgGathered\":0,\"orgPay\":50000,\"usdGathered\":\"0\",\"usdPay\":\"50000\"}],\"gatheredTotal\":0,\"orgGatheredTotal\":50000,\"orgPayTotal\":50000,\"usdGatheredTotal\":50000,\"usdPayTotal\":50000}&attachFiles=&token=jBwgYHSkjp&receiptType=1"

url = "https://www.pdmarket.cn/ocrm/receiptAdd?"
form_data = {
    'applyAt':1677204737150,
    'companyName':None,
    'currencyName':None,

    }


payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)