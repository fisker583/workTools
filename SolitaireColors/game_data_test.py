import pandas as pd
import numpy as np
from myLogger import my_logger
import logging
import sys
import os
import numpy as np

out_xlsx_path = 'e:/project/desigin/Data/Excels/'
test_xlsx_path = 'e:/project/desigin/Data/Test/Excels/'
in_xlsx_file = 'E:/Fisker/Documents/Solitaire Colors/Solitaire Colors数值.xlsx'


def get_design_df(xlsx_name, design_cols, design_header):
    return pd.read_excel(
        in_xlsx_file,
        sheet_name=design_data_sheet[xlsx_name],
        usecols=design_cols,
        header=design_header,
    ).dropna(how='all')


design_data_sheet = {
    'Offline': '离线奖励',
    'LevelCostNew': '关卡道具消耗',
    'LevelRewardNew': '关卡奖励',
    'Turntable': '转盘',
    'DailyGift': '签到',
    'DailyGiftMF': '签到',
    'Shop': '商城',
    'ShopFactor': '商城',
    'GiftBag2': '进度礼包',
    'GiftBag3': '限时礼包',
    'ItemNew': '道具定价',
    'ItemReward': '道具资源',
    'ItemIcon': '道具图标',
    'Purchase': '内购',
    'FunctionOpen': '功能开启',
    'DefaultPlayerItem': '初始资源',
    'TutorialsReward': '功能开启奖励',
    'LevelRewardFirst': '关卡进度奖励',
    'LevelWinRate': '验算胜率'
}
logger = my_logger()
logger.setLevel(logging.WARNING)


def all_item(df, file_name):
    result_df = pd.DataFrame()
    result_df['ID'] = df['道具id']
    result_df['ItemType'] = df['类型']
    result_df['ItemName'] = df['道具名称']
    result_df.reset_index(drop=True, inplace=True)
    logger.debug(file_name)
    logger.debug(result_df)


def all_offline(df, file_name):
    result_df = pd.DataFrame()
    result_df['Level'] = df['配置关卡'].astype('int')
    result_df['Reward'] = df['免费奖励'].astype('int').astype('str')
    result_df['ADReward'] = df['广告奖励'].astype('int').astype('str')

    logger.debug(file_name)
    logger.debug(result_df)
    return (result_df)


def all_level(df, desig_filed, target_filed, file_name):
    result_df = pd.DataFrame()
    # result_df['Level'] = df['配置关卡'].astype('int')
    for i_filed, filed in enumerate(target_filed):
        result_df[filed] = df[desig_filed[i_filed]]

    result_df.reset_index(drop=True, inplace=True)
    result_df['mode'] = result_df.index
    result_df['mode'] = (result_df['mode'] % 3) + 1
    logger.debug(file_name)
    logger.debug(result_df)

    return (result_df)


