#coding=utf-8

import itertools
import random
import xlrd

def readCardData():
	wb = xlrd.open_workbook("card.xlsx")
	card_info = wb.sheet_by_name('card')
	type_info = wb.sheet_by_name('type')

	return(card_info,type_info)

def sendCard():
	card_32 = [i+1 for i in range(32)]
	card_8 = random.sample(card_32,8)

	return(card_8)

def getCardScore(card_index):
	card_score = card_info.cell(card_index,3).value
	return(card_score)

def getCardIndex(in_card_S,in_card_P):
	card_S = card_info.col_values(1)
	card_P = card_info.col_values(2)
	card_index = None

	for i,v_card_S in enumerate(card_S):
		if in_card_S == v_card_S and in_card_P == card_P[i] :
			card_index = i
			break
		else:
			pass

	return(card_index)

def getCardP(card_index):
	card_P = card_info.cell(card_index,2).value
	return(card_P)

def getCardS(card_index):
	card_S = card_info.cell(card_index,1).value
	return(card_S)

def genScoreLave(card_8):
	sum_score = 0
	for v in card_8:
		card_score = getCardScore(v)
		sum_score += card_score

	return(sum_score % 10)

def genCardComb(card_8):
	card_3_1 = list(itertools.combinations(card_8, 3))
	card_comb = []
	isKing = True
	isLost = False

	for v_card in card_3_1:
		score_lave = genScoreLave(v_card)
		if score_lave == 0:
			isKing = False
			card_comb,isLost = genLastCard(v_card,card_8,isLost)
		else:
			pass

	return(card_comb,isKing,isLost)

def genLastCard(v_card,card_8,isLost):
	card_comb = []
	card_comb_temp = {'comb1':[],'comb2':[],'comb3':[]}
	card_5 = []
	card_5 = diffCard(v_card,card_8)
	card_5_lave = genScoreLave(card_5)
	card_2 = list(itertools.combinations(card_5, 2))

	for v_card_2 in card_2:
		card_2_lave = genScoreLave(v_card_2)

		if card_2_lave == card_5_lave:
			card_comb_temp = {'comb1':[],'comb2':[],'comb3':[]}
			card_3_2 = diffCard(v_card_2,card_5)
			card_comb_temp['comb1'] = (list(v_card_2))
			card_comb_temp['comb2'] = (list(card_3_2))
			card_comb_temp['comb3'] = (list(v_card))
			card_comb.append(card_comb_temp)
		else:
			pass

	if len(card_comb) == 0:
		isLost = True
		card_comb_temp = {'comb1':[],'comb2':[],'comb3':[]}
		card_comb_temp['comb3'] = (list(v_card))
		card_comb_temp['comb2'] = card_5[0:3]
		card_comb_temp['comb1'] = card_5[3:5]
		card_comb.append(card_comb_temp)

	return(card_comb,isLost)

def diffCard(card,card_all):
	card_last = []
	card_all_set = set(card_all)
	card_last = list(card_all_set.difference(tuple(card)))

	return(card_last)

def interCard(card1,card2):
	card1_set = set(card1)
	card3 = list(card1.intersection(tuple(card2)))

	return(card1 == card2 == card3)

def getCardType():
	pass

def genTypeIndex(card_index):
	card_S1 = type_info.cell(card_index,1).value
	card_P1 = type_info.cell(card_index,2).value
	card_S2 = type_info.cell(card_index,3).value
	card_P2 = type_info.cell(card_index,4).value
	card_type_comb = [getCardIndex(card_S1,card_P1),getCardIndex(card_S2,card_P2)]
	return(card_type_comb)

def printCardData(card_comb):
	for x in card_comb:
		for i,v in enumerate(x.values()):
			if len(v) > 0:
				for vs in v:
					print('S-',getCardS(vs),'\tP-',getCardP(vs),'\tScore-',getCardScore(vs))

def printCardKing(my_card):
	for vs in my_card:
		print('S-',getCardS(vs),'\tP-',getCardP(vs),'\tScore-',getCardScore(vs))


# *************************************************************************************
global card_info,type_info

card_info,type_info = readCardData()
my_card = sendCard()
card_comb,isKing,isLost = genCardComb(my_card)

while isLost != True:
	my_card = sendCard()
	card_comb,isKing,isLost = genCardComb(my_card)

print('my_card',my_card)
print('isKing',isKing,'isLost',isLost)
printCardData(card_comb)
# printCardKing(my_card)

# rate
sum_isKing = 0
sum_isLost = 0
sum_error = 0
sum_comb = 0
sum_count = 1000


for x in range(sum_count):
	print('sendCard',x)
	my_card = sendCard()
	card_comb,isKing,isLost = genCardComb(my_card)
	if isKing == True:
		sum_isKing += 1
	elif isLost == True:
		sum_isLost += 1
	elif isKing == True and isLost == True:
		sum_error += 1
	elif isKing == False or isLost == False:
		sum_comb += 1

print(sum_isKing/sum_count,sum_isLost/sum_count,sum_error/sum_count,sum_comb/sum_count)	


type_col = type_info.col_values(0)

for i in range(1,len(type_col)):
	tmp = genTypeIndex(i)
	tmp.sort()
	print(tmp)

global Card_Data,Card_S,Card_Score

Card_Data = [
	0x02,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,	#♦
	0x14,0x16,0x17,0x18,0x1A,							#♣
	0x22,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,	#♥
	0x33,0x34,0x36,0x37,0x38,0x3A,						#♠
	0x4F												#King	
]

Card_Score = [	
]

print(len(Card_Data))
for x in Card_Data:
	print(int(x&0xF0)/16+1,int(x&0x0F))