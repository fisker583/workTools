receipt_table_excel_name_dict = {
    'fundCategory': '资金类别',
    'content': '备注内容',
    'receipt_id': '单据单号',
    'receiptType': '单据类型',
    'orgGathered': '收款金额',
    'usdGathered': '借方金额',
    'orgPay': '付款金额',
    'usdPay': '贷方金额',
    # 'isDiscard': '是否废弃',
    'applyAt': '单据时间',
    'currencyName': '单据币种',
    'verifyStatus': '审核步骤',
    'isPay': '是否已付款',
    'isSelfClose': '是否自己已关闭',
    'bankAcc': '银行账号',
    'internetBankAt': '银行日期',
    'receiptRate': '单据汇率'

}
expense_table_excel_name_dict = {
    'fundCategory': '资金类别',
    'content': '备注内容',
    'receipt_id': '单据单号',
    'payAmount': '贷方金额',
    'applyAt': '单据时间',
    'currencyName': '单据币种',
    'receiptType': '单据类型',
    'verifyStatus': '审核步骤',
    'isPay': '是否已付款',
    'isSelfClose': '是否自己已关闭',
    'bankAcc': '银行账号',
    'internetBankAt': '银行日期',
    'receiptRate': '单据汇率',
    'orgPay': '付款金额'
}
cashier_excel_name_dict = {
    '_id': '序号',
    'bankAcc': '银行账号',
    'createAt': '创建时间',
    'currencyName': '银行币种',
    'gatheredTotal': '出纳金额',
    'internetBankAt': '银行日期',
    'receiptObjId': '单据单号',
    'receiptType': '单据类型',
    'serviceCharge': '手续费金额'
}
bank_detail_columns = [
    'bankAcc',
    'currencyName',
    'bankCurrencyName',
    'receiptId',
    'receiptType',
    'fundCategory',
    'content',
    'internetBankAt',
    'orgGathered',
    'bank_receiveAmount',
    'orgPay',
    'bank_payAmount',
    'overAmount',
    'receiptRate',
    'isPay',
    'verifyStatus'
    # 'isDiscard'
]
bank_detail_excel_name_dict = {
    'bankAcc': '银行账号',
    'bankCurrencyName': '账号资金币种',
    'currencyName': '单据资金币种',
    'receiptId': '单据单号',
    'receiptType': '单据类型',
    'fundCategory': '资金类别',
    'content': '备注内容',
    'internetBankAt': '银行日期',
    'orgGathered': '单据收款金额',
    'bank_receiveAmount':'银行币种借方金额',
    'orgPay': '单据付款金额',
    'bank_payAmount':'银行币种贷方金额',
    'overAmount': '当前余额',
    'receiptRate': '单据汇率',
    'isPay': '单据是否已付款',
    'verifyStatus': '单据审核状态'
    # 'isDiscard': '单据是否已废弃'

}
receipt_type_dict = {
    0: '无',
    1: '收款单',
    2: '付款单',
    3: '报销单'
}
receipt_status_dict = {
    0: '无',
    1: '未送审',
    2: '部门复核中',
    3: '业务经理审核中',
    4: '公司批复中',
    5: '财务经理审核中',
    6: '出纳审核中',
    7: '总经理审核中',
    8: '出纳完成中',
    9: '已关闭',
    10: '驳回中'
}