def all_daily(df, file_name):
    result_df = pd.DataFrame()
    result_df = df.iloc[1:8, 3:]
    result_df['Day'] = df.iloc[1:8, df.columns.get_loc('配置天数')]
    result_df.iloc[:, 0] = (result_df.iloc[:, 0]*1000).astype('int')
    result_df.fillna(0, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    logger.debug(file_name)
    logger.debug(result_df)

    return (result_df)


def all_daily_mf(df, file_name):
    result_df = pd.DataFrame()
    result_df = pd.concat([result_df, df.iloc[1:, 3:]], axis=1)
    result_df.rename(columns=lambda x: str(x)[:-2], inplace=True)
    result_df.insert(0, 'Level', df.iloc[1:, df.columns.get_loc('配置关卡')])
    result_df.reset_index(drop=True, inplace=True)
    logger.debug(file_name)
    logger.debug(result_df)
    return (result_df)


def all_level_rate_data(df, file_name):
    result_df = pd.DataFrame()
    result_df = df
    result_df.rename(columns={'配置关卡': 'Level'}, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    logger.debug(file_name)
    logger.debug(result_df)
    return (result_df)


def all_level_first(level_data, file_name):
    result_df = pd.DataFrame()
    result_df = level_data.iloc[1:,].dropna(
        axis=1, how='all')
    result_df.drop(result_df.iloc[:, 1:5], axis=1, inplace=True)
    result_df.rename(columns={'配置关卡': 'Level'}, inplace=True)
    result_df.fillna(0, inplace=True)
    result_df.reset_index(drop=True, inplace=True)

    logger.debug(file_name)
    logger.debug(result_df)
    return (result_df)


def all_gift_level(gif_bag_level, file_name):
    result_df = pd.DataFrame()

    # 免费进度礼包
    gif_bag_level_free_data_1 = gif_bag_level.iloc[2:, 4:7].rename(
        columns=lambda x: str(x)[:3]).dropna(how='all')
    gif_bag_level_free_data_2 = gif_bag_level.iloc[2:, 7:10].rename(
        columns=lambda x: str(x)[:3]).dropna(how='all')
    gif_bag_level_free_data_3 = gif_bag_level.iloc[2:, 10:13].rename(
        columns=lambda x: str(x)[:3]).dropna(how='all')
    result_df = pd.concat(
        [gif_bag_level_free_data_1, gif_bag_level_free_data_2])
    result_df = pd.concat([result_df, gif_bag_level_free_data_3])
    result_df['Level'] = gif_bag_level.iloc[2:, 0]
    result_df.fillna(0, inplace=True)
    result_df.sort_index(inplace=True)

    logger.debug(file_name)
    logger.debug(result_df)
    return (result_df)


def get_reward_offline(level):
    return int(offline_df.loc[(offline_df['Level'] <= level), 'Reward'].iat[-1])


def get_cost_level(level, mode, item):
    return int(level_cost_df.loc[(level_cost_df['Level'] <= level) & (level_cost_df['mode'] == mode), str(item)].iat[-1])


def get_reward_daily(level, day):
    base = daily_df.loc[(daily_df['Day'] == day), 101].iat[-1]
    mf = dailyMF_df.loc[(dailyMF_df['Level'] <= level), str(101)].iat[-1]
    return int(base*mf)


def get_reward_level_first(level):
    result = level_reward_first.loc[(
        level_reward_first['Level'] == level), 101]
    return (0 if len(result) == 0 else int(result))


def get_reward_gift_level(level):
    result = gift_level_df.loc[(
        gift_level_df['Level'] == level), '101']
    return (0 if len(result) == 0 else int(result))


def get_reward_gift_level(level):
    result = gift_level_df.loc[(
        gift_level_df['Level'] == level), '101']
    return (0 if len(result) == 0 else int(result))


def get_level_rate(level, type):
    return float(level_rate_df.loc[(level_rate_df['Level'] == level), str(type)])


all_item(get_design_df('ItemNew', 'C:F', 3), 'ItemNew')
offline_df = all_offline(get_design_df('Offline', 'AA:AD', 2), 'Offline')
level_cost_desig_filed = ['配置关卡', '关卡消耗.1', '回退.1',
                          '加5张.1', '万能牌.1', '开局-消三张.1', '开局-全清.1', '开局-万能牌.1']
level_cost_target_filed = ['Level', '101',
                           '301', '302', '303', '201', '202', '203']
level_reward_desig_filed = ['配置关卡', '消除基础奖励',
                            '消除递增奖励', '余牌基础奖励', '通关基础奖励', '废弃配置']
level_reward_target_filed = ['Level', 'CardRewardBase', 'CardRewardAdd',
                             'LastCardRewardBase', 'ClearedRewardBase', 'ClearedRewardMF']
level_cost_df = all_level(get_design_df('LevelCostNew', 'AA:AH', 3),
                          level_cost_desig_filed, level_cost_target_filed, 'LevelCostNew')
level_reward_df = all_level(get_design_df('LevelRewardNew', 'I:R', 2),
                            level_reward_desig_filed, level_reward_target_filed, 'LevelRewardNew')
daily_df = all_daily(
    get_design_df('DailyGift', 'F:R', 3), 'DailyGift')
dailyMF_df = all_daily_mf(get_design_df(
    'DailyGiftMF', 'U:AG', 3), 'DailyGiftMF')
level_rate_df = all_level_rate_data(get_design_df(
    'LevelWinRate', 'D:M', 3), 'LevelWinRate')

level_reward_first = all_level_first(get_design_df(
    'LevelRewardFirst', 'D:AA', 4), 'LevelRewardFirst')

gift_level_df = all_gift_level(get_design_df('GiftBag2', 'K:AD', 4), 'GiftBag')


class Level():
    def __init__(self, level, mode, item, day, rate_type):
        self.id = level
        self.cost = get_cost_level(level, mode, str(item))
        self.rate = get_level_rate(level, str(rate_type))
        self.reward_win_mf = 1.25
        self.reward_fail_mf = 0.24
        self.reward_win = round(self.reward_win_mf * self.cost)
        self.reward_fail = round(self.reward_fail_mf * self.cost)
        self.reward_daily = get_reward_daily(level, day)
        self.reward_gift = get_reward_gift_level(level)


level_id = 100
level_mode = 1
day = 1
rete = 'base'

ini_coin = 10000
level_end = 200
level = Level(level_id, level_mode, 101, day, rete)

# out_columns = {
#     '关卡',
#     '时间_天',
#     '通关率',
#     '消耗_挑战',
#     '消耗_通关',
#     '奖励_通关',
#     '奖励_失败',
#     '余额_通关前',
#     '余额_通关后',
#     '损耗_通关',
#     '奖励_离线',
#     '余额_离线',
#     '奖励_免费转盘',
#     '余额_免费转盘',
#     '奖励_签到',
#     '余额_签到'
# }

level_series,day,level_rate,cost_level,cost_level_win,reward_win,reward_fail,surplus_level_start,surplus_level_win,loss_level,= []
