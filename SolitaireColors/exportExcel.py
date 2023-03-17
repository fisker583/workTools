import sys
import time
import pandas as pd
import numpy as np
from myLogger import my_logger
import logging
import xlsxwriter
import math

logger = my_logger()
logger.setLevel(logging.WARNING)

out_xlsx_path = 'e:/project/desigin/Data/Excels/'
test_xlsx_path = 'e:/project/desigin/Data/Test/Excels/'
in_xlsx_file = 'E:/Fisker/Documents/Solitaire Colors/Solitaire Colors数值.xlsx'


def write_xlxs(write_df, xlsx_name):
    targe_file_name = out_xlsx_path + xlsx_name + '.xlsx'
    out_file_name = test_xlsx_path + xlsx_name + '.xlsx'
    targe_df = pd.read_excel(targe_file_name, header=1)
    targe_df_first_row = pd.read_excel(targe_file_name)
    targe_df_field = targe_df.columns.to_list()

    # 按实际配置整理配置字段
    write_df = write_df[targe_df_field]
    logger.warning(targe_df_field)
    if len(write_df.columns) != len(targe_df.columns):
        logger.warning('写入字段数量不一致!')
        logger.warning(xlsx_name)
        logger.warning(targe_df.columns)
        logger.warning(write_df.columns)
    # 合并表头
    write_df = pd.concat([targe_df[:3], write_df], ignore_index=True)
    css_alt_rows = 'background-color: powderblue; color: black;'
    css_indexes = 'background-color: steelblue; color: white;'
    write_df.style.set_table_styles([
        {'selector': 'tr:nth-child(even)', 'props': css_alt_rows},
        {'selector': 'th', 'props': css_indexes},
    ])
    with pd.ExcelWriter(out_file_name, engine='xlsxwriter') as writer:
        # 写入配置
        write_df.to_excel(excel_writer=writer,
                          sheet_name='data', index=False, startrow=1)

        # 写入字段描述
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


