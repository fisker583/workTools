import logging
import sys
import time

import pandas as pd
from tabulate import tabulate


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


def read_file(file):
    with open('./Configs/' + file + '.json', 'r') as f:
        logger.warning(file)
        return eval(
            f.read()
            .replace('null', 'None')
            .replace('true', 'True')
            .replace('false', 'False')
        )


def replace_name(df):
    # df.columns.tolist()
    columns_name = {'L': 'level', 'V': 'multiplier'}
    df = df.rename(columns=columns_name)
    return (df)


def df_to_excel(df, sheet_name):
    df.to_excel('./Excel/'+'SolitaireGrandHarvestData.xlsx',
                sheet_name=sheet_name)


def gen_shop_factor_costs_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.json_normalize(config_data['shopFactor']['baseConfig'])
    config_df = replace_name(config_df)
    return (config_df)


def explode_df(df):
    mode_df = pd.DataFrame({'level': []})
    for column_name in df.columns.to_list():
        column_df_temp = pd.DataFrame({column_name: df[column_name]})
        column_df = pd.json_normalize(
            column_df_temp[column_name].explode())
        if column_df.empty:
            column_df['V'] = 0
            column_df['L'] = 0
        column_df['L'] = column_df['L'].astype('int')
        column_df = column_df.rename(
            columns={'V': column_name, 'L': 'level'})
        mode_df = mode_df.merge(
            column_df, on=['level'], how='outer', sort=True)

    mode_df = mode_df.fillna(method='ffill')
    mode_df = mode_df[mode_df['level'] != 0]
    return (mode_df)


def gen_progress_levels_costs_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for v_map in config_data['progressLevelCosts'].values():
        v_map['baseConfig'].pop('gemsFactors')
        for v_mode in v_map['baseConfig'].keys():
            mode_df = explode_df(pd.json_normalize(
                v_map['baseConfig'][v_mode]))
            mode_df.insert(1, 'mode', str(v_mode))
            config_df = pd.concat([config_df, mode_df])
    config_df_sort_mode = config_df.sort_values(
        by=['mode', 'level']).reset_index(drop=True)
    config_df_sort_level = config_df.sort_values(
        by=['level', 'mode']).reset_index(drop=True)
    logger.debug(config_df)
    return (config_df_sort_mode, config_df_sort_level)


def gen_lucky_wheel_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value']['wedges'])
        mode_df.insert(0, 'mode', (i_mode+1))
        config_df = pd.concat([config_df, mode_df])
    config_df = config_df.sort_values(
        by=['mode', 'wedgeIndex']).reset_index(drop=True)
    config_df.columns = [s.replace('skuData.', '').replace(
        '.multiplier', '×1000') for s in config_df.columns]
    logger.debug(config_df)
    return (config_df)


def gen_harvest_costs_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame(
        config_data['harvest']['baseConfig']['cropHarvestPrizes'])
    config_df = config_df[config_df['L'] < 1000]
    config_df['base'] = config_data['harvest']['baseConfig']['harvestBaseCredits']
    config_df = replace_name(config_df)
    config_df['sum'] = config_df['multiplier'].cumsum()+config_df['base']
    logger.debug(config_df)
    return (config_df)


def gen_tutorial_xlsx(config_key):
    config_data = read_file(config_key)
    config_data['TutorialLevelData'].pop('Tutorials')
    config_df = pd.json_normalize(
        config_data['TutorialLevelData']).T.sort_values(by=[0])
    config_df.columns = ['level']
    config_df['level'] = config_df['level']+1
    config_df['tutorial'] = config_df.index
    config_df = config_df.reset_index(drop=True)
    logger.debug(config_df)
    return (config_df)


