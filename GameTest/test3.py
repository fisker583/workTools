# _*_ coding: utf-8
import pandas as pd
import os
import csv


def csvReader(file):
    data = []
    try:
        with open(file, 'r', newline='') as cf:
            reader = csv.DictReader(cf)
            for i, rows in enumerate(reader):
                data.append(rows)
            cf.close()
    except Exception as e:
        print(file)
    return(data)


outFile = 'E:/Fisker/Downloads/rs/zh_out.xlsx'
csvFile = 'E:/Fisker/Downloads/rs/zh-Hant.csv'


data = csvReader(csvFile)
data2 = []
for i, row in enumerate(data):
    dictRow = {}
    dictRow['string'] = row['string']
    nameList = row['name'].split('.')
    for j, nameStr in enumerate(nameList):
        dictRow[str(j)] = str(nameStr)
    data2.append(dictRow)

df = pd.DataFrame(data2)
df.to_excel(outFile)
