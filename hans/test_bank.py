import pandas as pd
import numpy as np
import pandas as pd
import os
import logging
import sys
import json
import test_bank_config

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
    # if 'isDiscard' not in df_table.columns:
    #     df_table_cells['isDiscard'] = 0
    #     df_table_cells['isDiscard.$numberInt'] = 0
    # else:
    #     df_table_cells['isDiscard'] = df_table['isDiscard']
    #     df_table_cells['isDiscard.$numberInt'] = df_table['isDiscard.$numberInt']

    if 'receiptRate' not in df_table.columns:
        df_table_cells['receiptRate'] = 1
    else:
        df_table_cells['receiptRate'] = df_table['receiptRate'].astype(float)
    if 'voyagesName' not in df_table.columns:
        df_table_cells['voyagesName'] = 1
    else:
        df_table_cells['voyagesName'] = df_table['voyagesName'].astype(str)
    df_table_cashier.set_index('receiptObjId', drop=False, inplace=True)
    df_table_cashier.rename_axis('receipt_id',inplace=True)
    df_table_cells['bankAcc'] = df_table_cashier['bankAcc']
    df_table_cells['internetBankAt'] = pd.to_datetime(df_table_cashier['internetBankAt'], unit='ms')
    return df_table_cells

def get_df_bank_detail(bank_name,bank_currencyName,bank_iniAmount):
    df_bank_detail = pd.DataFrame()
    df_bank_detail = pd.concat([df_bank_detail, df_receipt_table_cells[(df_receipt_table_cells['bankAcc'] == bank_name ) & (df_receipt_table_cells['isPay'] == True )]])
    df_bank_detail = pd.concat([df_bank_detail, df_expense_table_cells[(df_expense_table_cells['bankAcc'] == bank_name ) & (df_expense_table_cells['isPay'] == True )]])
    df_bank_detail['bank_receiveAmount'] = df_bank_detail.apply(lambda row: row.orgGathered if bank_currencyName == row.currencyName else row.orgGathered / row.receiptRate, axis=1)
    df_bank_detail['bank_payAmount'] = df_bank_detail.apply(lambda row: row.orgPay if bank_currencyName == row.currencyName else row.orgPay / row.receiptRate, axis=1)

    df_cashier_serviceCharge = df_cashier[(df_cashier['bankAcc'] == bank_name ) & (df_cashier['serviceCharge'] != 0 )].copy()
    df_cashier_serviceCharge.rename(columns={'receiptObjId': 'receiptId','serviceCharge': 'bank_payAmount'}, inplace=True)
    df_cashier_serviceCharge['fundCategory'] = '手续费'
    df_cashier_serviceCharge['content'] = '手续费'
    df_cashier_serviceCharge['receiptRate'] = 1.0
    df_bank_detail = pd.concat([df_bank_detail, df_cashier_serviceCharge])
    df_bank_detail.sort_values(by=['internetBankAt', 'receiptId','receiptType'],inplace=True)
    df_bank_detail.fillna(0,inplace=True)

    df_bank_ini = pd.DataFrame([[0] * len(df_bank_detail.columns)], columns=df_bank_detail.columns)
    df_bank_ini['bankAcc'] = bank_name
    df_bank_ini['bankCurrencyName'] = bank_currencyName
    df_bank_ini['bank_receiveAmount'] = bank_iniAmount
    df_bank_ini['fundCategory'] = '初始余额'
    df_bank_ini['content'] = '初始余额'
    df_bank_ini['receiptRate'] = 1.0
    df_bank_ini['internetBankAt'] = pd.to_datetime(0, unit='ms')
    df_bank_detail = pd.concat([df_bank_ini, df_bank_detail])
    df_bank_detail.reset_index(drop=True, inplace=True)

    df_bank_detail['diffAmount'] = df_bank_detail['bank_receiveAmount'] - df_bank_detail['bank_payAmount']
    df_bank_detail['overAmount'] = df_bank_detail['diffAmount'].cumsum()
    df_bank_detail = df_bank_detail[test_bank_config.bank_detail_columns]
    return (df_bank_detail)

