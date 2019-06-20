#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import random
import string

def openChrome():
	option = webdriver.FirefoxOptions()
	option.add_argument('--start-maximized')	# 窗口最大化启动
	# driver = webdriver.Chrome(chrome_options = option)
	driver = webdriver.Firefox(firefox_options = option)
	return(driver)

def getUrl(driver,url):
	driver.get(url)
	return(driver)

# element_to_be_clickable		DOM上是否存在元素并且可点击。可点击意味着enable
# visibility_of_element_located	DOM上是否存在元素并且可见。 可见性意味着元素不仅显示，而且高度和宽度也大于0.
# presence_of_element_located	DOM上是否存在元素,并不一定意味着该元素是可见的

def authlogin(driver):
	wait = WebDriverWait(driver, 5)	# 等待超时5秒
	# 清理输入账号密码
	elementName = wait.until(EC.presence_of_element_located((By.NAME,'username')))
	elementName.clear()
	elementName.send_keys('admin')
	elementPassword = wait.until(EC.presence_of_element_located((By.NAME,'password')))
	elementPassword.clear()
	elementPassword.send_keys('admin')

	# 点击提交登录
	submitXpath = '//button[contains(@type, "submit") and contains(text(), "Login")]'
	elementLogin = wait.until(EC.element_to_be_clickable((By.XPATH, submitXpath)))
	elementLogin.click()
def authSubmitMail(driver,mailDict):
	wait = WebDriverWait(driver, 5)	# 等待超时5秒

	navXpath = '//a[contains(@href, "#")]/span[contains(text(), "游戏管理工具")]'
	tabXpath = '//a[contains(@href, "/admin/game/email")]'
	createXpath = '//a[contains(@href, "/admin/game/email/create")]'
	try:
		#点击进入新建邮件
		elementCreate = wait.until(EC.visibility_of_element_located((By.XPATH,createXpath)))
		elementCreate.click()
	except Exception as e:
		#点击进入邮件页面
		elementMainNav = wait.until(EC.visibility_of_element_located((By.XPATH,navXpath)))
		elementMainNav.click()
		elementTab = wait.until(EC.visibility_of_element_located((By.XPATH, tabXpath)))
		elementTab.click()
		#点击进入新建邮件
		elementCreate = wait.until(EC.visibility_of_element_located((By.XPATH,createXpath)))
		elementCreate.click()
	
	#清理输入邮件标题
	elementTitle = wait.until(EC.visibility_of_element_located((By.ID,'e_title')))
	elementTitle.clear()
	elementTitle.send_keys(mailDict['e_title'])

	#清理输入邮件正文
	contentXpath = '//textarea[contains(@name, "e_content")]'
	elementContent = wait.until(EC.visibility_of_element_located((By.XPATH,contentXpath)))
	elementContent.clear()
	elementContent.send_keys(mailDict['e_content'])

	#选择服务器
	serverXpath = '//select[contains(@name, "e_server")]/option[contains(@value, "{}")]'.format(mailDict['e_server'])
	elementServer = wait.until(EC.presence_of_element_located((By.XPATH, serverXpath)))
	elementServer.click()

	#清理输入发件人
	acceptXpath = '//textarea[contains(@name, "e_accept")]'
	elementAccept= wait.until(EC.visibility_of_element_located((By.XPATH,acceptXpath)))
	elementAccept.clear()
	elementAccept.send_keys(mailDict['e_accept'])

	#清理输入收件人
	contentXpath = '//textarea[contains(@name, "e_content")]'
	elementContent = wait.until(EC.visibility_of_element_located((By.XPATH,contentXpath)))
	elementContent.clear()
	elementContent.send_keys(mailDict['e_content'])

	#清理输入金币、钻石、经验
	elementRGold = wait.until(EC.visibility_of_element_located((By.ID, 'r_gold')))
	elementRGold.clear()
	elementRGold.send_keys(mailDict['r_gold'])
	elementRDiamond = wait.until(EC.visibility_of_element_located((By.ID, 'r_diamond')))
	elementRDiamond.clear()
	elementRDiamond.send_keys(mailDict['r_diamond'])
	elementRExp = wait.until(EC.visibility_of_element_located((By.ID, 'r_exp')))
	elementRExp.clear()
	elementRExp.send_keys(mailDict['r_exp'])

	# 选择附件道具
	propXpath = '//select[contains(@name, "prop[]")]/option[contains(@value, "{}")]'.format(mailDict['r_prop_id'])
	elementRProp = wait.until(EC.presence_of_element_located((By.XPATH, propXpath)))
	elementRProp.click()

	# 清理输入附件道具数量
	propNumXpath = '//input[contains(@name, "prop_num[]")]'
	elementRPropNum = wait.until(EC.visibility_of_element_located((By.XPATH, propNumXpath)))
	elementRPropNum.clear()
	elementRPropNum.send_keys(mailDict['r_prop_num'])

	#点击发送邮件
	mailSubmitXpath = '//button[contains(@type, "submit") and contains(text(), "提交")]'
	elementSubmit = wait.until(EC.visibility_of_element_located((By.XPATH, mailSubmitXpath)))
	elementSubmit.click()
	#点击发送邮件
	mailSubmitXpath = '//button[contains(@type, "submit") and contains(text(), "提交")]'

