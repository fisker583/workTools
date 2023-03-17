import pandas as pd
import os
import json

with open('./Configs/FirstMapProgressLevelsCost.json', 'r') as f:
    data = eval(f.read())

level_keys = list((data['ProgressLevelCostData']
                   ['FirstModeCostsConfig'].keys()))

mode_list = ['FirstModeCostsConfig',
             'SecondModeCostsConfig', 'ThirdModeCostsConfig','FourthModeCostsConfig']

level = [1, 13, 20, 27, 35, 47, 58, 100, 168]
all_level_data = pd.DataFrame()

for mode in mode_list:
    df_tmp = pd.json_normalize(data['ProgressLevelCostData'][mode])
    level_data = pd.DataFrame({'Level': level, 'mode': mode})
    config_df = pd.DataFrame({'Level': level})
    for v in level_keys:
        config_df[v] = df_tmp[v].explode(v)
        print(config_df)
        config_col_df = pd.json_normalize(config_df[v]).dropna(how='all')
        if not config_col_df.empty:
            config_col_df['Level'] = config_col_df['Level'].astype('int')
            config_col_df = config_col_df.rename(columns={'Value': v})
            level_data = level_data.merge(
                config_col_df, on=['Level'], how='left')
            level_data = level_data.fillna(method='ffill')
    all_level_data = pd.concat([all_level_data, level_data])
# print(all_level_data)
# all_level_data.to_excel('./Solitaire Colors/LevelCostData.xlsx')
