#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
import os
import json
import pandas as pd

clueDict ={
	"ClientAddress",
	"ClientCity",
	"ClientCode",
	"ClientFax",
	"ClientHttp",
	"ClientMail",
	"ClientMan",
	"ClientName",
	"ClientSource",
	"ClientTel",
	"ClientType",
	"ClientZip",
	"ComNum",
	"CommStatus",
	"ContactType",
	"CreateDate",
	"CreateUser",
	"Credit",
	"DelFlag",
	"GUID",
	"ID",
	"IndustryCode",
	"InviteType",
	"IsPoint",
	"IsTrans",
	"IsVisit",
	"L1",
	"L2",
	"L3",
	"L4",
	"L5",
	"L11",
	"Latitude",
	"LegalPerson",
	"LinkerList",
	"Longitude",
	"Manager",
	"Mobile",
	"ProtectTerm",
	"ProtectTime",
	"Province",
	"QQ",
	"RegCapital",
	"RegDate",
	"Remark",
	"Report",
	"ShareUser",
	"Status",
	"SubInfo",
	"VisitNum",
	"WeChat"
}

def loadFile(harFName,harFPath):
	print('loadFile...')
	fr = open(harFPath + str(harFName), 'r+', encoding='utf-8')
	fc = eval(fr.read().replace('null',"None").replace('false',"False").replace('true',"True"))
	fr.close()
	jd = json.dumps(fc)
	data = json.loads(jd)
	return(data)

harFName = 'crm.mlnacc.com6.har'
harFPath = 'e:/Fisker/Downloads/'

data = loadFile(harFName,harFPath)
harList = "entries/response/content/text/items"
clueData = []
entries = data['log']['entries']
for i, v in enumerate(entries):
	if isinstance(v, dict) and v.get('response') != None:
		# print(i)
		textCon = v['response']['content']['text']
		pre  = textCon.replace('totalCount',"\"totalCount\"").replace('items',"\"items\"").replace('None',"\"None\"")
		if (pre[2:12]) == "totalCount":
			print(i,pre[2:12])
			preJson =  json.loads(pre)
			items = preJson['items']
			clueData = clueData +items



df = pd.DataFrame(list(clueData), columns=clueDict)
df.drop_duplicates(subset=['GUID'],keep='first',inplace=True)
print('to_excel......')
df.to_excel('clueData.xlsx')