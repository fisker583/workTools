# _*_ coding: utf-8
import os
import datetime
import time
import re
import random
import string
import shutil

import xlsxwriter
from io import BytesIO
from PIL import Image
import requests

img_src = 'https://jira.hyperledger.org/secure/attachment/15373/Screen%20Shot%20Add%20Chaincode.png'
res = requests.get(img_src, stream=True) 

byte_stream = BytesIO(res.content)  
imageW,imageH = Image.open(byte_stream).size
print(imageW,imageH)