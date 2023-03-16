import sys
import time
import pandas as pd
import numpy as np
from myLogger import my_logger
import logging
import xlsxwriter

logger = my_logger()
logger.setLevel(logging.DEBUG)

out_xlsx_path = 'e:/project/desigin/Data/Excels/'
test_xlsx_path = 'e:/project/desigin/Data/Test/'
in_xlsx_file = 'E:/Fisker/Documents/Solitaire Colors/Solitaire Colors数值.xlsx'


def write_xlxs(write_df, xlsx_name):
    targe_file_name = out_xlsx_path + xlsx_name + '.xlsx'
    out_file_name = test_xlsx_path + xlsx_name + '.xlsx'
    targe_df = pd.read_excel(targe_file_name, header=1)
    targe_df_first_row = pd.read_excel(targe_file_name)
    if len(write_df.columns) != len(targe_df.columns):
        logger.warning('写入字段数量不一致!')
        logger.warning(targe_df.columns)
        logger.warning(write_df.columns)
    write_df = pd.concat([targe_df[:3], write_df], ignore_index=True)
    with pd.ExcelWriter(out_file_name, engine='xlsxwriter') as writer:
        write_df.to_excel(excel_writer=writer,
                          sheet_name='data', index=False, startrow=1)

        worksheet = writer.sheets['data']

        for k, v in enumerate(targe_df_first_row):
            worksheet.write_string(0, k, str(v))


def get_design_df(xlsx_name, design_cols, design_header):
    return pd.read_excel(
        in_xlsx_file,
        sheet_name=design_data_sheet[xlsx_name],
        usecols=design_cols,
        header=design_header,
    ).dropna(how='all')


def gen_Offline_out_df(df, file_name):
    result_df = pd.DataFrame()
    result_df['Level'] = df['配置关卡'].astype('int')
    result_df['Reward'] = ('101|') + df['免费奖励'].astype('int').astype('str')
    result_df['ADReward'] = ('101|') + df['广告奖励'].astype('int').astype('str')
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_Level_out_df(df, desig_filed, target_filed, file_name):
    result_df = pd.DataFrame()
    result_df['Level'] = df[df.index %
                            3 == 0]['配置关卡'].astype('int').reset_index(drop=True)
    mode_1 = df[df.index % 3 == 0].astype('int').reset_index(drop=True)
    mode_2 = df[df.index % 3 == 1].astype('int').reset_index(drop=True)
    mode_3 = df[df.index % 3 == 2].astype('int').reset_index(drop=True)
    for i_filed, filed in enumerate(target_filed):
        mode_1_str = mode_1[desig_filed[i_filed]].astype('string')
        mode_2_str = mode_2[desig_filed[i_filed]].astype('string')
        mode_3_str = mode_3[desig_filed[i_filed]].astype('string')
        result_df[filed] = mode_1_str + '|' + mode_2_str + '|' + mode_3_str

    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def get_Turntable_reward(df, type_str):
    reward_df = pd.DataFrame()
    df_columns_arrays = [
        [str(index)[0] for index in df.columns.to_list()],
        list(range(len(df.columns.to_list()))),
    ]
    df.columns = pd.MultiIndex.from_arrays(
        df_columns_arrays, names=['reward_index', 'index'])

    for i in range(8):
        turntable_index = str(i+1)

        reward_num_df = df.xs(
            turntable_index, level='reward_index', axis=1
        ).iloc[3:]

        reward_item_df = df.xs(
            turntable_index, level='reward_index', axis=1
        ).iloc[:1]

        reward_num_col = type_str + 'RewardNum' + str(i)
        reward_item_col = type_str + 'RewardItem' + str(i)

        if len(reward_num_df.axes[1]) > 1:
            reward_num_df[reward_num_col] = (
                reward_num_df.iloc[:, 0].astype('string')
                + '|'
                + reward_num_df.iloc[:, 1].astype('string')
            )
            reward_item_df[reward_item_col] = (
                reward_item_df.iloc[:, 0].astype('string')
                + '|'
                + reward_item_df.iloc[:, 1].astype('string')
            )
        else:
            reward_num_df[reward_num_col] = (
                reward_num_df.iloc[:, 0].astype('string')
            )
            reward_item_df[reward_item_col] = (
                reward_item_df.iloc[:, 0].astype('string')
            )

        reward_item = pd.DataFrame()
        reward_item[reward_num_col] = reward_num_df[reward_num_col]
        reward_item[reward_item_col] = reward_item_df.iloc[
            0, reward_item_df.columns.get_loc(
                reward_item_col)
        ]

        reward_df = pd.concat([reward_df, reward_item], axis=1)

        reward_weight = pd.DataFrame()
    for i in range(8):
        turntable_index = str(i+1)
        reward_weight_df = df.xs(
            turntable_index, level='reward_index', axis=1
        ).iloc[1:2]
        reward_weight = pd.concat(
            [reward_weight, reward_weight_df.iloc[:, 0].astype('string')], axis=1
        )

    reward_weight_str = reward_weight.iloc[0].str.cat(sep='|')
    reward_df.insert(0, type_str + 'Weight', reward_weight_str)
    return reward_df


