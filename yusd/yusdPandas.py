import numpy as np
import pandas as pd


class User():
    def __init__(self, dbFind):
        self.columnDict = {
            "_id": "2",
            "userName": "glen1",
            "password": "1"
        }
        self.df = pd.DataFrame(list(dbFind), columns=self.columnDict.keys())


class UserYusdSign():
    def __init__(self, dbFind):
        self.columnDict = {
            "_id": 'ID',
            "userId": '角色ID',
            "gearId": "签约档位",
            "rDays": "已返还天数",
            "dictRdays": "总返还天数",
            "rYusd": '已返还YUSD',
            "dRyusd": '日返还YUSD',
            "dictTotalRyusd": '总返还YUSD',
            "transferId": "transferId",
            "updateAt": "更新时间",
            "createAt": "创建时间",
            "status": "契约状态",
            "orderId": "契约编号",
            "isAnimation": ""
        }
        self.df = pd.DataFrame(list(dbFind), columns=self.columnDict.keys())


class YusdSign():
    def __init__(self):
        pass

    def get(self, dfObj, userId: list, user, status: list = [2]):
        mask1 = dfObj.df['userId'].isin(userId)
        mask2 = dfObj.df['status'].isin(status)
        maskDf = dfObj.df[(mask1 & mask2)]

        nameDict = user.df.set_index('_id').to_dict()['userName']
        pwdDict = user.df.set_index('_id').to_dict()['password']

        tName = maskDf['userId']
        tPwd = maskDf['userId']
        tName = tName.replace(nameDict)
        tPwd = tPwd.replace(pwdDict)
        maskDf.insert(1, 'password', tPwd)
        maskDf.insert(1, 'userName', tName)
        maskDf.pop('orderId')
        maskDf.pop('transferId')
        maskDf.pop('isAnimation')

        maskDf['percentage'] = maskDf['rDays'] / maskDf['dictRdays']
        maskDf['percentage'] = maskDf['percentage'].apply(
            lambda x: format(x, '.2%'))
        maskDf['updateAt'] = pd.to_datetime(
            maskDf['updateAt'], unit='ms')
        maskDf['createAt'] = pd.to_datetime(
            maskDf['createAt'], unit='ms')
        totalDict = {'gearId': 'sum', 'rYusd': 'sum', 'userId': 'nunique',
                     'dRyusd': 'sum', 'dictTotalRyusd': 'sum'}
        sumSeries = maskDf.agg(totalDict)
        countSeries = maskDf.count()
        maskDf.loc['sum'] = sumSeries
        maskDf.loc['count'] = countSeries
        maskDf.loc[['sum'], ['_id']] = 'SumAll'
        maskDf.loc[['count'], ['_id']] = 'CountAll'
        for v in userId:
            tmpDf = maskDf.loc[maskDf['userId'] == v]
            sumDf = tmpDf.agg(totalDict)
            countDf = tmpDf.count()
            maskDf.loc['sum_'+str(v)] = sumDf
            maskDf.loc['count_'+str(v)] = countDf
            maskDf.loc[['sum_'+str(v)], ['_id']] = 'sum_'+str(v)
            maskDf.loc[['count_'+str(v)], ['_id']] = 'count_'+str(v)
        headers = maskDf.columns.to_numpy().tolist()
        data = maskDf.to_numpy().tolist()
        data.insert(0, headers)
        return data, maskDf

    def getDfSum(self, childDf, descDf):
        return childDf.loc['sum', 'gearId'], descDf.loc['sum', 'gearId']

    def getAlliance(self, user, gear):
        df = pd.DataFrame({'userId': user, 'gear': gear},
                          columns=['userId', 'gear'])
        df.to_excel('Alliance.xlsx')