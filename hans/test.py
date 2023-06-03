import pandas as pd
import numpy as np
import pandas as pd
import os
import logging
import sys
import json


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

def get_cells_df(df_table, list_table_cells):  # sourcery skip: avoid-builtin-shadow
    df_table_cells = pd.DataFrame()
    for i, v in enumerate(list_table_cells):
        str = v.replace('null', 'None')
        data = json.dumps(eval(str))
        data_json = json.loads(data)
        df = pd.json_normalize(data_json)
        df['receipt_id'] = df_table.iloc[i, df_table.columns.get_loc('_id')]
        df_table_cells = pd.concat([df_table_cells, df])

    df_table_cells.fillna(0,inplace=True)
    return(df_table_cells)

def get_table_colum(df_table,df_table_cells,df_table_cashier):
    df_table_cells.set_index('receipt_id', drop=False, inplace=True)
    df_table.set_index('_id', drop=False, inplace=True)
    df_table_cells['applyAt'] = pd.to_datetime(df_table['applyAt'], unit='ms')
        

    df_table_cells['currencyName'] = df_table['currencyName']
    df_table_cells['receiptType'] = df_table['receiptType']
    df_table_cells['verifyStatus'] = df_table['verifyStatus']
    df_table_cells['isPay'] = df_table['isPay']
    df_table_cells['isSelfClose'] = df_table['isSelfClose']

    df_table_cashier.set_index('receiptObjId', drop=False, inplace=True)
    df_table_cashier.rename_axis('receipt_id',inplace=True)
    df_table_cells['bankAcc'] = df_table_cashier['bankAcc']
    df_table_cells['internetBankAt'] = pd.to_datetime(df_table_cashier['internetBankAt'], unit='ms')
    return df_table_cells

# sourcery skip: avoid-builtin-shadow
logger = my_logger()
logger.setLevel(logging.WARNING)


df_receipt = pd.read_excel('./hans/OcrmReceiptEntity.xlsx')
df_receipt_table = pd.read_excel('./hans/OcrmReceiptTableEntity.xlsx')
df_cashier = pd.read_excel('./hans/OcrmCashierRecEntity.xlsx')
df_cashier_receipt = df_cashier[(df_cashier['receiptType'] !=3 )]
df_cashier_expense = df_cashier[(df_cashier['receiptType'] ==3 )]
df_expense = pd.read_excel('./hans/OcrmExpenseEntity.xlsx')
df_expense_table = pd.read_excel('./hans/OcrmExpenseTableEntity.xlsx')
df_bank = pd.read_excel('./hans/OcrmCustomEntity.xlsx')


#收/付
list_receipt_table_cells = df_receipt_table['cells'].to_list()
df_receipt_table_cells = get_cells_df(df_receipt,list_receipt_table_cells)

receipt_float_colums = ['orgGathered.$numberInt', 'orgPay.$numberInt', 'usdGathered.$numberInt','usdPay.$numberInt', 'orgPay', 'usdPay', 'orgGathered', 'usdGathered']
receipt_int_colums = ['isDiscard', 'receiptObjId','receiptType', 'isDiscard.$numberInt', 'receipt_id']

df_receipt_table_cells[receipt_float_colums] = df_receipt_table_cells[receipt_float_colums].astype(float)
df_receipt_table_cells[receipt_int_colums] = df_receipt_table_cells[receipt_int_colums].astype(int)

df_receipt_table_cells['orgGathered_test'] = df_receipt_table_cells['orgGathered.$numberInt'] + df_receipt_table_cells['orgGathered']
df_receipt_table_cells['usdGathered_test'] = df_receipt_table_cells['usdGathered.$numberInt'] + df_receipt_table_cells['usdGathered']
df_receipt_table_cells['orgPay_test'] = df_receipt_table_cells['orgPay.$numberInt'] + df_receipt_table_cells['orgPay']
df_receipt_table_cells['usdPay_test'] = df_receipt_table_cells['usdPay.$numberInt'] + df_receipt_table_cells['usdPay']
df_receipt_table_cells['isDiscard_test'] = df_receipt_table_cells['isDiscard.$numberInt'] + df_receipt_table_cells['isDiscard']

df_receipt_table_cells.drop(df_receipt_table_cells[receipt_float_colums],axis=1, inplace=True)
df_receipt_table_cells.drop(df_receipt_table_cells[['isDiscard','isDiscard.$numberInt']],axis=1, inplace=True)

