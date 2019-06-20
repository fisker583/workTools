
import xlsxwriter
import json

def json_to_excel(test,data):
    if isinstance(data, list):
        for value in data:
            test = json_to_excel(test,value)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key in test:
                pass
            else:
                test.append(key)
            test = json_to_excel(test,value)
    return test


data = json.loads(text)
test = []
test = json_to_excel(test,data)
print(test)