def gen_score_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value']).T
        mode_df.rename(columns=lambda x: 'score_' +
                       str(i_mode+1), inplace=True)
        mode_df.insert(0, 'type', mode_df.index)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_recognition_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue'][0:2]):
        mode_df = pd.json_normalize(v_mode['value']['popups'])
        mode_df = mode_df.drop(['triggerType'], axis=1)
        mode_df.rename(columns=lambda x: x.replace(
            'triggerTarget', 'level') + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    # rewards_df = pd.json_normalize(config_df['rewards'])
    logger.debug(config_df)
    return (config_df)


def gen_new_game_modes_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value']).T
        mode_df.rename(columns=lambda x:  'level_' +
                       str(i_mode+1), inplace=True)
        mode_df.insert(0, 'modes', mode_df.index)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_happy_sam_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value']['dailyConfigs'])
        mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)

    logger.debug(config_df)
    return (config_df)


def gen_happy_sam_rewards_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value'])
        mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_happy_sam_multipliers_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        mode_df = pd.json_normalize(v_mode['value'])
        mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_crop_master_xlsx(config_key):
    config_data = read_file(config_key)
    config_df_picks = pd.DataFrame()
    config_df_rewards = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        for v_minigameConfigs in v_mode['value']['minigameConfigs'][:4]:
            for i_Rewards, Rewards in enumerate(v_minigameConfigs['ProbabilityConfigs']):
                Rewards_df = pd.json_normalize(
                    Rewards['Rewards'])
                Rewards_df.insert(0, 'Rewards_index', (i_Rewards+1))
                Rewards_df.insert(1, 'Probability', Rewards['Probability'])
                Rewards_df.insert(
                    2, 'StartLevel', v_minigameConfigs['StartLevel'])
                Rewards_df.insert(3, 'EndLevel', v_minigameConfigs['EndLevel'])
                Rewards_df.insert(0, 'segment', (i_mode+1))
                config_df_rewards = pd.concat(
                    [config_df_rewards, Rewards_df])
                logger.debug(Rewards_df)

        mode_df = pd.DataFrame(
            {'minigamePicks'+str(i_mode): v_mode['value']['minigamePicks'], 'starsThresholds'+str(i_mode): v_mode['value']['starsThresholds']})
        config_df_picks = pd.concat([config_df_picks, mode_df], axis=1)
    return (config_df_picks, config_df_rewards)


def gen_farmer_pass_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue'][0:1]):
        mode_df = pd.json_normalize(v_mode['value']['milestones'])
        # mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        logger.debug(config_df)
        # logger.debug(config_df['packs'].explode())
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_album_level_xlsx(config_key):
    config_data = read_file(config_key)
    config_df = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue'][0:2]):
        mode_df = pd.json_normalize(v_mode['value']['modes'])
        mode_df.rename(columns=lambda x: x + '_' + str(i_mode+1), inplace=True)
        mode_df.reset_index(drop=True, inplace=True)
        logger.debug(config_df)
        config_df.reset_index(drop=True, inplace=True)
        config_df = pd.concat([config_df, mode_df], axis=1)
    logger.debug(config_df)
    return (config_df)


def gen_my_farm_loot_xlsx(config_key):
    config_data = read_file(config_key)
    config_df_rewards = pd.DataFrame()
    for i_mode, v_mode in enumerate(config_data['queue']):
        for v_minigameConfigs in v_mode['value']['lootModes']:
            for i_Rewards, Rewards in enumerate(v_minigameConfigs['lootConfig']):
                Rewards_df = pd.json_normalize(
                    Rewards['reward'])
                Rewards_df.insert(0, 'Rewards_index', (i_Rewards+1))
                Rewards_df.insert(1, 'weight', Rewards['weight'])
                Rewards_df.insert(
                    2, 'mode', v_minigameConfigs['mode'])
                Rewards_df.insert(3, 'minGemsLootCards',
                                  v_minigameConfigs['minGemsLootCards'])
                Rewards_df.insert(3, 'maxGemsLootCards',
                                  v_minigameConfigs['maxGemsLootCards'])
                Rewards_df.insert(3, 'StarMultiplier',
                                  v_minigameConfigs['oneStarMultiplier'])
                Rewards_df.insert(0, 'segment', (i_mode+1))
                config_df_rewards = pd.concat(
                    [config_df_rewards, Rewards_df])
                logger.debug(Rewards_df)
    return (config_df_rewards)


