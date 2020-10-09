#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup
import re


def loadFile(harFName, harFPath):
    with open(harFPath + harFName, 'r', encoding='utf8') as f:
        return(f.read())


def requestPage():
    url = "https://f1022.wonderfulday27.live/viewthread.php?tid=392662&extra=page%3D1%26amp%3Bfilter%3Ddigest"
    payload = {}
    headers = {
        'Cookie': '__cfduid=d5b2f707186a9bc35c114ecb5b3aca7661602162501; CzG_sid=YxYy5c; CzG_oldtopics=D392662D; CzG_visitedfid=19; CzG_fid19=1602163111'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def downloadFile(url, wFPath, rFName):
    savePath = wFPath
    saveFile = savePath + rFName
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    try:
        print('download' + '\t' + url)
        rF = requests.get(url)
        with open(saveFile, "wb") as f:
            print('save' + '\t' + saveFile)
            f.write(rF.content)
    except Exception as e:
        pass


harFName = 'Detail.html'
harFPath = 'E:/Git/workTools/ml/'
wFPath = 'E:/Fisker/Downloads/leg668/'

test = requestPage()
print(test)
# data = loadFile(harFName, harFPath)
# soup = BeautifulSoup(data, "lxml")
# clueDiv = soup.find_all('img', onmouseover=re.compile('showMenu'))
# for i, v in enumerate(clueDiv):
#     fileUrl = v.get('file')
#     fileName = str(i)+'.gif'
#     print(fileUrl)
#     # downloadFile(fileUrl, wFPath, fileName)
