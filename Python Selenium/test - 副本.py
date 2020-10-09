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
	option = webdriver.ChromeOptions()
	option.add_argument('--start-maximized')	# 窗口最大化启动
	driver = webdriver.Chrome(chrome_options = option)
	return(driver)


# element_to_be_clickable		DOM上是否存在元素并且可点击。可点击意味着enable
# visibility_of_element_located	DOM上是否存在元素并且可见。 可见性意味着元素不仅显示，而且高度和宽度也大于0.
# presence_of_element_located	DOM上是否存在元素,并不一定意味着该元素是可见的

def authlogin(driver):
	wait = WebDriverWait(driver, 15)	# 等待超时5秒
	# 清理输入账号密码
	elementName = wait.until(EC.visibility_of_element_located((By.ID,'loginname')))
	elementName.clear()
	elementName.send_keys('admin')
	elementPassword = wait.until(EC.visibility_of_element_located((By.ID,'password')))
	elementPassword.clear()
	elementPassword.send_keys('MLN123456mln')
	elementComnum = wait.until(EC.visibility_of_element_located((By.ID,'comnum')))
	elementComnum.clear()
	elementComnum.send_keys('3101000001')
	
	time.sleep(30)
	# 点击提交登录
	# submitXpath = '//button[contains(@type, "submit") and contains(text(), "Login")]'
	# elementLogin = wait.until(EC.element_to_be_clickable((By.XPATH, submitXpath)))
	# elementLogin.click()

def authClue(driver):
	wait = WebDriverWait(driver, 10)
	elementTab = wait.until(EC.presence_of_element_located((By.ID,'tool-1037')))
	elementTab.click()

	tabSubXpath = '//span[contains(text(), "客户信息")]'
	elementTabSub = wait.until(EC.visibility_of_element_located((By.XPATH, tabSubXpath)))
	elementTabSub.click()
	time.sleep(15)

	elementAllBtn = wait.until(EC.presence_of_element_located((By.ID,'button-1017')))
	elementAllBtn.click()

	# checkeXpath  = '//td/div/input[(@type, "button")]'
	# elementChecke = wait.until(EC.visibility_of_element_located((By.XPATH, checkeXpath)))
	# elementchecke.click()

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


url = "http://crm.mlnacc.com/Home/Index"
driver = openChrome()
driver.get(url)

authlogin(driver)
authClue(driver)


# authChckMail(driver,'2019-04-15_17:33:24_星期_1')