def map_CodeBreakers(df, data):
    df['CodeBreakersGroup'] = len(data)
    df['CodeBreakersGroupNum'] = [0]
    if len(data) > 0:
        df['CodeBreakersGroupNum'] = pd.Series(
            str([len(i['CardValues']) for i in data]))
    return (df)


def map_BoneRewards(df, data):
    df['BoneNum'] = 0
    if len(data) > 0:
        df['BoneNum'] = len(data[0]['Rewards'])
    return (df)


def map_Streaks(df, data):
    if len(data) > 0:
        streaks_df = pd.json_normalize(data[0]['StreakList'])
        StreaksType = {0: 'plus+1', 1: 'gold_A',
                       2: 'gold_B', 3: 'gold_C', 4: 'wildCard'}
        StreaksNeed = {0: 5, 1: 4, 2: 4, 3: 4, 4: 6}
        streaks_df['TaskReward'] = streaks_df['StreakType'].apply(
            lambda x: StreaksType[x])
        streaks_df['TaskNeed'] = streaks_df['StreakType'].apply(
            lambda x: StreaksNeed[x])

        TaskNeed_df = pd.DataFrame(
            streaks_df['TaskNeed']).T.add_prefix('TaskNeed_').reset_index(drop=True)
        TaskReward_df = pd.DataFrame(
            streaks_df['TaskReward']).T.add_prefix('TaskReward_').reset_index(drop=True)
        streaks_df = pd.concat(
            [TaskNeed_df, TaskReward_df], axis=1).sort_index(axis=0)
        streaks_df.insert(0, 'TaskNum', len(TaskNeed_df.columns))
        df = pd.concat([df, streaks_df], axis=1)
    return (df)


def map_Groups(data):
    groups_df = pd.json_normalize(data)
    return (groups_df)


def map_StarLimits(df, data):
    data_df = pd.DataFrame(
        [data], columns=[f'StarLimits_{str(i + 1)}' for i in range(len(data))]
    )
    df = pd.concat([df, data_df], axis=1)
    return (df)


def map_Levels(config_df, config_Playfield_df, data, config_g):
    level_id = data['LevelIndex']
    logger.debug(level_id)
    level_df = pd.json_normalize(data)

    level_df['StackNum'] = len(
        data['Stack'])
    level_df['PlayfieldNum'] = len(
        data['Playfield'])

    level_df = map_CodeBreakers(
        level_df, data['CodeBreakers'])

    level_df = map_Streaks(
        level_df, data['Streaks'])

    level_Playfield_df = pd.json_normalize(
        data['Playfield'])

    level_df = map_BoneRewards(
        level_df, data['BoneRewards'])

    level_df = map_StarLimits(
        level_df, data['StarLimits'])

    level_Playfield_df = pd.json_normalize(
        data['Playfield'])

    level_Groups_df = map_Groups(data['Groups'])
    level_Groups_df['LevelIndex'] = level_df.loc[0, 'LevelIndex']
    level_Playfield_df['LevelIndex'] = level_df.loc[0,
                                                    'LevelIndex']
    level_Playfield_df['Name'] = level_df.loc[0, 'Name']

    level_df = level_df.drop(
        columns=[
            'Playfield', 'Stack', 'CodeBreakers', 'Groups', 'Streaks', 'BoneRewards', 'StarLimits', 'StarLimitsManual', 'DealDuration'
        ])

    config_df = pd.concat(
        [config_df, level_df])
    config_g = pd.concat(
        [config_g, level_Groups_df])
    config_Playfield_df = pd.concat(
        [config_Playfield_df, level_Playfield_df])
    return (config_df, config_Playfield_df, config_g)