def authChckMail(driver,mailTitle):
	wait = WebDriverWait(driver, 5)	# 等待超时5秒

	checkRowXpath = '//td[contains(text(), "{}")]'.format(mailTitle)
	try:
		wait.until(EC.element_to_be_clickable((By.XPATH, checkRowXpath)))
		pass
	except Exception as e:
		raise e
	print(temp)
def authRedcode(driver,codeDict):
	wait = WebDriverWait(driver, 5)	# 等待超时5秒

	navXpath = '//a[contains(@href, "#")]/span[contains(text(), "游戏管理工具")]'
	tabXpath = '//a[contains(@href, "/admin/game/redcode")]'
	createXpath = '//a[contains(@href, "/admin/game/redcode/create")]'
	try:
		#点击进入新建CDKey
		elementCreate = wait.until(EC.visibility_of_element_located((By.XPATH,createXpath)))
		elementCreate.click()
	except Exception as e:
		#点击进入CDKey页面
		elementMainNav = wait.until(EC.visibility_of_element_located((By.XPATH,navXpath)))
		elementMainNav.click()
		elementTab = wait.until(EC.visibility_of_element_located((By.XPATH, tabXpath)))
		elementTab.click()
		#点击进入新建CDKey
		elementCreate = wait.until(EC.visibility_of_element_located((By.XPATH,createXpath)))
		elementCreate.click()
		
	#清理输入CDKey批次
	elementCode = wait.until(EC.visibility_of_element_located((By.ID,'r_code')))
	elementCode.clear()
	elementCode.send_keys(codeDict['r_code'])

	#清理输入CDKey标题
	elementTitle = wait.until(EC.visibility_of_element_located((By.ID,'r_title')))
	elementTitle.clear()
	elementTitle.send_keys(codeDict['r_title'])

	#选择类型
	timesXpath = '//select[contains(@name, "r_times")]/option[contains(@value, "{}")]'.format(codeDict['r_times'])
	elementTimes = wait.until(EC.presence_of_element_located((By.XPATH, timesXpath)))
	elementTimes.click()

	#清理输入生成数量
	elementCreateNum = wait.until(EC.visibility_of_element_located((By.ID, 'create_num')))
	elementCreateNum.clear()
	elementCreateNum.send_keys(codeDict['create_num'])

	#清理输入过期时间
	elementExpiredTime = wait.until(EC.visibility_of_element_located((By.ID, 'expired_time')))
	elementExpiredTime.clear()
	elementExpiredTime.send_keys(codeDict['expired_time'])
	jsSetExpiredTimes = 'document.getElementById("expired_time").value = "{}";'.format(codeDict['expired_time'])
	driver.execute_script(jsSetExpiredTimes)

	#选择服务器
	serverXpath = '//select[contains(@name, "server_id")]/option[contains(@value, "{}")]'.format(codeDict['server_id'])
	elementServer = wait.until(EC.presence_of_element_located((By.XPATH, serverXpath)))
	elementServer.click()

	#选择渠道
	channelXpath = '//select[contains(@name, "server_channel")]/option[contains(@value, "{}")]'.format(codeDict['server_channel'])
	elementChannel = wait.until(EC.presence_of_element_located((By.XPATH, channelXpath)))
	elementChannel.click()

	#激活状态设置为激活
	statusXpath = '//input[contains(@name, "r_status")]'
	jsGetStatus = 'return(document.getElementsByName("r_status")[0].value)'
	jsSetStatus = 'document.getElementsByName("r_status")[0].value = "on";'
	curStatus = driver.execute_script(jsGetStatus)
	if curStatus == 'off':
		driver.execute_script(jsSetStatus)
		elementStatus = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'bootstrap-switch-animate')))
		elementStatus.click()

	elementRGold= wait.until(EC.visibility_of_element_located((By.ID, 'r_gold')))
	elementRGold.clear()
	elementRGold.send_keys(codeDict['r_gold'])
	elementRDiamond = wait.until(EC.visibility_of_element_located((By.ID, 'r_diamond')))
	elementRDiamond.clear()
	elementRDiamond.send_keys(codeDict['r_diamond'])
	elementRExp = wait.until(EC.visibility_of_element_located((By.ID, 'r_exp')))
	elementRExp.clear()
	elementRExp.send_keys(codeDict['r_exp'])

	# 选择附件道具
	propXpath = '//select[contains(@name, "prop[]")]/option[contains(@value, "{}")]'.format(codeDict['r_prop_id'])
	elementRProp = wait.until(EC.presence_of_element_located((By.XPATH, propXpath)))
	elementRProp.click()

	# 清理输入附件道具数量
	propNumXpath = '//input[contains(@name, "prop_num[]")]'
	elementRPropNum = wait.until(EC.visibility_of_element_located((By.XPATH, propNumXpath)))
	elementRPropNum.clear()
	elementRPropNum.send_keys(codeDict['r_prop_num'])

	#点击提交CDKey邮件
	codeSubmitXpath = '//button[contains(@type, "submit") and contains(text(), "提交")]'
	elementSubmit = wait.until(EC.visibility_of_element_located((By.XPATH, codeSubmitXpath)))
	elementSubmit.click()