def gen_Turntable_out_df(df, file_name):
    result_df = pd.DataFrame()
    free_df = df.iloc[0:, 10:18]
    pay_df_1 = df.iloc[0:, 20:31]
    pay_df_2 = df.iloc[0:, 33:45]
    result_df = get_Turntable_reward(free_df, 'Free')
    pay_1_reward = get_Turntable_reward(pay_df_1, 'Pay')
    pay_2_reward = get_Turntable_reward(pay_df_2, 'Pay')

    PurchaseID = 25
    result_df.insert(0, 'PurchaseID', PurchaseID)
    result_df.insert(0, 'Level', df.iloc[3:, 5:6])
    result_df.insert(0, 'NeedPoint', df.iloc[3:, 2:3])
    result_df.reset_index(drop=True, inplace=True)

    pay_1_reward.insert(0, 'Level', df.iloc[3:, 5:6])
    pay_2_reward.insert(0, 'Level', df.iloc[3:, 5:6])
    pay_reward = pd.concat([pay_1_reward[pay_1_reward['Level'] < 168],
                           pay_2_reward[pay_2_reward['Level'] >= 168]])
    pay_reward = pay_reward.drop(['Level'], axis=1)
    pay_reward.reset_index(drop=True, inplace=True)

    result_df = pd.concat([result_df, pay_reward], axis=1)

    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_DailyGift_out_df(df, file_name):
    result_df = pd.DataFrame()
    result_df['Day'] = df.iloc[1:8, df.columns.get_loc('配置天数')]
    reward_num = df.iloc[1:8, 3:]
    reward_num[101] = (reward_num[101]*1000).astype('int')
    result_df['RewardNum'] = reward_num.apply(
        lambda row: row.dropna().astype('string').str.cat(sep='|'), axis=1)

    reward_item = df.iloc[1:8, 3:]
    reward_item[:] = np.where(reward_item.notnull(),
                              reward_item.columns, reward_item)
    result_df['RewardItem'] = reward_item.apply(
        lambda row: row.dropna().astype('string').str.cat(sep='|'), axis=1)

    result_df['Type'] = df.iloc[1:8, df.columns.get_loc('配置类型')]
    result_df['DailyName'] = 'daily_name_' + result_df['Day'].astype('string')
    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_DailyGiftMF_out_df(df, file_name):
    result_df = pd.DataFrame()
    result_df = pd.concat([result_df, df.iloc[1:, 3:]], axis=1)
    result_df.rename(columns=lambda x: 'Item' + str(x)[:-2], inplace=True)

    result_df.insert(0, 'Level', df.iloc[1:, df.columns.get_loc('配置关卡')])
    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_Shop_out_df(df, file_name):
    result_df = pd.DataFrame()
    result_df['PurchaseID'] = df.iloc[1:, df.columns.get_loc(
        '内购')].fillna(0).astype('int')
    result_df['Type'] = df.iloc[1:, df.columns.get_loc(
        '类型索引')].fillna(0).astype('int')
    result_df['ListGroup'] = df.iloc[1:,
                                     df.columns.get_loc('商品分组')].fillna(0).astype('int')
    result_df['Sort'] = df.iloc[1:, df.columns.get_loc(
        '分组排序')].fillna(0).astype('int')
    result_df['Tag'] = df.iloc[1:, df.columns.get_loc(
        '标签索引')].fillna(0).astype('int')
    result_df['ConditionValue'] = df.iloc[1:,
                                          df.columns.get_loc('前置商品索引')].fillna(0)
    result_df['Condition'] = result_df['ConditionValue'].apply(
        lambda x: 1 if x != 0 else 0)

    reward_num = df.iloc[1:, 9:]
    result_df['RewardNum'] = reward_num.apply(
        lambda row: row.dropna().astype('string').str.cat(sep='|'), axis=1)

    reward_item = df.iloc[1:, 9:]
    reward_item[:] = np.where(reward_item.notnull(),
                              reward_item.columns, reward_item)
    result_df['RewardItem'] = reward_item.apply(
        lambda row: row.dropna().astype('string').str.cat(sep='|'), axis=1)

    result_df['Icon'] = 'ui_icon_shop_' + df.iloc[1:, df.columns.get_loc(
        'icon索引')].astype('int').astype('string')

    result_df['Frequency'] = -1
    result_df['Time'] = -1
    result_df['GoodsName'] = 'Temp'
    result_df['GoodsDes'] = 'Temp'

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_ShopFactor_out_df(df, file_name):
    result_df = pd.DataFrame()
    df = df.fillna(0).astype('int').rename(columns={'去重关卡':'Level'})
    # df.rename(columns={'去重关卡':'Level'})
    result_df = df.melt(id_vars='Level', var_name='ShopID', value_name='RewardNum')
    result_df['ShopID'] = result_df['ShopID'].astype('float').astype('int')
    result_df = result_df.sort_values(by=['Level','ShopID'])

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


