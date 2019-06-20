# encoding=utf8
#----------------------------------------------------------------------------------------------------------------------------------
import requests
import datetime
import time
import json
import copy

def mailItem(item,item_num,item_data):

	mail_item = {'Pid':'','Title':'test','Sender':'test','Content':'test',
	'Exp':'','Jewel':'','Gold':'','Chests':'','RolePieces':'','EtcItems':''}

	for v in item:
		tmp_key = str(item_data[v]['type'])
		tmp_value = str(item_data[v]['id'])
		tmp_sep = "|"

		if mail_item[tmp_key] == '':
			tmp_sep = ''

		if tmp_value == '0':
			mail_item[tmp_key] = str(item_num)
		else:
			mail_item[tmp_key] = str(mail_item[tmp_key]) + tmp_sep + tmp_value +"," + str(item_num)

	return(mail_item)

def mailSend(user_id,ip,mail_type,mail_item):
	
	time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	time2 = ' 星期' + datetime.datetime.now().strftime('%w')
	now_time = time1 + time2

	mail_item['Pid'] = user_id	
	mail_item['Title'] = now_time
	mail_item['Sender'] = now_time
	mail_item['Content'] = now_time
	
	mail_item_copy = copy.copy(mail_item)

	for v in mail_item.keys():
		if mail_item[v] == '':
			mail_item_copy.pop(v)

	# print(mail_item_copy)
	url_text = ip + mail_type + json.dumps(mail_item_copy, ensure_ascii = False)
	print(url_text)
	res = requests.get(url_text)
	# return(res.text)
#----------------------------------------------------------------------------------------------------------------------------------

user_id = 89

item = [0]
item_data = [
{'type':'Exp','id':'0'}
]

item_num = 100000

ip1 = 'http://115.159.215.154:18080'	#内部
ip2 = 'http://106.14.135.22:18080'		#外部
mail_type = "/Mail/SingleMail?"

ip = ip1

#----------------------------------------------------------------------------------------------------------------------------------
# 1		经验
# 2		钻石
# 3		金币
# 4		青铜宝箱
# 5		白银宝箱
# 6		黄金宝箱
# 7		赛季选卡宝箱
# 8		普通选卡宝箱
# 9		复活币
# 10	任务活跃度
# 11	竞技活跃度
# 13	格兰特碎片
# 14	暴君碎片
# 15	红雀碎片
# 16	深蓝碎片
# 17	尤娜碎片
# 18	黑火药碎片
# 19	EI碎片
# 20	再不斩碎片

mail_item = mailItem(item,item_num,item_data)

for i in range(1):
	mailSend(user_id,ip,mail_type,mail_item)
	time.sleep(1)
