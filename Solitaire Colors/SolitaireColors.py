import pandas as pd
import os
import json
import sys
# with open('./Solitaire Colors/MapConfig_1.json', 'r') as f:
#     data = eval(f.read())


def get_level(lis, val):
    # minimum_difference is used to check the difference between value in list and key we have and it will keep record of minimum difference
    minimum_difference = sys.maxsize
    # nearest_value will save the list value for which we got minimum difference

    nearest_value = None
    # iterating through the list elements
    for i in lis:
        # getting the difference b/w key value and list element
        difference_key_element = val - i
        # checking if difference is neagtive or not, if negative make
        # it positive
        if difference_key_element < 0:
            difference_key_element *= -1
        # checking if minimum value we find so far, is less then the
        # current difference b/w key value and element value
        # if it is less then the current min value, replace it
        # and store the list element in the store variable
        if difference_key_element < minimum_difference:
            minimum_difference = difference_key_element
            nearest_value = i
    # return the store variable
    return nearest_value


file_name = './Solitaire Colors/Solitaire Colors.xlsx'

level_data = pd.read_excel(open(file_name, 'rb'),
                           sheet_name='关卡消耗奖励')

day_level_round = 20
day_offline_count = 1
ini_coin = 20000
days = [i+1 for i in range(10)]

out_dict = {'level': 0, 'coin_start': 0, 'coin_end': 0}

cur_coin = ini_coin
cur_level = 0

get_level(level_data[])