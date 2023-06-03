import pandas as pd
import numpy as np
import os
import wget


df_db = pd.read_excel('./hans/OcrmReceiptEntity.xlsx')

df = df_db[(df_db['receiptType'] == 2) & (df_db['attachFiles'].notna())]

file_list = df['attachFiles'].to_list()
file_list_new = []
for files in file_list:
    url_list = files.split('https')
    url_list_new = []
    for url in url_list:
        if len(url) > 0 and url[-1] == ',':
            url_list_new.append(url[:-1])
        elif len(url) > 0:
            url_list_new.append(url)
    file_list_new.append(url_list_new)

    if not url_list_new:
        print("NOT OK" + '_'*20)


root = './hans/out/'
customName = df['customName'].to_list()
companyName = df['companyName'].to_list()
voyagesName = df['voyagesName'].to_list()
shipName = df['shipName'].to_list()

df['path'] = (root + df['customName'] + '/' + df['companyName'] +
              '/' + df['voyagesName'] + '/' + df['shipName'])
path_list = df['path'].to_list()

if len(file_list_new) != len(path_list):
    print("path NOT OK" + '_'*20)

for i, path in enumerate(path_list):
    if not os.path.exists(path):
        os.makedirs(path)
        for file in file_list_new[i]:
            url = 'https' + file
            names = file.split('/')
            name = path + '/' + names[-1]
            print(name)
            wget.download(url, name)
