#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
import os
import json
import requests

def loadFile(harFName,harFPath):
	print('loadFile...')
	fr = open(harFPath + str(harFName), 'r+', encoding='utf-8')
	fc = eval(fr.read().replace('true','True').replace('false','False'))
	fr.close()
	jd = json.dumps(fc)
	data = json.loads(jd)
	return(data)
	
def gen(urls,data,wFPath):
	urlKey = 'url'
	if isinstance(data, list):
		for value in data:
			urls = gen(urls,value,wFPath)
	elif isinstance(data, dict):
		for key, url in data.items():
			if key == urlKey and url != None and url != '':
				# urls.append(url)
				rFPath, rFName = getPath(url)
				if rFPath != None:
					downloadFile(url,wFPath,rFPath,rFName)
			else:
				urls = gen(urls,url,wFPath)
	return urls

def getPath(url):
	strSplit = url[len('https://'):].split('/')
	rFPath = ''
	rFName = ''
	if len(strSplit) > 2:
		for v in strSplit[1:-1]:
			rFPath = rFPath + v + '/'
		rFName = strSplit[-1]
	else:
		rFPath = None
	return(rFPath,rFName)

def downloadFile(url,wFPath,rFPath,rFName):
	savePath = wFPath + rFPath
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

test = [
'https://api.leg668.com:192/statisticsHandle?s=1&agent=70000&account=70000_%E4%B9%90%E6%B8%B8VIP1005&gameId=510&type=0',
'https://csqd.leg111.com/resource/assets/hbby/hall/l_fishing_room_logo_a16289aa.png']

harFName = 'demo.leg666.com2.har'
harFPath = 'F:/Fisker/Downloads/'
wFPath = 'F:/Fisker/Downloads/leg668/'

data = loadFile(harFName,harFPath)
urls = []
urls = gen(urls,data,wFPath)
