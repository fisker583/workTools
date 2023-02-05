from PIL import Image
import pandas as pd
import numpy as np
import matplotlib as mpl
import pandas.io.formats.excel as fmt_xl
import logging
import sys


df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=list('abc'))
test = {
    "mode1": {
        "levelStartCosts": [
            {
                "L": 1,
                "V": 1000.0
            },
            {
                "L": 20,
                "V": 1500.0
            },
            {
                "L": 35,
                "V": 1800.0
            },
            {
                "L": 58,
                "V": 2000.0
            },
            {
                "L": 100,
                "V": 2200.0
            },
            {
                "L": 168,
                "V": 2500.0
            }
        ],
        "levelWonPrizes": [
            {
                "L": 1,
                "V": 1110.0
            },
            {
                "L": 20,
                "V": 1665.0
            },
            {
                "L": 35,
                "V": 2100.0
            },
            {
                "L": 58,
                "V": 2221.0
            },
            {
                "L": 100,
                "V": 2442.0
            },
            {
                "L": 168,
                "V": 2775.0
            }
        ],
        "wildCosts": [
            {
                "L": 1,
                "V": 500.0
            },
            {
                "L": 13,
                "V": 1000.0
            },
            {
                "L": 20,
                "V": 2000.0
            },
            {
                "L": 35,
                "V": 3000.0
            },
            {
                "L": 47,
                "V": 4500.0
            },
            {
                "L": 58,
                "V": 6000.0
            },
            {
                "L": 100,
                "V": 6600.0
            },
            {
                "L": 168,
                "V": 7500.0
            }
        ],
        "undoCosts": [
            {
                "L": 1,
                "V": 100.0
            },
            {
                "L": 20,
                "V": 200.0
            },
            {
                "L": 35,
                "V": 300.0
            },
            {
                "L": 47,
                "V": 400.0
            },
            {
                "L": 58,
                "V": 500.0
            },
            {
                "L": 100,
                "V": 550.0
            },
            {
                "L": 168,
                "V": 625.0
            }
        ],
        "plus5Costs": [
            {
                "L": 1,
                "V": 500.0
            },
            {
                "L": 20,
                "V": 900.0
            },
            {
                "L": 27,
                "V": 1500.0
            },
            {
                "L": 35,
                "V": 2000.0
            },
            {
                "L": 47,
                "V": 3000.0
            },
            {
                "L": 58,
                "V": 4000.0
            },
            {
                "L": 100,
                "V": 4400.0
            },
            {
                "L": 168,
                "V": 5000.0
            }
        ],
        "removeCardsCosts": [
            {
                "L": 1,
                "V": 1700.0
            },
            {
                "L": 20,
                "V": 2500.0
            },
            {
                "L": 58,
                "V": 3300.0
            },
            {
                "L": 100,
                "V": 3700.0
            },
            {
                "L": 168,
                "V": 4200.0
            }
        ],
        "clearPlayablesCosts": [
            {
                "L": 1,
                "V": 2000.0
            },
            {
                "L": 20,
                "V": 3000.0
            },
            {
                "L": 58,
                "V": 4000.0
            },
            {
                "L": 100,
                "V": 4400.0
            },
            {
                "L": 168,
                "V": 5000.0
            }
        ],
        "wildDropCosts": [
            {
                "L": 1,
                "V": 2700.0
            },
            {
                "L": 20,
                "V": 4000.0
            },
            {
                "L": 58,
                "V": 5300.0
            },
            {
                "L": 100,
                "V": 5900.0
            },
            {
                "L": 168,
                "V": 6700.0
            }
        ],
        "removeBombsCosts": [
            {
                "L": 1,
                "V": 1700.0
            },
            {
                "L": 20,
                "V": 2500.0
            },
            {
                "L": 58,
                "V": 3300.0
            },
            {
                "L": 100,
                "V": 3700.0
            },
            {
                "L": 168,
                "V": 4200.0
            }
        ],
        "removeValueChangersCosts": [
            {
                "L": 1,
                "V": 1700.0
            },
            {
                "L": 20,
                "V": 2500.0
            },
            {
                "L": 58,
                "V": 3300.0
            },
            {
                "L": 100,
                "V": 3700.0
            },
            {
                "L": 168,
                "V": 4200.0
            }
        ],
        "removeCodeBreakersCosts": [
            {
                "L": 1,
                "V": 2000.0
            },
            {
                "L": 20,
                "V": 3000.0
            },
            {
                "L": 58,
                "V": 4000.0
            },
            {
                "L": 100,
                "V": 4400.0
            },
            {
                "L": 168,
                "V": 5000.0
            }
        ],
        "triggerProbabilities": [
            {
                "L": 1,
                "V": 0.15
            }
        ],
        "levelCostWithFreeRoundDiscounts": None
    },

}


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


logger = my_logger()
# mode_df = pd.DataFrame({'L': []})
# df1 = pd.DataFrame(test['mode1']['levelStartCosts'])
# df2 = pd.DataFrame(test['mode1']['wildCosts'])
# df1 = df1.merge(df2, on=['L'], how='outer', sort=True)
# mode_df = mode_df.merge(df1, on=['L'], how='outer', sort=True)
# mode_df['mode'] = 'mode_df'
# logger.debug(mode_df)
# with pd.ExcelWriter('output.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='Sheet_name_1')
#     df2.to_excel(writer, sheet_name='Sheet_name_2')
colourImg = Image.open("test.png")
colourPixels = colourImg.convert("RGB")
colourArray = np.array(colourPixels.getdata()).reshape(colourImg.size + (3,))
indicesArray = np.moveaxis(np.indices(colourImg.size), 0, 2)
allArray = np.dstack((indicesArray, colourArray)).reshape((-1, 5))


df = pd.DataFrame(allArray, columns=["y", "x", "red", "green", "blue"])

test = {"Streaks": [
    {
        "StreakList": [
            {
                "StreakType": 0,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 3,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 4,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 4,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 0,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 4,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 4,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            },
            {
                "StreakType": 0,
                "BoneProperty": {
                    "Type": 0,
                    "Count": 0
                },
                "StarPoints": 0
            }
        ]
    }
]
}


test = [2.709, 6.5, 8.99]

df = pd.DataFrame([test], columns=['A_' + str(i+1)
                  for i in range(len(test))])
df = df[['A_3', 'A_1', 'A_2']]
# logger.debug(df)

map_columns_names = {'A_1': 'B1', 'A_2': 'B2', 'A_3': 'B3', 'A_4': 'B4'}
nameA = list(df.columns)


def map_df_rename(df):
    new_name = {}
    for key in list(map_columns_names.keys()):
        if key in list(df.columns):
            new_name.update({key: map_columns_names[key]})
    df = df.rename(columns=new_name)
    df = df[list(new_name.keys())]
    return (df)


df = map_df_rename(df)
logger.debug(df)