def get_df_excel_rename(df,name_dict):
    df_excel = df.copy()
    if 'receiptType' in df_excel.columns:
        df_excel['receiptType'] = df_excel['receiptType'].map(test_bank_config.receipt_type_dict)
    if 'verifyStatus' in df_excel.columns:
        df_excel['verifyStatus'] = df_excel['verifyStatus'].map(test_bank_config.receipt_status_dict)
    df_excel.rename(columns=name_dict, inplace=True)
    return (df_excel)
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
df_custom = pd.read_excel('./hans/OcrmCustomEntity.xlsx')
df_bank = df_custom[(df_custom['type'] ==5 )]

#R/P
list_receipt_table_cells = df_receipt_table['cells'].to_list()
df_receipt_table_cells = get_cells_df(df_receipt,list_receipt_table_cells)
df_receipt_table_cells = get_table_colum(df_receipt,df_receipt_table_cells,df_cashier_receipt)

receipt_float_colums = ['orgGathered.$numberInt', 'orgPay.$numberInt', 'usdGathered.$numberInt','usdPay.$numberInt', 'orgPay', 'usdPay', 'orgGathered', 'usdGathered']
# receipt_int_colums = ['isDiscard', 'receiptObjId','receiptType', 'isDiscard.$numberInt', 'receipt_id']
receipt_int_colums = ['receiptObjId','receiptType', 'isDiscard.$numberInt', 'receipt_id']

df_receipt_table_cells[receipt_float_colums] = df_receipt_table_cells[receipt_float_colums].astype(float)
df_receipt_table_cells[receipt_int_colums] = df_receipt_table_cells[receipt_int_colums].astype(int)

df_receipt_table_cells['orgGathered'] = df_receipt_table_cells['orgGathered.$numberInt'] + df_receipt_table_cells['orgGathered']
df_receipt_table_cells['db_usdGathered'] = df_receipt_table_cells['usdGathered.$numberInt'] + df_receipt_table_cells['orgGathered']
df_receipt_table_cells['usdGathered'] = df_receipt_table_cells['orgGathered'] / df_receipt_table_cells['receiptRate']

df_receipt_table_cells['orgPay'] = df_receipt_table_cells['orgPay.$numberInt'] + df_receipt_table_cells['orgPay']
df_receipt_table_cells['db_usdPay'] = df_receipt_table_cells['usdPay.$numberInt'] + df_receipt_table_cells['usdPay']
df_receipt_table_cells['usdPay'] = df_receipt_table_cells['orgPay'] / df_receipt_table_cells['receiptRate']

# df_receipt_table_cells['isDiscard'] = df_receipt_table_cells['isDiscard.$numberInt'] + df_receipt_table_cells['isDiscard']

df_receipt_table_cells.drop(df_receipt_table_cells[['orgGathered.$numberInt', 'orgPay.$numberInt', 'usdGathered.$numberInt','usdPay.$numberInt']],axis=1, inplace=True)
df_receipt_table_cells.drop(df_receipt_table_cells[['isDiscard','isDiscard.$numberInt']],axis=1, inplace=True)

df_receipt_table_cells.drop(df_receipt_table_cells[['receiptObjId']],axis=1, inplace=True)
logging.debug(df_receipt_table_cells)

df_receipt_table_cells_excel = get_df_excel_rename(df_receipt_table_cells,test_bank_config.receipt_table_excel_name_dict)
df_receipt_table_cells_excel.to_excel('./hans/df_receipt_table_cells.xlsx',index=False)

#E
list_expense_table_cells = df_expense_table['cells'].to_list()
df_expense_table_cells = get_cells_df(df_expense_table,list_expense_table_cells)
df_expense_table_cells = get_table_colum(df_expense,df_expense_table_cells,df_cashier_expense)

df_expense_table_cells[['payAmount.$numberInt', 'payAmount']] = df_expense_table_cells[['payAmount.$numberInt', 'payAmount']].astype(float)
df_expense_table_cells['orgPay'] = df_expense_table_cells['payAmount.$numberInt'] + df_expense_table_cells['payAmount']

df_expense_table_cells.drop(df_expense_table_cells[['payAmount.$numberInt']],axis=1, inplace=True)

logging.debug(df_expense_table_cells)

df_expense_table_cells_excel = get_df_excel_rename(df_expense_table_cells,test_bank_config.expense_table_excel_name_dict)
df_expense_table_cells_excel.to_excel('./hans/df_expense_table_cells.xlsx',index=False)

#C
df_cashier['createAt'] = pd.to_datetime(df_cashier['createAt'], unit='ms')
df_cashier['internetBankAt'] = pd.to_datetime(df_cashier['internetBankAt'], unit='ms')

