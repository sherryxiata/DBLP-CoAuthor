# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 17:56
# @Author  : wenlei

'''
项目配置文件
'''

import codecs
import time
import numpy as np
import pandas as pd

root_path='E:/研二上学习/研二课程/数据挖掘/DBLP/dataset/'

result_path='E:/研二上学习/研二课程/数据挖掘/DBLP/result/'

#加载apriori所需数据
def loadData(inFile):
    dataSet = []
    for line in inFile:
        line = line.strip().split(',')
        dataLine = [int(word) for word in line if word.isdigit()]
        dataSet.append(dataLine)
    return dataSet