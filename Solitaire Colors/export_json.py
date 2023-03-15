# from asyncio import current_task
import pandas as pd
import os
import ast
from pymongo import MongoClient
import requests


def convert_type(x, type_name):
    # type 'int' 'str' 'int_array' 'str_array' 'condition
    if type_name == 'int':
        return(int(x))
    elif type_name == 'str':
        return(str(x))
    elif type_name == 'int_array':
        x_list = []
        for v in str(x).split(','):
            x_list.append(int(v))
        return(x_list)
    elif type_name == 'str_array':
        x_list = []
        for v in str(x).split(','):
            x_list.append(str(v))
        return(x_list)
    elif type_name == 'condition':
        return({'type': 0})
    else:
        return(x)


def import_db(df, name, dbName):
    client = MongoClient('172.62.98.100', 27017)
    db = client[dbName]
    for collection in import_db_xlsx:
        if name == collection:
            db[collection].delete_many({})
            print(collection, 'delete_collection')
            data = df.to_dict(orient='records')
            db[collection].insert_many(data)
            print(collection, 'insert_collection')


def save_json_s():
    pass


def refresh_db():
    url = "http://172.62.98.100:9001/dress/test/refreshCache"

    payload = {}
    headers = {
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMjA0MTYyNTEwODIzNDI0IiwiZXhwIjoxNjU4Mzg5Njk5fQ._NAgKoHkgc3de0KYQ1Efg8bSsjreWQ-07-xdVJupDak'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


def save_json_c(df, name):
    json_file = '..\\'+DATA_PATH+'\\'+JSON_PATH_C + '\\' + name + '.json'
    # print(json_file, 'to_json\n', '*'*40)
    df.to_json(json_file, orient='records')
    if name == 'Language':
        # print(df)
        df.set_index('lang_key').to_json(json_file, orient='index')


def convert_df(df):
    column_types = df.loc[[1]].to_dict('records')[0]
    column_names = df.columns.to_list()
    df_drop = df.drop([0, 1]).fillna(0)
    for column_name in column_names:
        df_drop[column_name] = df_drop[column_name].apply(
            convert_type, args=(column_types[column_name],))

    return(df_drop)


def gen(file_path, name):
    def usecols(x): return not any(
        sub_str in x for sub_str in exclude_xlsx_columns)
    df = pd.read_excel(file_path+'\\' + XLSX_PATH+'\\' +
                       name + '.xlsx', usecols=usecols)
    print(name, 'gen\n', '*'*40)
    df_json = convert_df(df)
    save_json_c(df_json, name)
    import_db(df_json, name, 'dress_kokoya_test')
    import_db(df_json, name, 'dress_kokoya')


def gen_all():
    for (_, _, files) in os.walk('..\\'+DATA_PATH+'\\'+XLSX_PATH):
        for file_name in files:
            if (file_name[0] != '~' and file_name[-5:] == '.xlsx' and not file_name in exclude_xlsx):
                name = file_name[0:-5]
                file_path = os.getcwd()
                gen(file_path, name)


DATA_PATH, XLSX_PATH, JSON_PATH_C, JSON_PATH_S = 'NFT_Project_Data', 'xlsx_design', 'json_client', 'json_server'
exclude_xlsx = [
    '房型家具图片列表'
]
import_db_xlsx = [
    'equip_static',
    'global_static',
    'scene',
    'scene_jump',
    'furniture_static',
    'room_static',
    'room_type_static',
    'room_layout_furniture_static',
    'equip_body_static'
]
exclude_xlsx_columns = ['cehua']


gen_all()
refresh_db()
