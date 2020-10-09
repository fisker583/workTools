import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient('192.168.0.160', 27017)
db = client['orangelove']

dictLogYakl = {
    "_id": None,
    "orderId": None,
    "type": None,
    "yakChatId": None,
    "amount": None,
    "createAt": None,
    "code": None,
    "message": None,
    "userId": None,
    "userName": None,
    "reqValue": None
}
dictLogUserYusdRevenue = {
    "_id": None,
    "userId": None,
    "userName": None,
    "gearId": None,
    "type": None,
    "total": None,
    "beforeValue": None,
    "delta": None,
    "afterValue": None,
    "param": None,
    "createAt": None
}

dicitUserYusdSign = {
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
    "createAt": "创建时间"
}

dictUserAlliHistoryLog = {
    "_id": None,
    "userId": None,
    "userName": None,
    "getLev": None,
    "effectLev": None,
    "alliVipLev": None,
    "totalProfit": None,
    "memAmount": None,
    "createAt": None,
    "effectSignList": None,
    "alreadyReturn": None,
    "dictTotalReturn": None,
    "totalGear": None,
    "finalProfit": None,
    "childTotalGear": None,
    "childMemAmount": None,
    "totalRyusd": None,
    "totalDyusd": None
}

# db.getCollection("LogUserYusdRevenue").find({"createAt" : { $gte : 1588780800000 }}).sort({
logYakl = pd.DataFrame(list(db['LogYakl'].find()), columns=dictLogYakl.keys())
LogUserYR = pd.DataFrame(
    list(db['LogUserYusdRevenue'].find()), columns=dictLogUserYusdRevenue.keys())
UserYusdSign = pd.DataFrame(
    list(db['UserYusdSign'].find()), columns=dicitUserYusdSign.keys())
UserAlliHistoryLog = pd.DataFrame(
    list(db['UserAlliHistoryLog'].find()), columns=dictUserAlliHistoryLog.keys())

Wallet = pd.DataFrame(
    list(db['Wallet'].find()))
logYakl366 = logYakl[logYakl['userId'] == 366]
LogYR366 = LogUserYR[LogUserYR['createAt'] >= 1589385600000]
UserYS366 = UserYusdSign[UserYusdSign['userId'] == 366]
UserAlli366 = UserAlliHistoryLog[UserAlliHistoryLog['userId'] == 366]
Walletdf = Wallet['yusdRevenue'].sum()
print(Walletdf)
with pd.ExcelWriter('output.xlsx') as writer:
    # logYakl366.to_excel(writer, sheet_name='logYakl366')
    LogYR366.to_excel(writer, sheet_name='LogYR366')
    # UserYS366.to_excel(writer, sheet_name='UserYS366')
    # UserAlli366.to_excel(writer, sheet_name='UserAlli366')
