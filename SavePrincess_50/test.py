# _*_ coding: utf-8
import os
import xlsxwriter
from PIL import Image
import json
from dict2xml import dict2xml as xmlify
import collections
def getDialog(dialog,data):
	Dialogues = {'speaker':'','sentence':''}
	# mapData
	if isinstance(data, list):
		for value in data:
			dialog = getDialog(dialog,value)
	elif isinstance(data, dict):
		for key, value in data.items():
			if key in dialogues.keys():
				dialog.append(value)
			dialog = getDialog(dialog,value)
	return dialog

def getMapData(fileName,filePath):
	fileName = str(fileName)
	fr = open(filePath + fileName + '.file', 'r+', encoding='utf-8')
	fileContent = eval(fr.read().replace('true','True').replace('false','False'))
	fr.close()
	jsonTemp = json.dumps(fileContent)
	mapData = json.loads(jsonTemp)
	return(mapData)

def writeEventText(imageData,mapData,elementTypes):
	for iMapData,vMapData in enumerate(mapData['mapData']):
		if len(vMapData) > 0:
			posX = int(iMapData / MAPWIDTH) + 1
			posY = int(iMapData % MAPWIDTH) + 1
			# vMapData.update(dict([('posIndex',iMapData +1)]))
			# vMapData.update(dict([('posX',posX +1)]))
			# vMapData.update(dict([('posY',posY +1)]))
			# vMapData.update(dict([('floor',floor)]))
			# elementTypes = getElementInfo(vMapData['element'],imageData,elementTypes)
	return(elementTypes)
def getElementInfo(elementImage,imageData,elementTypes):
	elementName = None
	elementType = None
	for v in imageData['image']:
		if v['name'] == elementImage and v['type'] not in elementTypes:
			elementTypes.append(v['type'])
			break
	return(elementTypes)

def genAll():
	global MAPCOUNT,MAPWIDTH,MAPHIGHT
	filePath = './map/'
	imagePath = './image/'
	imageData = getMapData('resources',imagePath)
	elementTypes = []
	for i in range(MAPCOUNT):
		mapDialog = []
		mapData = getMapData(i,filePath)
		# jsonData = writeEventText(imageData,mapData,elementTypes)
		mapDialog = getMapDialog(i,mapData,mapDialog)
	# for mapkey in mapDialog:
	# 	print(mapkey)
	print(elementTypes)
MAPCOUNT = 51
MAPWIDTH = 11
MAPHIGHT = 11

genAll()
