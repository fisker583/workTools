# _*_ coding: utf-8
import os
import xlsxwriter
from PIL import Image
import json
from dict2xml import dict2xml as xmlify
import collections

def getStyle(styleType):
	sheetText = {'font_size': 10,'align': 'left','valign': 'top','text_wrap': 1,'font_name': '微软雅黑'}
	sheetFilesUrl = {'font_size': 10,'font_color':'#0c60e1','bold':1,'align': 'left','valign': 'top','text_wrap': 1,'font_name': '微软雅黑','underline':1}
	sheetImageText = {'font_size': 10,'align': 'left','valign': 'top','bold':1,'text_wrap': 1,'font_name': '微软雅黑'}
	sheetRuler = {'font_size': 10,'font_color':'#888888','align': 'center','valign': 'center','text_wrap': 1,'font_name': '微软雅黑'}
	sheetRulerTitle = {'font_size': 10,'font_color':'#333333','bold':1,'align': 'center','valign': 'center','text_wrap': 1,'bg_color': '#d8d8d8','bottom': 0,'font_name': '微软雅黑'}
	styles = {'sheetText': sheetText,'sheetImageText': sheetImageText,'sheetRuler': sheetRuler,'sheetFilesUrl': sheetFilesUrl,'sheetRulerTitle':sheetRulerTitle}
	return(styles[styleType])

def getFileData(fileName,filePath):
	fr = open(filePath + str(fileName) + '.file', 'r+', encoding='utf-8')
	fileContent = eval(fr.read().replace('true','True').replace('false','False'))
	fr.close()
	jsonTemp = json.dumps(fileContent)
	mapData = json.loads(jsonTemp)
	return(mapData)
def setws():
	global MAPCOUNT,MAPWIDTH,MAPHIGHT
	global infoColumns,dialogColumns
	wb = xlsxwriter.Workbook('./SavePrincessMap.xlsx')
	ws = collections.OrderedDict()
	ws.update(dict([('all',wb.add_worksheet('all'))]))
	for i, v in enumerate(dialogColumnsAll.keys()):
		ws['all'].write(0, dialogColumnsAll[v][1], dialogColumnsAll[v][0], wb.add_format(getStyle('sheetRulerTitle')))
		ws['all'].set_column(dialogColumnsAll[v][1], dialogColumnsAll[v][1], dialogColumnsAll[v][2])
	for iHight in range(MAPHIGHT + 1 + 200):
		ws['all'].set_row(iHight, 32*0.75, wb.add_format())
		
	for iMap in range(MAPCOUNT):
		print('图层...',iMap,'\n')
		workSheetName = str(iMap)
		ws.update(dict([(iMap,wb.add_worksheet(workSheetName))]))
		ws[iMap].set_column(0,MAPWIDTH + 1,3.38)
		for iHight in range(MAPHIGHT + 1 + 50):
			ws[iMap].set_row(iHight, 32*0.75, wb.add_format())
		for iColumn in range(MAPHIGHT + 1):
			ws[iMap].write(iColumn, 0, iColumn,wb.add_format(getStyle('sheetRulerTitle')))
		for iRow in range(MAPWIDTH + 1):
			ws[iMap].write(0, iRow, iRow,wb.add_format(getStyle('sheetRulerTitle')))
		for iColumn in range(MAPHIGHT):
			for iRow in range(MAPWIDTH):
				ws[iMap].write(iColumn + 1, iRow + 1, (iColumn + 1) * (iRow + 1),wb.add_format(getStyle('sheetRuler')))
		for i, v in enumerate(infoColumns.keys()):
			ws[iMap].write(0, infoColumns[v][1], infoColumns[v][0], wb.add_format(getStyle('sheetRulerTitle')))
			ws[iMap].set_column(infoColumns[v][1], infoColumns[v][1], infoColumns[v][2])
		for i, v in enumerate(dialogColumns.keys()):
			ws[iMap].write(0, dialogColumns[v][1], dialogColumns[v][0], wb.add_format(getStyle('sheetRulerTitle')))
			ws[iMap].set_column(dialogColumns[v][1], dialogColumns[v][1], dialogColumns[v][2])

	return(wb,ws)

