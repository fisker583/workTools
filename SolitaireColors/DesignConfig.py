import pandas as pd
import numpy as np
# from myLogger import my_logger
# import logging

# logger = my_logger()
# logger.setlevel(logging.CRITICAL)

in_xlsx_file = 'E:/github/workTools/SolitaireColors/Excel/SolitaireColors数值.xlsx'


def design_data(xlsx_name, design_cols, design_header):
    return pd.read_excel(
        in_xlsx_file,
        sheet_name=design_data_sheet[xlsx_name],
        usecols=design_cols,
        header=design_header,
    ).dropna(how='all')


design_data_sheet = {
    'Offline': '离线奖励',
    'levelCostNew': '关卡道具消耗',
    'levelRewardNew': '关卡奖励',
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
    'levelRewardFirst': '关卡进度奖励',
    'levelWinRate': '验算胜率'
}


def item_data(df):
    result_df = pd.DataFrame()
    # 道具数据
    result_df['ID'] = df['道具id']
    result_df['ItemType'] = df['类型']
    result_df['ItemName'] = df['道具名称']
    result_df.reset_index(drop=True, inplace=True)
    return (result_df)


def reward_offline(df):
    result_df = pd.DataFrame()
    # 转盘奖励数据
    result_df['level'] = df['配置关卡'].astype('int')
    result_df['coin'] = df['免费奖励'].astype('int')
    return (reward_clean(result_df))


def reward_level(df):
    result_df = pd.DataFrame()

    # 关卡奖励数据
    level_reward_desig_filed = ['消除基础奖励', '消除递增奖励', '余牌基础奖励', '通关基础奖励', '废弃配置']
    level_reward_target_filed = [
        'CardRewardBase', 'CardRewardAdd', 'LastCardRewardBase', 'ClearedRewardBase', 'ClearedRewardMF']
    for i_filed, filed in enumerate(level_reward_target_filed):
        result_df[filed] = df[level_reward_desig_filed[i_filed]]
    result_df.reset_index(drop=True, inplace=True)
    result_df['mode'] = result_df.index
    result_df['mode'] = (result_df['mode'] % 3) + 1
    return (result_df)


def cost_level(df):
    result_df = pd.DataFrame()

    # 关卡消耗数据
    level_cost_desig_filed = ['配置关卡', '关卡消耗.1', '回退.1',
                              '加5张.1', '万能牌.1', '开局-消三张.1', '开局-全清.1', '开局-万能牌.1']
    level_cost_target_filed = ['level', '101',
                               '301', '302', '303', '201', '202', '203']
    for i_filed, filed in enumerate(level_cost_target_filed):
        result_df[filed] = df[level_cost_desig_filed[i_filed]]
    result_df.reset_index(drop=True, inplace=True)
    result_df = reward_clean(result_df)
    result_df['mode'] = result_df.index
    result_df['mode'] = (result_df['mode'] % 3) + 1
    return (result_df)


def reward_daily(df):
    result_df = pd.DataFrame()

    # 签到基础奖励
    result_df = df.iloc[1:8, 3:]
    result_df['day'] = df.iloc[1:8, df.columns.get_loc('配置天数')].astype('int')
    result_df.iloc[:, 0] = (result_df.iloc[:, 0]*1000).astype('int')
    return (reward_clean(result_df))


def reward_daily_mf(df):
    result_df = pd.DataFrame()

    # 签到奖励系数
    result_df = pd.concat([result_df, df.iloc[1:, 3:]], axis=1)
    result_df.rename(columns=lambda x: str(x)[:-2], inplace=True)
    result_df.insert(0, 'level', df.iloc[1:, df.columns.get_loc('配置关卡')])
    return (reward_clean(result_df))


def all_level_rate_data(df):
    result_df = pd.DataFrame()

    # 关卡通关数据
    result_df = df
    result_df.rename(columns={'配置关卡': 'level'}, inplace=True)
    return (reward_clean(result_df))


def reward_level_first(level_data):
    result_df = pd.DataFrame()

    # 首次通关奖励
    result_df = level_data.iloc[1:,].dropna(
        axis=1, how='all')
    result_df.drop(result_df.iloc[:, 1:5], axis=1, inplace=True)
    result_df.rename(columns={'配置关卡': 'level'}, inplace=True)
    return (reward_clean(result_df))


