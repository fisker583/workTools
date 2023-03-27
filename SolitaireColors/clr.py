import contextlib
import re
file  = 'E:/Fisker/Documents/log.txt'
with open(file, 'r+', encoding='utf-8') as fr:
    data = fr.readlines()
out = []
for v in data:
    if v[:len('<color=#39E32C>MoneyChange')] == '<color=#39E32C>MoneyChange':
        s = v.split(' ')
        lists =[]
        for v2 in s:
            with contextlib.suppress(Exception):
                v2 = v2.replace('</color>',"")
                lists.append(int(v2))
        out.append(lists)

print(out)