def gen_map_xlsx(config_key):
    config_df_A = pd.DataFrame()
    config_Playfield_df_A = pd.DataFrame()
    config_df_B = pd.DataFrame()
    config_Playfield_df_B = pd.DataFrame()
    config_g_A = pd.DataFrame()
    config_g_B = pd.DataFrame()
    for v_config in config_key:
        config_data = read_file(v_config)
        for v_map in config_data['mapLevelData']['CropFields']:
            for v_level in v_map['Levels']:
                plan = v_level['Original']
                config_df_A, config_Playfield_df_A, config_g_A = map_Levels(
                    config_df_A, config_Playfield_df_A, plan, config_g_A)
                if len(v_level['Alternatives']) > 0:
                    plan = v_level['Alternatives'][0]
                    config_df_B, config_Playfield_df_B, config_g_B = map_Levels(
                        config_df_B, config_Playfield_df_B, plan, config_g_B)
    config_df_A = config_df_A.loc[:,
                                  (config_df_A != config_df_A.iloc[0]).any()]
    config_df_B = config_df_B.loc[:,
                                  (config_df_B != config_df_B.iloc[0]).any()]
    # logger.debug(config_df)
    return (config_df_A, config_Playfield_df_A, config_df_B, config_Playfield_df_B, config_g_A, config_g_B)


def gen_Streaks(config_key):
    Streaks_A = pd.DataFrame()
    Streaks_B = pd.DataFrame()
    for v_config in config_key:
        config_data = read_file(v_config)
        for v_map in config_data['mapLevelData']['CropFields']:
            for v_level in v_map['Levels']:
                plan = v_level['Original']
                Streaks_A = map_Streaks_BoneRewards(Streaks_A,  plan)
                if len(v_level['Alternatives']) > 0:
                    plan = v_level['Alternatives'][0]
                    Streaks_B = map_Streaks_BoneRewards(Streaks_B, plan)
    # Streaks_A = Streaks_A.loc[:,
    #                           (Streaks_A != Streaks_A.iloc[0]).any()]
    # Streaks_B = Streaks_B.loc[:,
    #                           (Streaks_B != Streaks_B.iloc[0]).any()]
    # logger.debug(config_df)
    return (Streaks_A, Streaks_B)


def map_Streaks_BoneRewards(config_df, data):
    level_df = pd.DataFrame()
    if len(data['BoneRewards']) > 0:
        level_df = pd.json_normalize(data['BoneRewards'][0]['Rewards'])

    level_df.insert(0, 'StackNum', len(data['Stack']))
    level_df.insert(0, 'PlayfieldNum', len(data['Playfield']))
    level_df.insert(0, 'Level', int(data['LevelIndex']))
    level_df.insert(0, 'Task_index', level_df.index+1)
    level_df['RestoredBoneRewards'] = pd.DataFrame(data['RestoredBoneRewards'])
    logger.warning(int(data['LevelIndex']))
    config_df = pd.concat(
        [config_df, level_df])
    return (config_df)


def map_df_rename(df):
    new_name = {
        key: map_columns_names[key]
        for key in list(map_columns_names.keys())
        if key in list(df.columns)
    }
    df = df.rename(columns=new_name)
    df = df[list(new_name.values())]
    return (df)


configs = {
    'shop_factor_costs_config': '商城系数',
    'progress_levels_costs_config': '关卡消耗',
    'crop_master': '宝箱奖励',
    'lucky_wheel_v2': '转盘奖励',
    'super_lucky_wheel_v2': '付费转盘奖励',
    'harvest_costs_config': '农场收获奖励',
    'TutorialConfig': '新手引导',
    'score_configuration': '计分配置',
    'recognition_popups': '首通奖励',
    'new_game_modes_opening': '模式解锁',
    'happy_sam_v2': '28天签到',
    'happy_sam_rewards_v2': '28天签到_奖励',
    'happy_sam_multipliers_v2': '28天签到_系数',
    'farmer_pass_milestone': '通行证奖励',
    'album_level': '图鉴掉落',
    'my_farm_loot_config': '宝石掉落'
}
map_config = [
    'MapConfig_1',
    'MapConfig_2',
    'MapConfig_3',
    'MapConfig_4'
]

