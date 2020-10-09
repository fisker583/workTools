import requests
import json
from bs4 import BeautifulSoup
import time
import pandas as pd
import itertools
import re


def requestPage(page, start, limit):
    pageParma = 'page={}&start={}&limit={}'.format(
        str(page), str(start), str(limit))
    timeParma = str(round(time.time() * 1000))
    url = "http://crm.mlnacc.com/Khgl/Consultant/GetLeaderInfo?_dc=" + timeParma
    payload = pageParma + '&users=%27admin%27%2C%27test3%27%2C%27%u676D%u5DDE%u4F5C%u5E9F%27%2C%27%u5BA2%u670D%27%2C%27%u7A0B%u5A9B%u5A9B%27%2C%27%u987E%u9676%u9759%27%2C%27%u90DD%u80DC%u78CA%27%2C%27%u4FAF%u6D01%27%2C%27%u80E1%u82AC%27%2C%27%u9EC4%u6653%u7487%27%2C%27%u6C5F%u4FCA%u704F%27%2C%27%u5C45%u7EF4%u5A1C%27%2C%27%u674E%u84D3%u534E%27%2C%27%u674E%u4E3D%u5A9B%27%2C%27%u674E%u677E%u9716%27%2C%27%u5218%u4F73%u59AE%27%2C%27%u5218%u5029%u6587%27%2C%27%u5218%u5B50%u7433%27%2C%27%u5362%u4F73%27%2C%27%u7F57%u601D%u8BD7%27%2C%27%u5B81%u8389%27%2C%27%u5B81%u73AE%27%2C%27%u4EFB%u5A49%u5A77%27%2C%27%u5C71%u8FC8%27%2C%27%u6C88%u5B9D%u7965%27%2C%27%u5B59%u5029%27%2C%27%u5B59%u6587%u9759%27%2C%27%u738B%u6155%u5149%27%2C%27%u738B%u5EF7%u654F%27%2C%27%u81E7%u9038%u8D07%27%2C%27%u5F20%u6653%u60E0%27%2C%27%u5F20%u6653%u7490%27%2C%27%u90D1%u6167%u5FC3%27%2C%27%u6731%u4E3D%27%2C%27%u6731%u76DB%u534E%27%2C%27%u5218%u5E86%u6797%27%2C%27juliet%27%2C%27%u7A0B%u957F%u6CE2%27%2C%27test1%27%2C%27%u5317%u4EAC%27%2C%27%u91D1%u665F%27%2C%27%u674E%u6590%27%2C%27%u6797%u91D1%u73B2%27%2C%27%u5218%u7490%27%2C%27%u6155%u8FDC%27%2C%27%u738B%u747E%27%2C%27%u6587%u6676%27%2C%27%u5F90%u5DCD%27%2C%27%u676D%u5DDE%27%2C%27%u5218%u8D24%u9704%27%2C%27%u9648%u60A6%27%2C%27%u7A0B%u7476%27%2C%27%u676D%u5DDE%u8FC7%u6E21%27%2C%27%u676D%u5DDE%u53F7%27%2C%27%u676D%u5DDE%u4E2D%27%2C%27%u5415%u7B11%u7ACB%27%2C%27%u738B%u6960%27%2C%27%u5434%u96C5%u96EF%27%2C%27%u59DC%u6653%u4E91%27%2C%27%u9A6C%u6765%u897F%u4E9A%27%2C%27%u5415%u5229%27%2C%27%u8463%u5C0F%u8273%27%2C%27%u82DF%u4E91%u5E06%27%2C%27%u6797%u96EF%u4E3D%27%2C%27%u7F57%u56FD%u6881%27%2C%27%u5434%u8BED%u806A%27%2C%27%u9999%u542F%u5EB7%27%2C%27%u8C22%u4F73%u6F94%27%2C%27%u66FE%u7EF4%u4F26%27%2C%27%u7AE0%u94E0%u68CB%27%2C%27%u4E0A%u6D77%27%2C%27%u53F6%u83C1%27%2C%27%u66F9%u91D1%u79CB%27%2C%27%u9648%u4E9A%u5170%27%2C%27%u6210%u4E39%u4E39%27%2C%27%u4F55%u8273%u5A77%27%2C%27%u674E%u6797%27%2C%27%u674E%u5B50%u7199%27%2C%27%u5218%u8389%27%2C%27%u4E0A%u6D77%u53F7%27%2C%27%u738B%u65D6%27%2C%27%u738B%u6C38%u8000%27%2C%27%u5F20%u695A%u4E91%27%2C%27%u5468%u66E6%u5F64%27%2C%27%u6731%u8389%27%2C%27%u738B%u5C91%u5A77%27%2C%27%u5357%u4EAC%27%2C%27%u9648%u5A77%u5A77%27%2C%27%u94B1%u946B%27%2C%27%u6768%u9759%27%2C%27%u4FDE%u7ACB%u5EAD%27%2C%27%u5357%u4EAC%u4E2D%27%2C%27%u5CB3%u8FDB%u8FDB%27%2C%27test2%27%2C%27%u6DF1%u5733%27%2C%27%u90ED%u6653%u7EA2%27%2C%27%u8C2D%u745E%27%2C%27%u4E07%u6B63%27%2C%27%u6C6A%u6C38%u5E73%27%2C%27%u97E6%u73CD%u73CD%27%2C%27%u66FE%u7075%u8D24%27%2C%27%u5434%u6D77%u6620%27%2C%27%u5E7F%u5DDE%u4E2D%27%2C%27%u5218%u73B2%27%2C%27%u65B0%u52A0%u5761%27%2C%27%u59DC%u519B%27%2C%27%u8521%u548F%u4F73%27%2C%27%u6BB5%u65E5%u6674%27%2C%27%u59DC%u7F8E%u971E%27%2C%27%u8346%u84C9%u8F69%27%2C%27%u674E%u6797%u96E8%27%2C%27%u674E%u82B8%27%2C%27%u5ED6%u7F8E%u82B3%27%2C%27%u82CF%u7ECD%u82B3%27%2C%27%u738B%u5FD7%u521A%27%2C%27%u9B4F%u7389%u5CF0%27%2C%27%u6C88%u7D2B%u83B9%27%2C%27%u53F6%u7D2B%u5706%27%2C%27%u5F20%u60E0%u6167%27%2C%27%u6CE8%u518C%27'
    headers = {
        'Cookie': 'LoginNameCookie=admin; ComNumCookie=3101000001; ASP.NET_SessionId=vrmy5lqo5ce1przfya0bz25r',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def requestDetail(keyValue):
    url = "http://crm.mlnacc.com/Khgl/Consultant/Detail?"
    headers = {
        'Cookie': 'LoginNameCookie=admin; ComNumCookie=3101000001; ASP.NET_SessionId=vrmy5lqo5ce1przfya0bz25r',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    parma = {"keyValue": keyValue}
    response = requests.request("POST", url, headers=headers, params=parma)
    return response.text.encode('utf8')


def getBDict(itemTable):
    resDict = {}
    itemB = itemTable.find_all("b")
    for iB, vB in enumerate(itemB):
        bKey = vB.string.replace(':', '').replace('：', '')
        bValue = vB.next_sibling.string
        cleanStr = ''
        if bValue != None:
            tmpStr = re.compile(
                r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
            cleanStr = tmpStr.sub('', bValue)
        bDict = dict([(bKey, cleanStr)])
        resDict.update(bDict)
    return resDict


def getDetail(detailText, clueIndex, otherInfo):
    soup = BeautifulSoup(detailText, "lxml")
    itemData = [{}, [], [], []]
    clueDiv = soup.find_all('div', "div-content")
    for iDiv, vDiv in enumerate(clueDiv):
        itemTable = vDiv.find("table")
        if iDiv == 0 and itemTable != None:
            bDict = getBDict(itemTable)
            itemData[iDiv].update(bDict)
            itemData[iDiv].update(clueIndex)
            itemData[iDiv].update(otherInfo)
        elif itemTable != None:
            itemTr = itemTable.find_all("tr")
            itemDict = {}
            cellCount = 0
            for iTr, vTr in enumerate(itemTr):
                bDict = getBDict(vTr)
                if len(bDict) > 0:
                    cellCount += 1
                    bDict.update(clueIndex)
                    bDict.update(dict([('记录索引', cellCount)]))
                    itemData[iDiv].append(bDict)
    return itemData

def gen():
    clueData = []
    clueAssignCell = []
    clueFollowUpCell = []
    pages = 1
    for i in range(pages):
        page = i+1
        start = 25*i
        limit = 25
        print('requestPage\t\t', 'page:', page, 'start:', start, 'limit:', limit)
        pageText = requestPage(page, start, limit)
        textStr = (pageText.replace('totalCount', "\"totalCount\"").replace(
            'items', "\"items\"").replace('null', "\"\""))
        textDict = eval(textStr)
        for item in textDict['items']:
            GUID = item['GUID']
            clueIndex = {
                'GUID': item['GUID'],
                'ID': item['ID'],
                '客户姓名': item['ClientName'],
                '客户编号': item['ClientCode']
            }

            otherInfo = {
                '录入人员': item['CreateUser'],
                '录入时间': item['CreateDate'],
                '咨询时间': item['RegDate'],
                '客户城市': item['ClientCity']
            }
            print('requestDetail\t\t', 'page:', page, 'ID:', item['ID'])
            detailText = requestDetail(GUID)
            # time.sleep(1.25)
            itemData = getDetail(detailText, clueIndex, otherInfo)
            # if GUID == '822065A0-9A80-4796-BBED-FD595A5B68FA':
            #     print(itemData[2])
            clueData.append(itemData[0])
            clueAssignCell.append(itemData[1])
            clueFollowUpCell.append(itemData[2])
            clueFollowUpCell.append(itemData[3])

    dfCule = pd.DataFrame(list(clueData))
    dfCule.drop_duplicates(subset=['GUID'], keep='first', inplace=True)
    print('clueData to_excel......')
    dfCule.to_excel('clueData.xlsx')

    dfAssignCell = pd.DataFrame(list(itertools.chain(*clueAssignCell)))
    print('clueAssignCell to_excel......')
    dfAssignCell.to_excel('clueAssignCell.xlsx')

    dfFollowUpCell = pd.DataFrame(list(itertools.chain(*clueFollowUpCell)))
    print('clueFollowUpCell to_excel......')
    dfFollowUpCell.to_excel('clueFollowUpCell.xlsx')

gen()