# _*_ coding: utf-8
import xlsxwriter
import os
import datetime
import time
import re
import csv
import shutil
from PIL import Image

def csvReader():
	filePath = 'F:/Fisker/Downloads/'
	fileName = '未命名.csv'
	csvFile = filePath + fileName
	data = []
	try:
		with open(csvFile,'r',newline='') as cf:
			reader = csv.DictReader(cf)
			for i,rows in enumerate(reader):
				data.append(rows)
			cf.close()
	except Exception as e:
		os.startfile(filePath)
	return(data)
def wsStyle(style):
	styles = {
		'text': {'font_size': 10,'align': 'left','valign': 'top','text_wrap': 1,'font_name': '微软雅黑'},
		'fileUrl': {'font_size': 10,'font_color':'#0c60e1','bold':1,'align': 'left','valign': 'top','text_wrap': 1,'font_name': '微软雅黑','underline':1},
		'imageTitle': {'font_size': 10,'align': 'left','valign': 'top','bold':1,'text_wrap': 1,'font_name': '微软雅黑'},
		'imageUrl': {'font_size': 16,'font_color':'#1a73e8','align': 'right','valign': 'vcenter','text_wrap': 1,'bold':1,'font_name': '微软雅黑','underline':1},
		'filed': {'font_size': 10,'font_color':'#333333','align': 'left','valign': 'top','bold':1,'text_wrap': 1,'bg_color': '#f2f2f2','bottom': 1,'font_name': '微软雅黑'},
		'totalBottom': {'font_size': 10,'font_color':'#333333','align': 'left','valign': 'top','bold':1,'text_wrap': 1,'bg_color': '#f2f2f2','top': 1,'font_name': '微软雅黑'},
		'totalTop': {'font_size': 10,'font_color':'#333333','align': 'left','valign': 'top','bold':1,'text_wrap': 1,'bg_color': '#f2f2f2','bottom': 1,'font_name': '微软雅黑'}
	}
	return(styles[style])
def getTotalData(keys,data):
	res = []
	for key in keys:
		for i, v in enumerate(data):
			if key in v.keys():
				res.append(v[key])
	return(res)
def setCount(keys,data):
	res = {}
	for key in keys:
		if key == '严重程度':
			res = severityData()
	for i in set(data):
		res[i] = data.count(i)
	return(res)
def severityData():
	res = {'S':0, 'A':0, 'B':0, 'C':0}
	return(res)
def setSort(data):
	if severityData().keys() != data.keys():
		res = sorted(data.items(), key = lambda item:item[1],reverse=True)
	else:
		res = list(zip(data.keys(),data.values()))
	return(res)
def insertRow(data, keys):
	sumVal = 0
	for v in data:
		sumVal += v[1]
	rowEnd = ('总计',sumVal )
	data.append(rowEnd)

	rowStart = tuple(keys)
	data.insert(0,rowStart)
	return(data)
def setWidth(ws, field):
	offset = 0
	for i, v in enumerate(field):
		if i > 0:
			offset += len(field[i-1]) + 1 
		for j, k in enumerate(v.values()):
			col = j + offset
			ws.set_column(col, col, int(k))
def formatStr(key, value):
	if value == None or not(isinstance(value, str)):
		value = ''
	else:
		value = re.sub(r'\s+', '\n', value)
		value = re.sub(r'^\s+|\s+$', '', value)
	if key == 'Bug编号':
		value = int(value)
	return(value)
def getImage(value):
	path = 'F:/Fisker/Pictures/bug/'
	images = []
	strSplit = value.split('\n')
	for vSplit in strSplit:
		if len(vSplit) > 0:
			image = path + vSplit
			images.append(image)
	return(images)
def getScale(image):
	imageS,imageH = 1,None
	maxW,maxH = 640, 450
	if image != None:
		try:
			with open(image) as cf:
				cf.close()
		except Exception as e:
			image = 'F:/Fisker/Pictures/bug/temp.png'
		imageW,imageH = Image.open(image).size
		if  imageW> maxW:
			imageS = maxW/imageW
		elif imageH > maxH:
			imageS = maxH/imageH
		imageH = ((imageH * imageS)*0.75)
		return(imageS,imageH)
def copyImage(bugId,image):
	path = 'F:/Fisker/Pictures/Bug_zentao/'
	try:
		fileName = os.path.basename(image)
		fileName = 'SH_' + str(bugId) + '_' + fileName
		shutil.copyfile(image,path+fileName)
	except Exception as e:
		print(bugId,e)