map_columns_names = {
    'LevelIndex': '关卡',
    'Name': '关卡名称',
    'StackNum': '手牌数量',
    'PlayfieldNum': '场牌数量',
    'CodeBreakersGroup': '锁关卡组数量',
    'CodeBreakersGroupNum': '锁关卡每组锁数量',
    'GroupsNum': '分组数量',
    'BoneNum': '骨头关卡',
    'StarLimits_1': '星数限制_1',
    'StarLimits_2': '星数限制_2',
    'StarLimits_3': '星数限制_3',
    'TaskNum': '连击任务数量',
    'TaskNeed_0': '连击任务点数_1',
    'TaskReward_0': '连击任务奖励_1',
    'TaskNeed_1': '连击任务点数_2',
    'TaskReward_1': '连击任务奖励_2',
    'TaskNeed_2': '连击任务点数_3',
    'TaskReward_2': '连击任务奖励_3',
    'TaskNeed_3': '连击任务点数_4',
    'TaskReward_3': '连击任务奖励_4',
    'TaskNeed_4': '连击任务点数_5',
    'TaskReward_4': '连击任务奖励_5',
    'TaskNeed_5': '连击任务点数_6',
    'TaskReward_5': '连击任务奖励_6',
    'TaskNeed_6': '连击任务点数_7',
    'TaskReward_6': '连击任务奖励_7',
    'TaskNeed_7': '连击任务点数_8',
    'TaskReward_7': '连击任务奖励_8',
    'TaskNeed_8': '连击任务点数_9',
    'TaskReward_8': '连击任务奖励_9',
    'TaskNeed_9': '连击任务点数_10',
    'TaskReward_9': '连击任务奖励_10',
    'SimulateBoundStack': 'SimulateBoundStack',
    'SimulateBoundPlayfield': 'SimulateBoundPlayfield',
    'UnfoldType': 'UnfoldType',
    'UnfoldDuration': 'UnfoldDuration',
    'GladeDifficulty': 'GladeDifficulty',
    'UnfoldCenter.x': 'UnfoldCenter.x',
    'UnfoldCenter.y': 'UnfoldCenter.y',
    'UUID': 'UUID'

}

logger = my_logger()
logger.setLevel(logging.WARNING)


# with pd.ExcelWriter('./Excel/'+'HarvestData'+str(time.strftime("%Y-%m-%d %H_%M_%S", time.localtime()))+'.xlsx') as writer:
#     shop_df = gen_shop_factor_costs_xlsx('shop_factor_costs_config')
#     shop_df.to_excel(
#         writer, sheet_name=configs['shop_factor_costs_config'], index=False)

#     levels_costs_df_mode, levels_costs_df_level = gen_progress_levels_costs_xlsx(
#         'progress_levels_costs_config',)
#     levels_costs_df_mode.to_excel(
#         writer, sheet_name=configs['progress_levels_costs_config']+'-模式', index=False)
#     levels_costs_df_level.to_excel(
#         writer, sheet_name=configs['progress_levels_costs_config']+'-关卡', index=False)

#     lucky_wheel_df = gen_lucky_wheel_xlsx('lucky_wheel_v2')
#     lucky_wheel_df.to_excel(
#         writer, sheet_name=configs['lucky_wheel_v2'], index=False)

#     super_lucky_wheel_df = gen_lucky_wheel_xlsx('super_lucky_wheel_v2')
#     super_lucky_wheel_df.to_excel(
#         writer, sheet_name=configs['super_lucky_wheel_v2'], index=False)

