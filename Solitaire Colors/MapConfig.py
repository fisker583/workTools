import pandas as pd
import os
import json

with open('./Solitaire Colors/MonoBehaviour/MapConfig_1.json', 'r') as f:
    data = eval(f.read())


# obj = data['mapLevelData']['CropFields'][1]['Levels'][0]['Original']['Playfield']
# obj2 = data['mapLevelData']['CropFields'][1]['Levels'][0]['Original']['Stack']
# test_key = 'Playfield'
# print(type(obj))
# print(len(obj))
# print(obj.keys())
# print(obj['LevelIndex'])
# print(obj[test_key])


# df = pd.DataFrame(obj)
# df2 = pd.DataFrame(obj2)
# print(df)
# print(df2)

# df.to_excel('./Solitaire Colors/Playfield.xlsx')

def get_streaks(streaks_data):
    df = pd.json_normalize(streaks_data)
    StreaksType = {0: 'plus1', 1: 'gold1',
                   2: 'gold2', 3: 'gold3', 4: 'wildCard'}
    df['StreakType'] = df['StreakType'].apply(lambda x: StreaksType[x])
    res = df.T.drop(
        labels=['StarPoints', 'BoneProperty.Type', 'BoneProperty.Count'], axis=0).reset_index(drop=True)
    res.columns = ['Streaks' + str(i+1) for i in range(len(res.columns))]
    res['StreaksNum'] = len(res.columns)
    return (res)


Playfield = pd.DataFrame()
Stack = pd.DataFrame()
Original = pd.DataFrame()
for i, v in enumerate(data['mapLevelData']['CropFields']):
    for i2, v2 in enumerate(v['Levels']):
        print('map', i, i2, 'LevelIndex', v2['Original']['LevelIndex'])
        LevelIndex = v2['Original']['LevelIndex']
        level_df = pd.json_normalize(v2['Original'])
        level_df['StackNum'] = len(v2['Original']['Stack'])
        level_df['PlayfieldNum'] = len(v2['Original']['Playfield'])
        if len(v2['Original']['Streaks']) > 0:
            streaks_df = get_streaks(
                v2['Original']['Streaks'][0]['StreakList'])
            level_df = pd.concat([level_df, streaks_df], axis=1)
        Original = pd.concat(
            [Original, level_df.drop(columns=['Playfield', 'Stack'])])

        Playfield_df = pd.json_normalize(v2['Original']['Playfield'])
        Playfield_df['LevelIndex'] = LevelIndex
        Playfield = pd.concat(
            [Playfield, Playfield_df])

        Stack_df = pd.json_normalize(v2['Original']['Stack'])
        Stack_df['LevelIndex'] = LevelIndex
        Stack = pd.concat(
            [Stack, Stack_df])

Original = Original.loc[:, (Original != Original.iloc[0]).any()]


Original.to_excel('./Solitaire Colors/Original.xlsx')
Playfield.to_excel('./Solitaire Colors/Playfield.xlsx')
Stack.to_excel('./Solitaire Colors/Stack.xlsx')

# for i, v in enumerate(data['mapLevelData']['CropFields']):
#     for i2, v2 in enumerate(v['Levels']):
#         print(i, i2, v2['Original']['LevelIndex'])
