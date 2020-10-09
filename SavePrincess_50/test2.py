import requests
import datetime
import time
import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np

t = 1595174400000
df = pd.DataFrame(np.random.randn(6, 2),columns=list('AB'))
df['B'] =  t
df['time'] = pd.to_datetime(df['B'], unit='ms')
df['time'] = df['time'].apply(
            lambda x: format(x, x.strftime('%Y-%m-%d')))
print(df)