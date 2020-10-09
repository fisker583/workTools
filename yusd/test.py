import numpy as np
import pandas as pd

a = [12, 367]
b = [
    [],
    [560, 373, 375, 376, 538, 558],
]
c = [
    [],
    [
        [],
        [384],
        [380, 470, 422],
        [377, 520],
        [539],
        []
    ]
]


def replaceList(val):
    t = [pd.NA]
    if len(val) == 0:
        t = pd.Series(val).apply(lambda x: [pd.NA] if (
            type(x) == list and len(x) == 0) else x).to_list()
    return t


df = pd.DataFrame({'user': a, 'child': b, 'alli': c})
df['child'] = df['child'] .apply(lambda x: [pd.NA] if (
    type(x) == list and len(x) == 0) else x)
df['alli'] = df['alli'].apply(replaceList)
print(df['alli'])
# df2 = df.loc[:, ['user', 'child', 'alli']]

# r = pd.DataFrame({
#     col: np.repeat(df2[col].values, df2['child'].str.len())
#     for col in df2.columns.drop('child')}
# ).assign(**{'child': np.concatenate(df2['child'].values)})[df2.columns]
# print(r)

# ab = np.array(np.array(df['alli'].values).flatten()).flatten()

# lst_col = 'samples'
# df = pd.DataFrame(
#     {'trial_num': [1, 2, 3, 1, 2, 3],
#      'subject': [1, 1, 1, 2, 2, 2],
#      'samples': [list(np.random.randn(3).round(2)) for i in range(6)]
#      }
# )


# r = pd.DataFrame({
#     col: np.repeat(df[col].values, df[lst_col].str.len())
#     for col in df.columns.drop(lst_col)}
# ).assign(**{lst_col: np.concatenate(df[lst_col].values)})[df.columns]
