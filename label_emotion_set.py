#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 标记原始样本
from __future__ import division
import json
import os
# 经分割后的原始文本
os.system("> ./training_data_res.txt")
fpText = open("./training_data_mark_5.txt")
fpDuit = open("./duit.txt")
textContents = fpText.readlines()
duitContents = fpDuit.readlines()
for tweet in textContents:  
    lineSet = []
    for dictionary in duitContents:
        dictItem = dictionary.split(",") 
        try:
            if dictItem[0] in tweet and int(dictItem[2]) >= 5 and int(dictItem[3] != 0):
                lineSet.append(dictItem[1])
        except:
            print dictItem
    lineSet = list(set(lineSet))
    lineStr = ",".join(lineSet)
    os.system("echo %s >> ./training_data_res.txt"%(lineStr))
