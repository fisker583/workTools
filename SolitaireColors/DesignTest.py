import pandas as pd
from myLogger import my_logger
import logging
import numpy as np
from DesignConfig import Config

logger = my_logger()
logger.setLevel
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
ini_res = config.reward_default_by_item()

level_play_columns = ['win_round', 'fail_round', 'win_percent', 'plus5_count']
level_play = pd.DataFrame(index=range(1), columns=level_play_columns)
level_play.fillna(0, inplace=True)

items_columns = ['coin', 'plus5', 'undo', 'wild']

level_cost_start = pd.DataFrame(index=range(1), columns=items_columns)
level_cost_win = pd.DataFrame(index=range(1), columns=items_columns)
current_item = pd.DataFrame(index=range(1), columns=items_columns)
after_item = pd.DataFrame(index=range(1), columns=items_columns)
level_cost_start.fillna(0, inplace=True)
level_cost_win.fillna(0, inplace=True)
current_item.fillna(0, inplace=True)
after_item.fillna(0, inplace=True)

level_cost_config = config.cost_level_by_level_mode(25, 1)

logging.debug(level_cost_win)
