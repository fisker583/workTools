import pandas as pd
from myLogger import my_logger
import logging
import numpy as np
from DesignConfig import Config

logger = my_logger()
logger.setLevel(logging.WARNING)


# class DataTest():
#     def __init__(self, level):
#         self.level = level
#         self.ini_res = pd.DataFrame(['coin', 'plus5', 'undo'])

    # def get_current_res(self, df, change_type=0, change_val=0):
    #     col_name = ['coin', 'plus5', 'undo']
    #     result_df = pd.DataFrame(columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)

    # def get_level_play(self, df, modeVal=1, change_val=0):
    #     col_name = ['win_times', 'fail_times', 'win_percent']
    #     row_prefix = 'by_plus5_'
    #     result_df = pd.DataFrame(columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)

    # def get_level_cost(self, df, modeVal=1, change_val=0):
    #     col_name = ['coin', 'plus5', 'undo', 'coin_plus5', 'coin_undo']
    #     row_name = ['start', 'win']
    #     result_df = pd.DataFrame(index=row_name, columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)

    # def get_sys_reward(self, df, day=1):
    #     col_name = ['coin', 'plus5', 'undo']
    #     row_name = ['start', 'win']
    #     result_df = pd.DataFrame(index=row_name, columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)

    # def get_change_after_res(self, df, change_type=0, change_val=0):
    #     col_name = ['coin', 'plus5', 'undo']
    #     result_df = pd.DataFrame(columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)

    # def get_current_level(self, df, day=1, change_val=0):
    #     col_name = ['coin', 'plus5', 'undo']
    #     result_df = pd.DataFrame(columns=col_name)
    #     result_df.fillna(0, inplace=True)
    #     return (result_df)


# level_test = DataTest(100)
config = Config()
ini_res = config.reward_default_by_res()

col_name = ['win_times', 'fail_times', 'win_percent','plus5_count']
row_prefix = 'by_plus5_'
level_play = pd.DataFrame(
    [(3, 2, round(1/3, 2),1)], columns=col_name)
logging.warning(level_play)


col_name = ['coin', 'plus5', 'undo', 'coin_plus5', 'coin_undo']
row_name = ['start', 'win']
level_cost = pd.DataFrame(index=row_name, columns=col_name)
logging.warning(level_cost)

level_cost_start =config.cost_level_by_level_mode(25,1)
level_cost_start.rename(index={0: 'start'},inplace=True)
logging.warning(level_cost_start)


current_res = config.reward_default_by_res()
logging.warning(current_res)