#     harvest_costs_df = gen_harvest_costs_xlsx('harvest_costs_config')
#     harvest_costs_df.to_excel(
#         writer, sheet_name=configs['harvest_costs_config'], index=False)

#     tutorial_df = gen_tutorial_xlsx('TutorialConfig')
#     tutorial_df.to_excel(
#         writer, sheet_name=configs['TutorialConfig'], index=False)

#     score_df = gen_score_xlsx('score_configuration')
#     score_df.to_excel(
#         writer, sheet_name=configs['score_configuration'], index=False)

#     recognition_df = gen_recognition_xlsx('recognition_popups')
#     recognition_df.to_excel(
#         writer, sheet_name=configs['recognition_popups'], index=False)

#     new_game_modes_df = gen_new_game_modes_xlsx('new_game_modes_opening')
#     new_game_modes_df.to_excel(
#         writer, sheet_name=configs['new_game_modes_opening'], index=False)

#     new_happy_sam_df = gen_happy_sam_xlsx('happy_sam_v2')
#     new_happy_sam_df.to_excel(
#         writer, sheet_name=configs['happy_sam_v2'], index=False)

#     new_happy_sam_rewards_df = gen_happy_sam_rewards_xlsx(
#         'happy_sam_rewards_v2')
#     new_happy_sam_rewards_df.to_excel(
#         writer, sheet_name=configs['happy_sam_rewards_v2'], index=False)

#     new_happy_sam_multipliers_df = gen_happy_sam_multipliers_xlsx(
#         'happy_sam_multipliers_v2')
#     new_happy_sam_multipliers_df.to_excel(
#         writer, sheet_name=configs['happy_sam_multipliers_v2'], index=False)

#     crop_master_df, crop_master_reward_df = gen_crop_master_xlsx(
#         'crop_master')
#     crop_master_df.to_excel(
#         writer, sheet_name='宝箱奖励需求', index=False)
#     crop_master_reward_df.to_excel(
#         writer, sheet_name='宝箱奖励', index=False)

#     farmer_pass_df = gen_farmer_pass_xlsx(
#         'farmer_pass_milestone')
#     farmer_pass_df.to_excel(
#         writer, sheet_name='通行证奖励', index=False)

#     album_level_df = gen_album_level_xlsx(
#         'album_level')
#     album_level_df.to_excel(
#         writer, sheet_name='图鉴掉落', index=False)

#     my_farm_loot_df = gen_my_farm_loot_xlsx(
#         'my_farm_loot_config')
#     my_farm_loot_df.to_excel(
#         writer, sheet_name='宝石掉落', index=False)

with pd.ExcelWriter('./Excel/'+'HarvestMap'+str(time.strftime("%Y-%m-%d %H_%M_%S", time.localtime()))+'.xlsx') as writer:

    map_df_A, map_playfield_df_A, map_df_B, map_playfield_df_B, config_g_A, config_g_B = gen_map_xlsx(
        map_config[:3]
    )
    map_df_A = map_df_rename(map_df_A)
    map_df_B = map_df_rename(map_df_B)

    map_df_A.to_excel(writer, sheet_name='关卡概要_A', index=False)
    map_playfield_df_A.to_excel(writer, sheet_name='关卡场牌_A', index=False)
    config_g_A.to_excel(writer, sheet_name='关卡牌组_A', index=False)

    map_df_B.to_excel(writer, sheet_name='关卡概要_B', index=False)
    map_playfield_df_B.to_excel(writer, sheet_name='关卡场牌_B', index=False)
    config_g_B.to_excel(writer, sheet_name='关卡牌组_B', index=False)

    Streaks_A, Streaks_B = gen_Streaks(map_config[:3])
    Streaks_A.to_excel(writer, sheet_name='骨头关卡奖励_A', index=False)
    Streaks_B.to_excel(writer, sheet_name='骨头关卡奖励_B', index=False)