def insertImageFloor(ws,mapData):
	for i, _ in enumerate(mapData['mapData']):
		cellRow = int(i / MAPWIDTH) + 1
		cellCol = int(i % MAPWIDTH) + 1
		imageFloor  = './saveImage/' + 'floor' + '_0.png'
		print('地板...',i,cellRow,cellCol,imageFloor,'\n')
		ws.insert_image(cellRow, cellCol, imageFloor)
def insertImageElement(ws,mapData):
	for i,v in enumerate(mapData['mapData']):
		cellRow = int(i / MAPWIDTH) + 1
		cellCol = int(i % MAPWIDTH) + 1
		element  = v['element']
		if element != '' and element != None:
			imageElement = './saveImage/' + element + '_0.png'
			print('地图...',i,cellRow,cellCol,imageElement,'\n')
			ws.insert_image(cellRow, cellCol, imageElement)
def getEventContent(mapData):
	elementKey = {'element'}
	allKeys = set(mapData.keys())
	diffKey = list(allKeys.difference({'element'}))
	eventContent = collections.OrderedDict()
	if len(diffKey) > 0:
		for i,v in enumerate(diffKey):
			eventContent.update(dict([(v,mapData[v])]))
	return(eventContent)
def writeEventText(ws,mapData):
	textRow = 1
	textCol = 15
	for iMapData,vMapData in enumerate(mapData['mapData']):
		eventContent = getEventContent(vMapData)
		if len(eventContent) > 0:
			print(eventContent)

def insertElementInfo(wb,ws,mapData,imageData):
	global infoColumns
	elements = []
	for i, v in enumerate(mapData['mapData']):
		element  = v['element']
		if element != '' and element != None and element not in elements:
			elements.append(element)

	for i, v in enumerate(elements):
		elementImage = './saveImage/' + v + '_0.png'
		elementName,elementType = getElementInfo(v,imageData)
		print('图例...',i,elementImage,elementName,elementType,'\n')
		ws.insert_image(i+ 1, infoColumns['elementImage'][1] , elementImage)
		ws.write(i+ 1, infoColumns['elementKey'][1], v, wb.add_format(getStyle('sheetText')))
		ws.write(i+ 1, infoColumns['elementType'][1], elementType, wb.add_format(getStyle('sheetText')))
		ws.write(i+ 1, infoColumns['elementName'][1], elementName, wb.add_format(getStyle('sheetText')))
def getElementInfo(elementImage,imageData):
	elementName = None
	elementType = None
	typeName = {
		'stairUp':'楼梯',
		'goods':'道具',
		'enemy':'怪物',
		'wall':'墙壁',
		'door':'门',
		'stairDown':'楼梯',
		'npc':'NPC',
		'stair':'楼梯'
	}
	for v in imageData['image']:
		if v['name'] == elementImage:
			elementType = typeName[v['type']]
			if 'property' in v.keys():
				if 'name'in v['property'].keys() :
					elementName = v['property']['name']
				elif 'message'in v['property'].keys() and v['type'] == 'goods':
					elementName = v['property']['message'].replace('获得','')
				elif 'dialogue'in v['property'].keys() and v['type'] == 'goods':
					elementName = v['property']['dialogue'].replace('获得','')
	return(elementName,elementType)
def getDialog(dialog,data):
	dialogues = {'speaker':'','sentence':''}
	dialoguesKey = 'dialogues'
	# mapData
	if isinstance(data, list):
		for value in data:
			dialog = getDialog(dialog,value)
	elif isinstance(data, dict):
		for key, value in data.items():
			if key == dialoguesKey :
				dialog.append(value)
			else:
				dialog = getDialog(dialog,value)
	return dialog
