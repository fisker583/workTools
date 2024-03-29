from styleframe import StyleFrame
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib as mpl
import pandas.io.formats.excel as fmt_xl
import logging
import sys
import matplotlib.pyplot as plt
import shutil
import math
import os
import json

df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=list('abc'))


def my_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    format_color = {
        'grey': "\x1b[38;20m",
        'yellow': "\x1b[33;20m",
        'red': "\x1b[31;20m",
        'bold_red': "\x1b[31;1m",
        'reset': "\x1b[0m"
    }

    formatter = logging.Formatter(
        format_color['red']+'%(asctime)s - %(name)s - %(levelname)s \n \
        %(message)s' + format_color['reset'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return (logger)


logger = my_logger()
# mode_df = pd.DataFrame({'L': []})
# df1 = pd.DataFrame(test['mode1']['levelStartCosts'])
# df2 = pd.DataFrame(test['mode1']['wildCosts'])
# df1 = df1.merge(df2, on=['L'], how='outer', sort=True)
# mode_df = mode_df.merge(df1, on=['L'], how='outer', sort=True)
# mode_df['mode'] = 'mode_df'
# logger.debug(mode_df)
# with pd.ExcelWriter('output.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='Sheet_name_1')
#     df2.to_excel(writer, sheet_name='Sheet_name_2')
# colourImg = Image.open("test.png")
# colourPixels = colourImg.convert("RGB")
# colourArray = np.array(colourPixels.getdata()).reshape(colourImg.size + (3,))
# indicesArray = np.moveaxis(np.indices(colourImg.size), 0, 2)
# allArray = np.dstack((indicesArray, colourArray)).reshape((-1, 5))


# df = pd.DataFrame(allArray, columns=["y", "x", "red", "green", "blue"])

# test = {"Streaks": [
#     {
#         "StreakList": [
#             {
#                 "StreakType": 0,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 3,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 4,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 4,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 0,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 4,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 4,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             },
#             {
#                 "StreakType": 0,
#                 "BoneProperty": {
#                     "Type": 0,
#                     "Count": 0
#                 },
#                 "StarPoints": 0
#             }
#         ]
#     }
# ]
# }


# test = [2.709, 6.5, 8.99]

# df = pd.DataFrame([test], columns=['A_' + str(i+1)
#                   for i in range(len(test))])
# df = df[['A_3', 'A_1', 'A_2']]
# # logger.debug(df)

# map_columns_names = {'A_1': 'B1', 'A_2': 'B2', 'A_3': 'B3', 'A_4': 'B4'}
# nameA = list(df.columns)


# def map_df_rename(df):
#     new_name = {}
#     for key in list(map_columns_names.keys()):
#         if key in list(df.columns):
#             new_name.update({key: map_columns_names[key]})
#     df = df.rename(columns=new_name)
#     df = df[list(new_name.keys())]
#     return (df)


# df = map_df_rename(df)
# logger.debug(df)


# x = [
#     167,
#     187,
#     207,
#     227,
#     247,
#     272,
#     297
# ]
# x = np.array(x)
# print('x is :\n', x)
# y = [
#     176,
#     196,
#     216,
#     236,
#     258,
#     283,
#     308
# ]
# y = np.array(y)
# print('y is :\n', y)
# # 用3次多项式拟合
# f1 = np.polyfit(x, y, 1)
# print('f1 is :\n', f1)

# p1 = np.poly1d(f1)
# print('p1 is :\n', p1)
# # 也可使用yvals=np.polyval(f1, x)
# yvals = p1(x)  # 拟合y值
# print('yvals is :\n', yvals)


# def genAll():
#     for (_, _, files) in os.walk('../data/xlsx'):
#         for fileName in files:
#             if (fileName[0] != '~' and fileName[-5:] == '.xlsx' and not fileName in excludeFiles):
#                 name = fileName[0:-5]
#                 gen(name)
#     # 生成Textmesh Pro 文字
#     sb = ''
#     for _, ch in enumerate(charMap.keys()):
#         sb = sb + ch
#     # open("text.txt", "wb").write(sb)


# a = {"Playfield": [
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 12,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -600.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 0,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -400.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 2,
#         "CardFace": 1,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -200.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 2,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 200.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 1,
#         "CardFace": 3,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 0.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 5,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 600.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 4,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 400.0,
#             "y": 110.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 11,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 700.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 1,
#         "CardFace": 10,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 500.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 2,
#         "CardFace": 8,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 100.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 1,
#         "CardFace": 9,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": 300.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 7,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -100.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 3,
#         "CardFace": 6,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -300.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 3,
#         "CardFace": 5,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -500.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     },
#     {
#         "UID": 0,
#         "GroupIndex": 0,
#         "Generated": 0,
#         "CardBack": 0,
#         "CardSuit": 0,
#         "CardFace": 4,
#         "CardSuit2": -1,
#         "CardFace2": -1,
#         "ExtraType": -1,
#         "AddonType": 0,
#         "NumberOfCardsToAdd": 0,
#         "FrogQuality": 1,
#         "SurpriseType": 0,
#         "SurpriseStrategy": 0,
#         "ColorCardType": 0,
#         "StackOrder": 0,
#         "NumberOfMoves": 0,
#         "CardChangerType": 0,
#         "ConnectedCardIndex": -1,
#         "RopeLengthFactor": 1.0,
#         "ShowFront": 0,
#         "Position": {
#             "x": -700.0,
#             "y": -10.0
#         },
#         "IsAllowHelpingHand": 1,
#         "HasDiceEnergy": 0,
#         "HasAlbumPackCard": 0,
#         "Gems": 0,
#         "Angle": 0.0
#     }
# ]}

# b = {"Groups": [
#     {
#         "OffsetType": -1,
#         "OffsetStart": 0,
#         "OffsetEnd": 0,
#         "GenerateOffset": 0,
#         "GenerateType": -1,
#         "DeckReplacementType": 0,
#         "GroupIndex": 0,
#         "Priority": 10,
#         "NumberOfCards": 0
#     },
#     {
#         "OffsetType": -1,
#         "OffsetStart": 0,
#         "OffsetEnd": 0,
#         "GenerateOffset": 0,
#         "GenerateType": 0,
#         "DeckReplacementType": 0,
#         "GroupIndex": 1,
#         "Priority": 0,
#         "NumberOfCards": 0
#     }
# ]}

# df = pd.json_normalize(a['Playfield'])
# print(df)


# css_style = {
#     'header': 'background-color: powderblue; color: black;font-family: Microsoft YaHei UI;',
#     'index': 'background-color: #000000; color: white;font-family: Microsoft YaHei UI;',
#     'rows': 'font-family: Microsoft YaHei UI;'
# }

# targe_df_first_row = pd.DataFrame(df.columns)
# print(targe_df_first_row)
# # write_df = pd.concat()
# write_df = df.style.apply(lambda col: np.where(
#     col.index < 3, css_style['header'], css_style['rows'])).applymap_index(lambda _: css_style['index'], axis=1)
# with pd.ExcelWriter('styled.xlsx', engine='xlsxwriter') as writer:
#     # 写入配置
#     write_df.to_excel(excel_writer=writer,
#                         sheet_name='data', index=False, startrow=1)

#     # # 写入字段描述
#     # worksheet = writer.sheets['data']
#     # for k, v in enumerate(targe_df_first_row):
#     #     worksheet.write_string(0, k, str(v))
# col_name = ['coin', 'plus5', 'undo', 'wild', 'coin_plus5', 'coin_undo']
# level_cost_start = tuple(0 for _ in range(len(col_name)))

# print(level_cost_start)

# df1 = pd.DataFrame(index=range(10), columns=['A','B','C'])
# df2 = pd.DataFrame(index=range(2), columns=['A','B','C'])
# df1.fillna(0,inplace=True)
# df2.fillna(2,inplace=True)
# logging.debug(df1)
# logging.debug(df2)

# df1.iloc[0:2,:]  = df2.iloc[0:2,:]
# logging.debug(df1)

# in_xlsx_file = 'E:/Fisker/Downloads/test.xlsx'


# def read_file(file):
#     with open('./Configs/' + file + '.json', 'r') as f:
#         logger.warning(file)
#         return eval(
#             f.read()
#             .replace('null', 'None')
#             .replace('true', 'True')
#             .replace('false', 'False')
#         )

# df = pd.read_excel(in_xlsx_file)
# data2 = eval(df['数据明细'].to_json())


# print(data2)
# data3 = json.loads(data2)
# print(data3)
# # df2 = pd.json_normalize(json.loads(data2))

a = [20,
50,
90,
150,
220,
330,
450,
600,
780,
1050
     ]

b = [i + 1 for i in range(len(a))]

print(a,b)
c = np.polyfit(b,a,2)

print(c)
