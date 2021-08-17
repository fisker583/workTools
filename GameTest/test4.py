# _*_ coding: utf-8
import xlsxwriter
import os
import xml.etree.ElementTree as ET
import pandas as pd


def iter_records(records):
    """
    遍历每个节点的生成器
    :param records:
    :return:
    """
    for record in records:
        temp_dict = {}  # 存储节点key-value
        for var in record:
            print(var.text)
            # temp_dict[var.attrib['var_name']] = var.text
        # 生成值，即每个节点的数据
        yield temp_dict


def read_xml(xmlFileName):
    with open(xmlFileName, 'r', encoding="utf-8") as xml_file:
        tree = ET.parse(xml_file)
        # 访问根节点
        root = tree.getroot()
        # 从根节点开始遍历，返回df
        return pd.DataFrame(list(iter_records(root)))


xmlFile = 'E:/Fisker/Downloads/rs/zh-Hant.xml'

df = read_xml(xmlFile)
