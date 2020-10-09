import numpy as np
import pandas as pd
from anytree import AsciiStyle, Node, PostOrderIter, RenderTree, search
from anytree.exporter import DictExporter
from pymongo import MongoClient


def getUserTree(userFind):
    root = Node('root')
    for user in userFind:
        Node(user['_id'], shareCodeMemList=user.get(
            'shareCodeMemList'), parent=root)
    for node in root.children:
        if isinstance(node.shareCodeMemList, (list)):
            for userId in node.shareCodeMemList:
                search.find(root, lambda node: node.name ==
                            userId).parent = node
    return root


def getAlliance(children):
    mem = []
    if len(children):
        for node in children:
            tmp = []
            for nodeD in node.descendants:
                tmp.append(nodeD.name)
            mem.append(tmp)
    return mem


userDict = {
    "_id": "2",
    "userName": "glen1",
    "password": "1"
}
userYSDict = {
    "_id": 'ID',
    "userId": '角色ID',
    "gearId": "签约档位",
    "rDays": "已返还天数",
    "dictRdays": "总返还天数",
    "rYusd": '已返还YUSD',
    "dRyusd": '日返还YUSD',
    "dictTotalRyusd": '总返还YUSD',
    "status": "契约状态",
    "orderId": "契约编号",
    "updateAt": "更新时间",
    "createAt": "创建时间",
    "percentage": "返还进度"
}

global ROOT, USERDF, USERYSDF
client = MongoClient('192.168.0.110', 27017)
db = client['testYK']
userDoc = db['User'].find()
userYSDoc = db['UserYusdSign'].find()

ROOT = getUserTree(userDoc)
userDoc = db['User'].find()
USERDF = pd.DataFrame(list(userDoc), columns=userDict.keys())
USERYSDF = pd.DataFrame(list(userYSDoc), columns=userYSDict.keys())


def insertColums(df):
    for v in ['password', 'userName']:
        tmpDict = USERDF.set_index('_id').to_dict()[v]
        tmpSeries = df['userId']
        tmpSeries = tmpSeries.replace(tmpDict)
        df.insert(1, v, tmpSeries)


def modifyColums(df):
    df['percentage'] = df['rDays'] / df['dictRdays']
    df['percentage'] = df['percentage'].apply(
        lambda x: format(x, '.2%'))
    df['updateAt'] = pd.to_datetime(
        df['updateAt'], unit='ms')
    df['createAt'] = pd.to_datetime(
        df['createAt'], unit='ms')


def getTotalDict(df):
    specialKeys = {
        'gearId': 'sum',
        'rYusd': 'sum',
        'dRyusd': 'sum',
        'dictTotalRyusd': 'sum',
        'userId': 'nunique'
    }

    totalDict = dict.fromkeys(set(df.columns), 'count')
    totalDict.update(specialKeys)
    return totalDict


def sortColums(df):
    df.insert(1, 'userId', df.pop('userId'))
    return df


def sortRowUser(df):
    return df.sort_values(by=['userId'])


def sortRowGear(df):
    return df.sort_values(by=['gearId'], ascending=False)


def iniDf(users):
    if not isinstance(users, (list)):
        users = [users]
    df = pd.DataFrame(None, index=users, columns=userYSDict.keys())
    df['userId'] = users
    return df


def select(users, status):
    if not isinstance(users, (list)):
        users = [users]
    if not isinstance(status, (list)):
        users = [status]
    condition1 = USERYSDF['userId'].isin(users)
    condition2 = USERYSDF['status'].isin(status)
    return USERYSDF[(condition1 & condition2)]


def totalGroup(df):
    totalDict = {
        "_id": 'count',
        "gearId": "sum",
        "rYusd": 'sum',
        "dRyusd": 'sum',
        "dictTotalRyusd": 'sum',
        "orderId": 'count'
    }
    totalGroup = df.groupby(['userId'])
    totalGroup = totalGroup.agg(totalDict)
    totalGroup['_id'] = 'totalGroup'
    result = totalGroup.reset_index('userId')
    result.index = result['userId'].tolist()
    return result


def totalAll(df):
    totalDict = getTotalDict(df)
    df.loc['total'] = df.agg(totalDict)
    df.loc['total', '_id'] = 'total'
    result = df.tail(1)
    df.drop('total', inplace=True)
    return result


def combineDf(df, dfR):
    df['_id'] = dfR.iloc[0]['_id']
    return df.combine_first(dfR)


def concatDf(df, *df2):
    result = df
    for v in df2:
        result = pd.concat([result, v], ignore_index=True)
    return result


def dropColums(df):
    col = ['rDays', 'dictRdays', 'status',
           'percentage', 'updateAt', 'createAt']
    result = df.drop(col, axis=1)
    return result


class User():
    def __init__(self, userId):
        self.userId = userId
        self.node = search.find(ROOT, lambda node: node.name == userId)
        self.group = [node.name
                      for node in PostOrderIter(self.node)]
        self.child = [node.name
                      for node in self.node.children]
        self.alliance = getAlliance(self.node.children)
        self.status = [2]

    def getYusdSign(self, users):
        df = iniDf(users)
        result = select(users, self.status)
        if result.empty:
            result = df
        result = sortRowUser(result)
        modifyColums(result)
        insertColums(result)
        totalDf = totalAll(result)
        result = concatDf(result, totalDf)
        return result

    def getYusdTotal(self, users):
        df = iniDf(users)
        selectDf = select(users, self.status)
        if selectDf.empty:
            selectDf = df
        totalGroupDf = totalGroup(selectDf)
        totalGroupDf = combineDf(df, totalGroupDf)
        totalGroupDf = sortRowGear(totalGroupDf)
        insertColums(totalGroupDf)
        totalDf = totalAll(totalGroupDf)
        result = concatDf(totalGroupDf, totalDf)
        result = sortColums(result)
        result = dropColums(result)
        return result


def getchildGroup(userGroup):
    group = []
    for user in userGroup:
        child = User(user).child
        if len(child) == 0:
            child = [0]
        group.append(child)
    return group


class Alliance():
    def __init__(self, user):
        self.alliDict = {
            'userId': User(user).group,
            'child': [User(user).child for user in User(user).group],
            'alliance': [User(user).alliance for user in User(user).group],
            'gearId': None,
            'perfAll': None,
            'perfMax': None,
            'perf': None,
            'perfLev': None
        }

    def getPerf(self):
        yusdTotal = USERYSDF[USERYSDF['status'] == 2].groupby(
            ['userId']).agg('sum')['gearId']
        df = pd.DataFrame(self.alliDict, index=self.alliDict['userId'])
        df.update(yusdTotal)
        return df


def toExcel(df, fn):
    fn = str(fn) + '_yusd.xlsx'
    df.to_excel(fn)


user = User(605)
me = user.userId
df = Alliance('root').getPerf()

print(df)
# condition1 = USERYSDF['userId'].isin(users)
# condition2 = USERYSDF['status'].isin(status)
# USERYSDF[(condition1 & condition2)]