class TotalWriter:
	"""docstring for TotalWriter"""
	def __init__(self, fieldDict,csvData):
		self.records = []
		for field in fieldDict:
			data = getTotalData(field.keys(), csvData)
			record = setCount(field.keys(), data)
			record = setSort(record)
			record = insertRow(record, field.keys())
			self.records.append(record)
	def write(self, wb, ws, fieldDict):
		setWidth(ws, fieldDict)
		offset = 0
		for i, record in enumerate(self.records):
			if i > 0:
				offset += len(self.records[i-1][0]) + 1
			for j, rows in enumerate(record):
				for k, v in enumerate(rows):
					row, col = j, k + offset
					style = 'text'
					if row == 0:
						style = 'totalTop'
					elif row == len(record) -1:
						style = 'totalBottom'
					ws.write(row, col, v, wb.add_format(wsStyle(style)))
class BugWriter:
	"""docstring for BugWriter"""
	def write(self, csvData, wb, wsBug, wsImage, bugFiled, imageFiled):
		setWidth(wsBug, bugFiled)
		for col, key in enumerate(bugFiled[0].keys()):
			wsBug.write(0, col, key, wb.add_format(wsStyle('totalTop'))) 
		setWidth(wsImage, imageFiled)
		for col, key in enumerate(imageFiled[0].keys()):
			wsImage.write(0, col, key, wb.add_format(wsStyle('totalTop')))
		rowImage = 0
		for i, rows in enumerate(csvData):
			rows['Bug标题'] = '【SH】'+ str(rows['Bug编号']) + '-' + rows['Bug标题']
			rows['重现步骤'] = rows['Bug标题'] + '\n' +rows['重现步骤']
			print(rows['Bug标题'])
			for j, key in enumerate(bugFiled[0].keys()):
				bugStr = formatStr(key,rows[key])
				row, col = i + 1, j
				wsBug.write(row, col, bugStr,wb.add_format(wsStyle('text')))
				if key == '附件' and bugStr != '':
					fileUrl = 'internal:' + '截图!B' + str(rowImage + 2)
					wsBug.write_url(row, col, fileUrl, wb.add_format(wsStyle('fileUrl')),string='截图')
					images = getImage(bugStr)
					for r, image in enumerate(images):
						# copyImage(rows['Bug编号'],image)
						rowImage += 1
						scale,hight = getScale(image)
						wsImage.set_row(rowImage, hight, wb.add_format(wsStyle('imageTitle')))
						wsImage.insert_image(rowImage, 1, image, {'x_scale': scale, 'y_scale': scale})
						wsImage.write(rowImage, 0, rows['Bug标题'] + '\n截图_' + str(r) ,wb.add_format(wsStyle('imageTitle')))
						bugUrl = 'internal:' + 'Bug!F' + str(i+2)
						wsImage.write_url(rowImage,1, bugUrl, wb.add_format(wsStyle('imageUrl')),string='查看Bug')
class BugXLsx:
	"""docstring for BugXLsx"""
	def __init__(self):
		date = datetime.datetime.now().strftime('%Y%m%d')
		self.path = 'F:/Fisker/Documents/《无限激战》/1.测试文档/Dev2/'
		self.file = self.path + '《无限激战》测试信息-' + date + '.xlsx'
	def gen(self):
		ws = {}
		wsDict = {
			'bug':'Bug',
			'image':'截图',
			'total':'统计'
		}
		fieldDict = {
			'bug': [{'Bug编号':8,'影响版本':8,'所属模块':12,'严重程度':8,'Bug标题':35,'重现步骤':70,'Bug状态':8,'附件':8}],
			'image':[{'Bug标题':35,'Bug截图':102}],
			'total': [{'所属模块': 15, '计数': 8},{'严重程度': 15, '计数': 8},{'Bug状态': 15, '计数': 8}]
		}
		wb = xlsxwriter.Workbook(self.file)
		for v in wsDict.items():
			ws.update(dict([(v[0],wb.add_worksheet(v[1]))]))
		csvData = csvReader()
		total = TotalWriter(fieldDict['total'], csvData)
		total.write(wb, ws['total'], fieldDict['total'])
		bug = BugWriter()
		bug.write(csvData, wb, ws['bug'], ws['image'], fieldDict['bug'], fieldDict['image'])
		print('wb.close()...')
		wb.close()
		# os.startfile(self.path)
		os.startfile(self.file)
test = BugXLsx()
test.gen()