df_receipt_table_cells = get_table_colum(df_receipt,df_receipt_table_cells,df_cashier_receipt)

logging.debug(df_receipt_table_cells)
df_receipt_table_cells.to_excel('./hans/df_receipt_table_cells.xlsx')

#报
list_expense_table_cells = df_expense_table['cells'].to_list()
df_expense_table_cells = get_cells_df(df_expense_table,list_expense_table_cells)

expense_float_colums = ['payAmount.$numberInt', 'payAmount']
df_expense_table_cells[expense_float_colums] = df_expense_table_cells[expense_float_colums].astype(float)
df_expense_table_cells['payAmount_test'] = df_expense_table_cells['payAmount.$numberInt'] + df_expense_table_cells['payAmount']

df_expense_table_cells.drop(df_expense_table_cells[expense_float_colums],axis=1, inplace=True)
df_expense_table_cells = get_table_colum(df_expense,df_expense_table_cells,df_cashier_expense)

logging.debug(df_expense_table_cells)
df_expense_table_cells.to_excel('./hans/df_expense_table_cells.xlsx')

#
df_cashier['createAt'] = pd.to_datetime(df_cashier['createAt'], unit='ms')
df_cashier['internetBankAt'] = pd.to_datetime(df_cashier['internetBankAt'], unit='ms')
df_cashier.drop(df_cashier[['attachFiles','remarks','updateAt']],axis=1, inplace=True)

logging.debug(df_cashier)
df_cashier.to_excel('./hans/df_cashier.xlsx')

bank_detail_columns = [
    'bankAcc',
    'currencyName',
    'receiptId',
    'receiptType',
    'isSserviceCharge',
    'receiveAmount',
    'payAmount',
    'overAmount',
    'fundCategory',
    'content',
    'internetBankAt'
]

df_bank_detail_taget_receipt_rename = {
    'receipt_id': 'receiptId',
    'usdGathered_test': 'receiveAmount',
    'usdPay_test': 'payAmount'
}

df_bank_detail_taget_expense_rename = {
    'receipt_id': 'receiptId',
    'payAmount_test': 'payAmount'
}
df_bank_detail_taget_cashier_rename = {
    'receiptObjId': 'receiptId',
    'serviceCharge': 'payAmount'
}

df_receipt_table_cells.rename(columns=df_bank_detail_taget_receipt_rename, inplace=True)
df_expense_table_cells.rename(columns=df_bank_detail_taget_expense_rename, inplace=True)
df_receipt_table_cells.reset_index(drop=True, inplace=True)
df_expense_table_cells.reset_index(drop=True, inplace=True)

df_bank_detail = pd.DataFrame()

bank_name = df_bank.iloc[0, df_bank.columns.get_loc('name')]
df_bank_detail = pd.concat([df_bank_detail, df_receipt_table_cells[(df_receipt_table_cells['bankAcc'] == bank_name ) & (df_receipt_table_cells['isPay'] == True )]])
df_bank_detail = pd.concat([df_bank_detail, df_expense_table_cells[(df_expense_table_cells['bankAcc'] == bank_name ) & (df_expense_table_cells['isPay'] == True )]])

df_cashier_serviceCharge = df_cashier[(df_cashier['bankAcc'] == bank_name ) & (df_cashier['serviceCharge'] != 0 )]
df_cashier_serviceCharge.rename(columns=df_bank_detail_taget_cashier_rename, inplace=True)
df_cashier_serviceCharge[['fundCategory','content']] = 'serviceCharge','serviceCharge'
# df_cashier_serviceCharge.reset_index(drop=True, inplace=True)
logging.warning(df_cashier_serviceCharge)

df_bank_detail = pd.concat([df_bank_detail, df_cashier_serviceCharge])

df_bank_detail.sort_values(by=['internetBankAt', 'receiptId','receiptType'],inplace=True)
df_bank_detail.fillna(0,inplace=True)
df_bank_detail.reset_index(drop=True, inplace=True)

bank_ini_amount = df_bank.iloc[0, df_bank.columns.get_loc('total')]
df_bank.loc[-1] = df_bank.loc(1)
df_bank.index = df_bank.index + 1
df_bank = df_bank.sort_index() 

df_bank_detail['diffAmount'] = df_bank_detail['receiveAmount'] - df_bank_detail['payAmount']

logging.warning(df_bank_detail)
df_bank_detail.to_excel('./hans/df_bank_detail.xlsx')
