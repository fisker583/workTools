# _*_ coding: utf-8
import xlsxwriter
import os
import csv
from PIL import Image
import shutil

def csvReader(fPath, fName):
    file = fPath + fName + '.csv'
    data = []
    try:
        with open(file, 'r', newline='') as cf:
            reader = csv.DictReader(cf)
            for i, rows in enumerate(reader):
                data.append(rows)
            cf.close()
    except Exception as e:
        print(file)
    return(data)


xlsxName = 'E:/Fisker/Pictures/Icon/SOMA_图标列表x.xlsx'
imagePath = 'E:/Fisker/Pictures/Icon/in/'
csvPath = 'E:/Fisker/Pictures/Icon/'
csvName = 'items'


def imageResize(path, name):
    image = path+name+'.png'
    imageOutPath = path+name+'.png'
    shutil.copyfile(image,'E:/Fisker/Pictures/Icon/out/'+name+'.png') 
    if os.path.exists(image):
        image1 = Image.open(image, 'r')
        scale = 1
        imageW, imageH = image1.size
        if imageW > 128 and imageW >= imageH:
            scale = 128/imageW
        elif imageH > 128 and imageH >= imageW:
            scale = 128/imageH
        newW = int(imageW*scale)
        newH = int(imageH*scale)
        image2 = image1.resize((newW, newH))
        image2.save(path+name+'_resize.png', 'png')
        imageOutPath = path+name+'_resize'+'.png'
    return(imageOutPath)


dataList = csvReader(csvPath, csvName)
wb = xlsxwriter.Workbook(xlsxName)
ws = wb.add_worksheet('ICON')
for i, rows in enumerate(dataList):
    col = 0
    row = rows['icon']
    image = imagePath+rows['icon']+'.png'
    print(image)
    imageOut = imageResize(imagePath, rows['icon'])
    ws.set_row(i, 96)
    ws.set_column(
        len(rows.items())+1, len(rows.items())+1, 16)
    if os.path.exists(image):
        print(image)
        ws.insert_image(i, len(rows.items()) +
                                             1, imageOut)
    for j, v in enumerate(rows.values()):
        col += 1
        ws.write(i, col, v)
print('wb.close()...')
wb.close()
# os.startfile(xlsxName)