def getTimeStr():
	ymd = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	week = '_星期_' + datetime.datetime.now().strftime('%w')
	timeStr = ymd + week
	return(timeStr)

def getMailDict():
	mailDict = {
		'e_title': 		getTimeStr(),
		'e_content': 	getTimeStr(),
		'e_server': 	3,
		'e_send': 		'tester',
		'e_accept': 	'',
		'r_gold': 		random.randrange(500, 5000, 100),
		'r_diamond': 	random.randrange(10, 100, 10),
		'r_exp': 		random.randrange(50, 500, 50),
		'r_prop_id':	random.randint(12, 45),
		'r_prop_num': 	random.randint(1, 10)
	}
	return(mailDict)

def getMailDictTest(testId):
	mailDict = {
		'e_title': 		getTimeStr(),
		'e_content': 	testId['itemName'] + '' + str(1),
		'e_server': 	3,
		'e_send': 		'testX',
		'e_accept': 	343,
		'r_gold': 		100,
		'r_diamond': 	10,
		'r_exp': 		5,
		'r_prop_id':	testId['itemOption'],
		'r_prop_num': 	1
	}
	return(mailDict)

def getCodeDict():
	codeDict = {
		'r_code': 		''.join(random.sample(string.ascii_uppercase, 8)),
		'r_title': 		getTimeStr(),
		'r_times': 		1,
		'create_num': 	random.randrange(5, 50, 5),
		'expired_time': '2019-12-30 00:00:00',
		'server_id': 	3,
		'server_channel': 1,
		'r_gold': 		random.randrange(500, 5000, 100),
		'r_diamond': 	random.randrange(10, 100, 10),
		'r_exp': 		random.randrange(50, 500, 50),
		'r_prop_id':	random.randint(12, 45),
		'r_prop_num': 	random.randint(1, 10)
	}
	return(codeDict)

test = [
		{'itemName':'格兰特碎片','itemOption':1},
		{'itemName':'暴君碎片','itemOption':12},
		{'itemName':'红雀碎片','itemOption':13},
		{'itemName':'深蓝碎片','itemOption':14},
		{'itemName':'尤娜碎片','itemOption':15},
		{'itemName':'黑火药碎片','itemOption':16},
		{'itemName':'艾米丽碎片','itemOption':17},
		{'itemName':'再不斩碎片','itemOption':18},
		{'itemName':'闪灵碎片','itemOption':19},
		{'itemName':'凯恩碎片','itemOption':20},
		{'itemName':'莱因哈特碎片','itemOption':21},
		{'itemName':'狂虫碎片','itemOption':22},
		{'itemName':'格兰特皮肤1','itemOption':23},
		{'itemName':'普通宝箱','itemOption':24},
		{'itemName':'大宝箱','itemOption':25},
		{'itemName':'超级宝箱','itemOption':26},
		{'itemName':'钻石宝箱','itemOption':28},
		{'itemName':'王者宝箱','itemOption':29},
		{'itemName':'赛季选卡宝箱','itemOption':30},
		{'itemName':'普通选卡宝箱','itemOption':31},
		{'itemName':'复活币','itemOption':32},
		{'itemName':'任务活跃度','itemOption':33},
		{'itemName':'格兰特','itemOption':34},
		{'itemName':'暴君','itemOption':35},
		{'itemName':'红雀','itemOption':36},
		{'itemName':'深蓝','itemOption':37},
		{'itemName':'尤娜','itemOption':38},
		{'itemName':'黑火药','itemOption':39},
		{'itemName':'艾米丽','itemOption':40},
		{'itemName':'再不斩','itemOption':41},
		{'itemName':'闪灵','itemOption':42},
		{'itemName':'凯恩','itemOption':43},
		{'itemName':'莱因哈特','itemOption':44},
		{'itemName':'狂虫','itemOption':45}
]

url = "http://106.14.186.5/admin/auth/login"
driver = openChrome()
driver = getUrl(driver,url)
authlogin(driver)
for i in range(1):
	mailDict = getMailDictTest(test[0])
	authSubmitMail(driver,mailDict)
	# codeDict = getCodeDict()
	# authRedcode(driver,codeDict)
	print('Over')
	time.sleep(2)

authChckMail(driver,'2019-04-15_17:33:24_星期_1')