design_data_sheet = {

    'Offline': '离线奖励',
    'LevelCostNew': '关卡道具消耗',
    'LevelRewardNew': '关卡奖励',
    'Turntable': '转盘',
    'DailyGift': '签到',
    'DailyGiftMF': '签到',
    'Shop': '商城',
    'ShopFactor': '商城',
    # 'GiftBag2': '进度礼包',
    # 'GiftBag3': '限时礼包',
    'ItemNew': '道具定价',
    'ItemReward': '道具定价'
}

Offline_data = get_design_df('Offline', 'AA:AD', 2)
Offline_out_df = gen_Offline_out_df(Offline_data, 'Offline')


level_cost_desig_filed = ['关卡消耗.1', '回退.1', '加5张.1',
                          '万能牌.1', '开局-消三张.1', '开局-全清.1', '开局-万能牌.1']
level_cost_target_filed = ['StartCosts', 'StartCosts301', 'StartCosts302',
                           'StartCosts303', 'StartCosts201', 'StartCosts202', 'StartCosts203']
level_reward_desig_filed = ['消除基础奖励', '消除递增奖励', '余牌基础奖励', '通关基础奖励']
level_reward_target_filed = [
    'CardRewardBase', 'CardRewardAdd', 'LastCardRewardBase', 'ClearedRewardBase']

LevelCostNew_data = get_design_df('LevelCostNew', 'AA:AH', 3)
LevelCostNew_out_df = gen_Level_out_df(
    LevelCostNew_data, level_cost_desig_filed, level_cost_target_filed, 'LevelCostNew')

LevelRewardNew_data = get_design_df('LevelRewardNew', 'I:Q', 2)
LevelRewardNew_out_df = gen_Level_out_df(
    LevelRewardNew_data, level_reward_desig_filed, level_reward_target_filed, 'LevelRewardNew')

Turntable_data = get_design_df('Turntable', 'I:BA', 3)
Turntable_out_df = gen_Turntable_out_df(
    Turntable_data, 'Turntable')

DailyGift_data = get_design_df('DailyGift', 'F:R', 3)
DailyGift_out_df = gen_DailyGift_out_df(
    DailyGift_data, 'DailyGift')

DailyGiftMF_data = get_design_df('DailyGiftMF', 'U:AG', 3)
DailyGiftMF_out_df = gen_DailyGiftMF_out_df(
    DailyGiftMF_data, 'DailyGiftMF')


Shop_data = get_design_df('Shop', 'F:S', 3)
Shop_out_df = gen_Shop_out_df(
    Shop_data, 'Shop')


ShopFactor_data = get_design_df('ShopFactor', 'AA:AK', 4)
ShopFactor_out_df = gen_ShopFactor_out_df(
    ShopFactor_data, 'ShopFactor')
