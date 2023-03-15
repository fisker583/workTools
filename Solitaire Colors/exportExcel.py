import sys
import time
import pandas as pd
import exportField
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
        write_df.to_excel(excel_writer=writer, sheet_name='data',
                          index=False, startrow=1)

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
    logger.warning(result_df)
    write_xlxs(result_df, file_name)


def gen_Turntable_out_df(df, file_name):
    result_df = pd.DataFrame()
    free_df = df.iloc[0:, 10:18]
    pay_df_1 = df.iloc[0:, 20:31]
    pay_df_2 = df.iloc[0:, 33:45]
    logger.warning(free_df)
    logger.warning(pay_df_1)
    logger.warning(pay_df_2)
    pay_df_2_arrays = [[index[0] for index in pay_df_2.columns.to_list()], [
        index[2] for index in pay_df_2.columns.to_list()]]
    pay_df_2.columns = pd.MultiIndex.from_arrays(
        pay_df_2_arrays, names=['pos', 'pos_index'])
    reward_num_tmp = pay_df_2.xs('1', level='pos', axis=1).iloc[2:]
    reward_num_tmp['PayRewardNum'] = (
        reward_num_tmp.iloc[:, 0].astype('string')
        + '|'
        + reward_num_tmp.iloc[:, 1].astype('string')
    )
    reward_item_tmp = pay_df_2.xs('8', level='pos', axis=1).iloc[:1]
    reward_item_tmp['PayRewardNum'] = (
        reward_item_tmp.iloc[:, 0].astype('string')
        + '|'
        + reward_item_tmp.iloc[:, 1].astype('string')
    )
    logger.warning(reward_num_tmp)
    logger.warning(reward_item_tmp)
    # logger.warning(pay_df_2)


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
