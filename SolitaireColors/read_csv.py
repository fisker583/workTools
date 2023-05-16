import pandas as pd

file = 'e:/Fisker/Downloads/test.xlsx'
file2 = 'e:/Fisker/Downloads/test.csv'

df = pd.read_csv(file2, sep=',')
print(df)
df.replace(
    {'数据明细': {'null': 'None', 'true': 'True', 'false': 'False'}}, inplace=True)
df2 = df['数据明细'].apply(eval).apply(pd.Series)
print(df2)
df.drop(['数据明细'], axis=1, inplace=True)

df2['properties'] = df2['properties'].astype('string')
df3 = df2['properties'].apply(eval).apply(pd.Series)
print(df3['LastLevel'])
df2.drop(['properties'], axis=1, inplace=True)

df4 = pd.concat([df, df2], axis=1)
df4 = pd.concat([df4, df3], axis=1)

df4.to_excel('test23.xlsx')
