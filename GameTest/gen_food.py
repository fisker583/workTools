import itertools
import pandas as pd

def choiceFood(lev,data):
    foodList = []
    foodLev = []
    for v in data[0:-1]:
        if v['unlock_lev'] <= lev:
            foodLev.append(v['unlock_lev'])
            foodLev.sort()
    for v in foodLev:
        for vF in data:
            if vF['unlock_lev'] == v:
                foodList.append(vF['id'])
    return foodList

data = [{'type': 1, 'name': '米', 'id': 7000001, 'unlock_lev': 2, 'limits': 1},
        {'type': 2, 'name': '面', 'id': 7000002, 'unlock_lev': 6, 'limits': 1},
        {'type': 3, 'name': '肉', 'id': 7000003, 'unlock_lev': 8, 'limits': 3},
        {'type': 4, 'name': '蛋', 'id': 7000004, 'unlock_lev': 4, 'limits': 1},
        {'type': 5, 'name': '水产', 'id': 7000005, 'unlock_lev': 15, 'limits': 4},
        {'type': 6, 'name': '蔬菜', 'id': 7000006, 'unlock_lev': 11, 'limits': 2}
        # {'type': 7, 'name': '水果', 'id': 7000007, 'unlock_lev': 26, 'limits': 6}
        # {'type': 8, 'name': '调料', 'id': 7000008, 'unlock_lev': 15, 'limits': 0}
        ]
foodT = 7000008
lev = 30
levT = 1

levList = list(range(lev))
foodList =[]
orderList = []
orderKeys = ['lev','index','foodIn1','foodIn2']
for lev in levList:
    foodList = choiceFood(lev,data)
    if lev >= levT-1:
        foodList.append(foodT)
    if len(foodList) > 1:
        for kIn in range(len(foodList)-1):
            for row in itertools.combinations_with_replacement(foodList[0:kIn-len(foodList)-1+2], 2):
                orderList.append(list((lev+1,)+(kIn+1,)+row))


df = pd.DataFrame(orderList, columns=orderKeys)
print(df)
df.to_excel('orderList.xlsx')