import pandas as pd
import numpy as np
import pandas as pd
import os
import logging
import sys
import math

A = {'c1':['R','R'],'c2':['R','R'],'num':[1,2],'num2':[10,100]}
A = {'c1':['R','R'],'c2':['U','U'],'num':[1,2],'num2':[10,100]}
A = {'c1':['R','R'],'c2':['U','R'],'num':[1,2],'num2':[10,100]}
B = {'c1':[1000,0],'c2':[0,1000*2],'num':[2.045,2.5]}


# df_a = pd.DataFrame(A)
# print(df_a)

# # df_a['Group'] = df_a.apply(lambda row: math.floor((row.ID-1)/(row.Type-1))+1, axis=1)
# df_a['Group'] = df_a.apply(lambda row: row.num if row.c1 == row.c2 else row.num / row.num2, axis=1)
# print(df_a)

df_b = pd.DataFrame(B)
df_b['test']  = df_b['c1'] +df_b['c2']
df_b['test2']  = (df_b['c1'] +df_b['c2']) /df_b['num']

print(df_b)