def gen_ItemReward_xlsx(df, file_name):
    result_df = pd.DataFrame()
    df = df.iloc[:, 4:]
    result_df = df.drop(['道具名称', '资源命名'], axis=1).melt(
        id_vars='道具id', var_name='ShopID', value_name='RewardID')
    result_df = result_df.sort_values(by=['道具id', 'RewardID'])
    result_df['ItemName'] = 'item.name.' + result_df['道具id'].astype('str')
    result_df['ItemDes'] = 'item.des.' + result_df['道具id'].astype('str')

    item_icon_data = get_design_df('ItemIcon', 'B:AA', 3)
    item_icon_data = item_icon_data.iloc[:, 4:]
    item_icon_df = item_icon_data.drop(['道具名称', '资源命名'], axis=1).melt(
        id_vars='道具id', var_name='ShopID', value_name='RewardID')

    result_df['ItemIcon'] = item_icon_df['RewardID']
    result_df = result_df.rename(
        columns={'道具id': 'ItemType', 'RewardID': 'ID'})

    reward_default = result_df.drop(index=result_df.index)
    reward_default['ItemType'] = df['道具id']
    reward_default['ID'] = reward_default['ItemType']
    reward_default['ItemName'] = 'item.name.' + \
        reward_default['ItemType'].astype('str')

    # 默认同itemID的itemRewardID
    reward_default['ItemDes'] = 'item.des.' + \
        reward_default['ItemType'].astype('str')
    reward_default['ItemIcon'] = 'icon_' + df['资源命名']+'_Medium'

    result_df = pd.concat([reward_default, result_df])
    logger.debug(reward_default)

    result_df.reset_index(drop=True, inplace=True)
    logger.debug(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def get_config_id(file_name):
    return ((config_df['配置索引'][config_df['配置名称'] == file_name]).astype('int').to_list()[0])


def gen_ItemNew_xlsx(df, file_name):
    result_df = pd.DataFrame()
    result_df['ID'] = df['道具id']
    result_df['ItemType'] = df['类型']
    result_df['ItemName'] = 'item.name.' + result_df['ID'].astype('str')
    result_df['ItemDes'] = 'item.des.' + result_df['ID'].astype('str')
    result_df.reset_index(drop=True, inplace=True)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_Offline_xlsx(df, file_name):
    result_df = pd.DataFrame()
    result_df['Level'] = df['配置关卡'].astype('int')
    result_df['Reward'] = ('101|') + df['免费奖励'].astype('int').astype('str')
    result_df['ADReward'] = ('101|') + df['广告奖励'].astype('int').astype('str')
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_Level_xlsx(df, desig_filed, target_filed, file_name):
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
    logger.debug(result_df)
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
        config_id = get_config_id('Turntable')
        if len(reward_num_df.axes[1]) > 1:
            reward_num_df[reward_num_col] = (
                reward_num_df.iloc[:, 0].astype('string')
                + '|'
                + reward_num_df.iloc[:, 1].astype('string')
            )
            reward_item_df[reward_item_col] = (
                (reward_item_df.iloc[:, 0]*100+config_id).astype('string')
                + '|'
                + (reward_item_df.iloc[:, 1]*100+config_id).astype('string')
            )
        else:
            reward_num_df[reward_num_col] = (
                (reward_num_df.iloc[:, 0]).astype('string')
            )
            reward_item_df[reward_item_col] = (
                (reward_item_df.iloc[:, 0]*100+config_id).astype('string')
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


def gen_Turntable_xlsx(df, file_name):
    result_df = pd.DataFrame()
    free_df = df.iloc[0:, 10:18]
    pay_df_1 = df.iloc[0:, 20:31]
    pay_df_2 = df.iloc[0:, 33:45]
    result_df = get_Turntable_reward(free_df, 'Free')
    pay_1_reward = get_Turntable_reward(pay_df_1, 'Pay')
    pay_2_reward = get_Turntable_reward(pay_df_2, 'Pay')

    PurchaseID = 11
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
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_DailyGift_xlsx(df, file_name):
    result_df = pd.DataFrame()
    config_id = get_config_id(file_name)
    reward_tmp = df.iloc[1:8, 3:]
    reward_tmp.iloc[:, 0] = (reward_tmp.iloc[:, 0]*1000).astype('int')
    result_df = get_reward_df(result_df, reward_tmp, config_id)
    result_df['Day'] = df.iloc[1:8, df.columns.get_loc('配置天数')]
    result_df['Type'] = df.iloc[1:8, df.columns.get_loc('配置类型')]
    result_df['DailyName'] = 'daily_name_' + result_df['Day'].astype('string')
    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_DailyGiftMF_xlsx(df, file_name):
    result_df = pd.DataFrame()
    result_df = pd.concat([result_df, df.iloc[1:, 3:]], axis=1)
    config_id = get_config_id('DailyGift')
    result_df.rename(columns=lambda x: 'Item' + str(x)
                     [:-2] + '0' + str(config_id), inplace=True)

    result_df.insert(0, 'Level', df.iloc[1:, df.columns.get_loc('配置关卡')])
    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_Shop_xlsx(df, file_name):
    result_df = pd.DataFrame()
    config_id = get_config_id(file_name)
    result_df = get_reward_df(result_df, df.iloc[1:, 9:], config_id)
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

    result_df['Icon'] = 'icon_shop_' + df.iloc[1:, df.columns.get_loc(
        'icon索引')].astype('int').astype('string')

    result_df['Frequency'] = -1
    result_df['Time'] = -1
    result_df['GoodsName'] = 'Temp'
    result_df['GoodsDes'] = 'Temp'

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_ShopFactor_xlsx(df, file_name):
    result_df = pd.DataFrame()
    df = df.fillna(0).astype('int').rename(columns={'去重关卡': 'Level'})
    result_df = df.melt(id_vars='Level', var_name='ShopID',
                        value_name='RewardNum')
    result_df['ShopID'] = result_df['ShopID'].astype('float').astype('int')
    result_df = result_df.sort_values(by=['Level', 'ShopID'])

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_Purchase_xlsx(df, file_name):
    result_df = pd.DataFrame()
    result_df['ID'] = df['内购id']
    result_df['Price'] = (round(df['内购价格'].astype('float')*100)).astype('int')
    result_df['ProductID'] = 'goods.' + result_df['ID'].astype('str')
    result_df['PurchaseName'] = 'goods.name.' + result_df['ID'].astype('str')

    result_df.reset_index(drop=True, inplace=True)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def get_reward_df(reward_df, df, config_id):
    reward_num = df
    reward_df['RewardNum'] = reward_num.apply(
        lambda row: row.dropna().astype('string').str.cat(sep='|'), axis=1)
    reward_item = df
    reward_item.columns = [
        int(float(column))*100 + config_id for column in reward_item.columns]
    reward_item[:] = np.where(reward_item.notnull(),
                              reward_item.columns, reward_item)
    reward_df['RewardItem'] = reward_item.apply(
        lambda row: row.dropna().astype('int').astype('string').str.cat(sep='|'), axis=1)
    return (reward_df)


def gen_GiftBag_xlsx(gif_bag_level, gif_bag_time, file_name):
    result_df = pd.DataFrame()

    gif_bag_level_free_data = gif_bag_level.iloc[2:, :13]
    gif_bag_level_free_df = pd.DataFrame()
    config_id = get_config_id('GiftBag2')
    gif_bag_level_free_df = get_reward_df(
        gif_bag_level_free_df, gif_bag_level_free_data.iloc[0:, 4:], config_id)
    gif_bag_level_free_df['PurchaseID'] = 0
    gif_bag_level_free_df['Condition1'] = 1
    gif_bag_level_free_df['ConditionValue1'] = gif_bag_level_free_data['配置关卡']
    gif_bag_level_free_df['Type'] = 3
    gif_bag_level_free_df['Sort'] = 1

    gif_bag_level_pay_data = gif_bag_level.iloc[2:, 15:]
    gif_bag_level_PurchaseID = 12
    gif_bag_level_pay_df = pd.DataFrame()
    config_id = get_config_id('GiftBag2')
    gif_bag_level_pay_df = get_reward_df(
        gif_bag_level_pay_df, gif_bag_level_pay_data.iloc[0:, 0:], config_id)
    gif_bag_level_pay_df['PurchaseID'] = gif_bag_level_PurchaseID
    gif_bag_level_pay_df['Condition1'] = 1
    gif_bag_level_pay_df['ConditionValue1'] = gif_bag_level_free_data['配置关卡']
    gif_bag_level_pay_df['Type'] = 3
    gif_bag_level_pay_df['Sort'] = 2

    gif_bag_level_df = pd.concat([gif_bag_level_free_df, gif_bag_level_pay_df])
    gif_bag_level_df['Discount'] = 0
    gif_bag_level_df = gif_bag_level_df.sort_values(
        by=['ConditionValue1', 'Sort'])

    gif_bag_time_pay_data = gif_bag_time.iloc[2:, 4:]
    gif_bag_time_PurchaseID = 13
    gif_bag_time_pay_df = pd.DataFrame()
    config_id = get_config_id('GiftBag3')
    gif_bag_time_pay_df = get_reward_df(
        gif_bag_time_pay_df, gif_bag_time_pay_data.iloc[0:, 0:], config_id)
    gif_bag_time_pay_df['PurchaseID'] = gif_bag_time_PurchaseID
    gif_bag_time_pay_df['Condition1'] = 1
    gif_bag_time_pay_df['ConditionValue1'] = gif_bag_time['配置关卡']
    gif_bag_time_pay_df['Type'] = 2
    gif_bag_time_pay_df['Sort'] = 1
    gif_bag_time_pay_df['Discount'] = gif_bag_time['配置原始金币'].fillna(
        0).astype('int')

    result_df = pd.concat([gif_bag_level_df, gif_bag_time_pay_df])
    result_df['Frequency'] = 1
    result_df['Time'] = 86400
    result_df['Condition2'] = -1
    result_df['ConditionValue2'] = -1
    result_df['OriginalPrice'] = 0
    result_df['GiftName'] = 'Temp'
    result_df['GiftDes'] = 'Temp'

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    result_df['Group'] = result_df.apply(
        lambda row: math.floor((row.ID-1)/(row.Type-1))+1, axis=1)
    logger.warning(file_name)
    logger.debug(result_df)
    write_xlxs(result_df, file_name)


def gen_FunctionOpen_xlsx(df, file_name):
    result_df = pd.DataFrame()
    result_df['Name'] = df['功能名称']
    result_df['OpenLevel'] = df['开启关卡'].astype('int')
    result_df['OpenLoginDays'] = df['开启限制天数'].astype('int')
    result_df['OpenRewardItem'] = df['道具奖励'].fillna(0).astype('int')
    result_df['OpenRewardItemNum'] = df['奖励数量'].fillna(0).astype('int')

    result_df.reset_index(drop=True, inplace=True)
    result_df.insert(0, 'ID', result_df.index+1)
    logger.warning(file_name)
    logger.debug(result_df)
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
    'GiftBag2': '进度礼包',
    'GiftBag3': '限时礼包',
    'ItemNew': '道具定价',
    'ItemReward': '道具资源',
    'ItemIcon': '道具图标',
    'Purchase': '内购',
    'FunctionOpen': '功能开启'
}

level_cost_desig_filed = ['关卡消耗.1', '回退.1', '加5张.1',
                          '万能牌.1', '开局-消三张.1', '开局-全清.1', '开局-万能牌.1']
level_cost_target_filed = ['StartCosts', 'StartCosts301', 'StartCosts302',
                           'StartCosts303', 'StartCosts201', 'StartCosts202', 'StartCosts203']
level_reward_desig_filed = ['消除基础奖励', '消除递增奖励', '余牌基础奖励', '通关基础奖励', '废弃配置']
level_reward_target_filed = [
    'CardRewardBase', 'CardRewardAdd', 'LastCardRewardBase', 'ClearedRewardBase', 'ClearedRewardMF']

config_df = get_design_df('ItemReward', 'B:C', 3)

gen_ItemReward_xlsx(get_design_df('ItemReward', 'B:AA', 3), 'ItemReward')


gen_ItemNew_xlsx(get_design_df('ItemNew', 'C:E', 3), 'ItemNew')
gen_Offline_xlsx(get_design_df('Offline', 'AA:AD', 2), 'Offline')

gen_Level_xlsx(get_design_df('LevelCostNew', 'AA:AH', 3),
               level_cost_desig_filed, level_cost_target_filed, 'LevelCostNew')

gen_Level_xlsx(get_design_df('LevelRewardNew', 'I:R', 2),
               level_reward_desig_filed, level_reward_target_filed, 'LevelRewardNew')

gen_Turntable_xlsx(get_design_df('Turntable', 'I:BA', 3), 'Turntable')

gen_DailyGift_xlsx(get_design_df('DailyGift', 'F:R', 3), 'DailyGift')

gen_DailyGiftMF_xlsx(get_design_df('DailyGiftMF', 'U:AG', 3), 'DailyGiftMF')

gen_Shop_xlsx(get_design_df('Shop', 'F:S', 3), 'Shop')

gen_ShopFactor_xlsx(get_design_df('ShopFactor', 'AA:AK', 4), 'ShopFactor')

gen_Purchase_xlsx(get_design_df('Purchase', 'C:J', 3), 'Purchase')

gen_GiftBag_xlsx(get_design_df('GiftBag2', 'K:AD', 4),
                 get_design_df('GiftBag3', 'K:S', 4), 'GiftBag')

gen_FunctionOpen_xlsx(get_design_df('FunctionOpen', 'C:J', 3), 'FunctionOpen')
