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


def read_file(file):
    with open('./'+file + '.json', 'r') as f:
        return eval(
            f.read()
            .replace('null', 'None')
            .replace('true', 'True')
            .replace('false', 'False')
        )


def gen_farmer_pass_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for v_mode in config_data['queue'][:1]:
        mode_df = pd.json_normalize(v_mode['value']['milestones'])
        # mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        # logger.debug(config_df['packs'].explode())
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    return (config_df)


file = 'farmer_pass_milestone'

df = gen_farmer_pass_xlsx(file)
df.to_excel(f'./{file}.xlsx')
print(df)