def insertElementDialog(wb,ws,mapData,floor,allDialogs):
	global dialogColumns
	for i,v in enumerate(mapData['mapData']):
		posX = int(i / MAPWIDTH) + 1
		posY = int(i % MAPWIDTH) + 1
		dialogs = []
		dialogs = getDialog(dialogs,v)
		if len(dialogs) > 0:
			for iDialogs,vDialogs in enumerate(dialogs):
				for iDialog,vDialog in enumerate(vDialogs):
					speakerImage = './saveImage/' + vDialog['speaker'] + '_0.png'
					speakerPos = 'X_Y：' + str(posX) + '_' + str(posY)
					speakerName = vDialog['speaker']
					dialogText = vDialog['sentence']
					cellRow = iDialogs + iDialog + 1
					dialogsTmp = {} 
					dialogsTmp.update(dict([('speakerImage',speakerImage)]))
					dialogsTmp.update(dict([('speakerFloor',floor)]))
					dialogsTmp.update(dict([('speakerPos',speakerPos)]))
					dialogsTmp.update(dict([('speakerName',speakerName)]))
					dialogsTmp.update(dict([('dialogText',dialogText)]))
					allDialogs.append(dialogsTmp)

					print('对话...',i,iDialogs,iDialog,speakerImage,vDialog,'\n')
					ws.insert_image(iDialogs + iDialog +1, dialogColumns['speakerImage'][1] , speakerImage)
					ws.write(cellRow, dialogColumns['speakerPos'][1], speakerPos, wb.add_format(getStyle('sheetText')))
					ws.write(cellRow, dialogColumns['speakerName'][1], speakerName, wb.add_format(getStyle('sheetText')))
					ws.write(cellRow, dialogColumns['dialogText'][1], dialogText, wb.add_format(getStyle('sheetText')))
	return (allDialogs)
def insertAllDialog(wb,ws,allDialogs):
	global dialogColumnsAll
	for i,v in enumerate(allDialogs):
		if len(v) > 0:
			print('所有对话...',i,v,'\n')
			cellRow = i + 1
			ws.insert_image(cellRow, dialogColumnsAll['speakerImage'][1],v['speakerImage'])
			ws.write(cellRow, dialogColumnsAll['speakerFloor'][1], v['speakerFloor'], wb.add_format(getStyle('sheetText')))
			ws.write(cellRow, dialogColumnsAll['speakerPos'][1], v['speakerPos'], wb.add_format(getStyle('sheetText')))
			ws.write(cellRow, dialogColumnsAll['speakerName'][1], v['speakerName'], wb.add_format(getStyle('sheetText')))
			ws.write(cellRow, dialogColumnsAll['dialogText'][1], v['dialogText'], wb.add_format(getStyle('sheetText')))
def genAll():
	global MAPCOUNT,MAPWIDTH,MAPHIGHT
	imagePath = './image/'
	imageData = getFileData('resources',imagePath)
	mapFilePath = './map/'
	wb,ws = setws()
	allDialogs = []

	for i in range(MAPCOUNT):
		mapData = getFileData(i,mapFilePath)
		insertImageFloor(ws[i],mapData)
		insertImageElement(ws[i],mapData)
		insertElementInfo(wb,ws[i],mapData,imageData)
		insertElementDialog(wb,ws[i],mapData,i,allDialogs)
	
	insertAllDialog(wb,ws['all'],allDialogs)
	print('wb.close().........')
	wb.close()

MAPCOUNT = 51
MAPWIDTH = 11
MAPHIGHT = 11
infoColumns =  {
		'elementImage':['物件图片',MAPWIDTH + 2, 3.5*2], 
		'elementType':['物件类型',MAPWIDTH + 3, 3.5*2], 
		'elementKey': ['物件Key',MAPWIDTH + 4, 3.5*5],
		'elementName':['物件名称',MAPWIDTH + 5, 3.5*15]
		}
dialogColumns =  {
		'speakerImage':['发言NPC',MAPWIDTH + 7, 3.5*2], 
		'speakerPos': ['NPC位置',MAPWIDTH + 8, 3.5*4],
		'speakerName':['NPCKey',MAPWIDTH + 9, 3.5*4], 
		'dialogText':['发言文字',MAPWIDTH + 10, 3.5*20]
		}
dialogColumnsAll =  {
		'speakerImage':['发言NPC',0, 3.5*2],
		'speakerFloor': ['NPC地图',1, 3.5*2], 
		'speakerPos': ['NPC位置',2, 3.5*4],
		'speakerName':['NPCKey',3, 3.5*4], 
		'dialogText':['发言文字',4, 3.5*30]
		}
genAll()