df_cashier.drop(df_cashier[['attachFiles','remarks','updateAt']],axis=1, inplace=True)

logging.debug(df_cashier)

df_cashier_excel = get_df_excel_rename(df_cashier,test_bank_config.cashier_excel_name_dict)
df_cashier_excel.to_excel('./hans/df_cashier.xlsx',index=False)


# R/P- C
# df_cashier['indexType'] = df_cashier['receiptType']*1000000 + df_cashier['receiptObjId']
# df_receipt_table_cells['indexType'] = df_receipt_table_cells['receiptType']*1000000 + df_receipt_table_cells['receipt_id']
# df_cashier_new = df_cashier.set_index('indexType', drop=False)
# df_receipt_table_cells_new = df_receipt_table_cells.set_index('indexType', drop=False)
# df_receipt_table_cells_new = pd.concat([df_receipt_table_cells_new,df_cashier_new],axis=1)
# logging.warning(df_receipt_table_cells_new)
# df_receipt_table_cells_new = get_df_excel_rename(df_receipt_table_cells_new,test_bank_config.receipt_table_excel_name_dict)
# df_receipt_table_cells_new.to_excel('./hans/df_receipt_table_cells_new.xlsx',index=False)

#B
df_receipt_table_cells.rename(columns={'receipt_id': 'receiptId','usdGathered': 'receiveAmount','usdPay': 'payAmount'}, inplace=True)
df_expense_table_cells.rename(columns={'receipt_id': 'receiptId','payAmount': 'payAmount'}, inplace=True)
df_receipt_table_cells.reset_index(drop=True, inplace=True)
df_expense_table_cells.reset_index(drop=True, inplace=True)

df_bank['total'] = df_bank['total'].astype(float)
bank_list = df_bank['name'].to_list()

# file_name = './hans/df_bank_detail.xlsx'
# if os.path.exists(file_name):
#     os.remove(file_name)
# pd.DataFrame().to_excel(file_name)
# for bank in bank_list:
#     bank_name = bank
#     bank_currencyName = df_bank.loc[df_bank['name'] == bank_name, 'currencyName'].values
#     bank_iniAmount = df_bank.loc[df_bank['name'] == bank_name, 'total'].values
#     df_bank_detail = get_df_bank_detail(bank_name,bank_currencyName,bank_iniAmount)

#     logging.debug(df_bank_detail)
#     df_bank_detail_excel = get_df_excel_rename(df_bank_detail,test_bank_config.bank_detail_excel_name_dict)
#     with pd.ExcelWriter(file_name, mode='a',engine='openpyxl') as writer:
#         sheet_name = bank.replace("/", '_')
#         logging.warning(sheet_name)
#         df_bank_detail_excel.to_excel(writer, sheet_name=sheet_name[:30], index=False)

df_bank_detail_all = pd.DataFrame()

for bank in bank_list:
    bank_name = bank
    bank_currencyName = df_bank.loc[df_bank['name'] == bank_name, 'currencyName'].values
    bank_iniAmount = df_bank.loc[df_bank['name'] == bank_name, 'total'].values
    df_bank_detail = get_df_bank_detail(bank_name,bank_currencyName,bank_iniAmount)

    logging.debug(df_bank_detail)
    df_bank_detail_all = pd.concat([df_bank_detail_all, df_bank_detail])

df_bank_detail_all.sort_values(by=[ 'bankAcc','internetBankAt'],inplace=True)
df_bank_detail_all = get_df_excel_rename(df_bank_detail_all,test_bank_config.bank_detail_excel_name_dict)
# df_bank_detail_all.to_excel('./hans/df_bank_detail_all.xlsx',index=False)


file_name = './hans/hans_all.xlsx'
if os.path.exists(file_name):
    os.remove(file_name)
pd.DataFrame().to_excel(file_name)

with pd.ExcelWriter(file_name, mode='a',engine='openpyxl') as writer:

        df_receipt_table_cells_excel.to_excel(writer, sheet_name='receipt', index=False)
        df_expense_table_cells_excel.to_excel(writer, sheet_name='expense', index=False)
        df_cashier_excel.to_excel(writer, sheet_name='cashier', index=False)
        df_bank_detail_all.to_excel(writer, sheet_name='bank', index=False)