def reward_level_gift(gif_bag_level):
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
    result_df['level'] = gif_bag_level.iloc[2:, 0]

    return (reward_clean(result_df))


def reward_default(df):
    result_df = pd.DataFrame()
    result_df = df.iloc[[1]].dropna(axis=1, how='any')

    return (reward_clean(result_df))


def reward_wheel(df):
    result_df = pd.DataFrame()

    # 关卡通关数据
    result_df = df.iloc[3:, 3:5]
    result_df.columns = ['sum_val', 'val']
    return reward_clean(result_df)


def reward_wheel_mf(df):
    return round(df.iat[0, 0], 2)


def reward_concat(df):
    col_names = ['coin', 'plus5', 'undo','wild']
    result = pd.DataFrame(columns=col_names)
    result = pd.concat([result, df])
    if result.empty == True:
        result = pd.DataFrame([(0, 0, 0)], columns=col_names)
    result = result[col_names].fillna(0).reset_index(drop=True)
    return (result)


def reward_clean(df):
    df.fillna(0, inplace=True)
    df.rename(columns=lambda x: str(x), inplace=True)
    df.rename(columns={'101': 'coin', '302': 'plus5',
              '301':  'undo', '303':  'wild'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return (df)


class Config():
    def __init__(self, *args):
        self._item_data = item_data(design_data('ItemNew', 'C:F', 4))
        self._reward_offline = reward_offline(
            design_data('Offline', 'P:R', 4))
        self._cost_level = cost_level(
            design_data('levelCostNew', 'AA:AH', 4))
        self._reward_level = reward_level(
            design_data('levelRewardNew', 'I:R', 4))
        self._reward_daily = reward_daily(
            design_data('DailyGift', 'F:R', 4))
        self._reward_daily_mf = reward_daily_mf(
            design_data('DailyGiftMF', 'U:AG', 4))
        self._level_rate = all_level_rate_data(
            design_data('levelWinRate', 'D:I', 4))
        self._reward_level_first = reward_level_first(
            design_data('levelRewardFirst', 'D:AA', 4))
        self._reward_gift_level = reward_level_gift(
            design_data('GiftBag2', 'K:AD', 4))
        self._reward_default = reward_default(
            design_data('DefaultPlayerItem', 'D:AA', 4))
        self._reward_wheel = reward_wheel(
            design_data('Turntable', 'I:BG', 4))
        self._reward_wheel_mf = reward_wheel_mf(
            design_data('Turntable', 'C:C', 24))

    def reward_offline_by_level(self, level):
        # 按关卡离线奖励
        reward = self._reward_offline[self._reward_offline['level'] <= level].tail(
            1)
        return (reward_concat(reward))

    def cost_level_by_level_mode(self, level, mode):
        # 按关卡、模式关卡消耗
        reward = self._cost_level[(self._cost_level['level'] <= level) & (
            self._cost_level['mode'] == mode)].tail(1)
        return (reward_concat(reward))

    def reward_daily_by_level_day(self, level, day):
        # 按关卡、天签到奖励
        reward = self._reward_daily[self._reward_daily['day'] == day].tail(
            1)
        reward_mf = self._reward_daily_mf.loc[(
            self._reward_daily_mf['level'] <= level), 'coin'].iat[-1]
        reward['coin'] = int(reward['coin'] * reward_mf)
        return (reward_concat(reward))

    def reward_level_first_by_level(self, level):
        # 按关卡首次通关奖励
        reward = self._reward_level_first[self._reward_level_first['level'] == level].tail(
            1)
        return (reward_concat(reward))

    def reward_gift_level_by_level(self, level):
        # 按关卡进度礼包
        reward = self._reward_gift_level[self._reward_gift_level['level'] == level].tail(
            1)
        return (reward_concat(reward))

    def reward_wheel_by_val(self, val):
        # 按进度值 转盘奖励系数
        reward = self._reward_wheel[self._reward_wheel['sum_val'] <= val].tail(
            1)
        reward['mf'] = self._reward_wheel_mf
        return (reward)

    def reward_default_by_item(self):
        # 按资源 初始资源
        return (reward_concat(self._reward_default))
