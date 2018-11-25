#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
emotionList = ["happiness","like","anger","sadness","fear","disgust","surprise"]
# 统计数据集中每个词出现在每个情绪中的概率
## 先统计情绪词语集合,即
## {"emotion1":[{"word1":1,"word2":4,...,"wordn":x}]
##  "emotion2":[{"word1":1,"word2":4,...,"wordn":x}]
##  ......
##  "emotionn":[{"word1":1,"word2":4,...,"wordn":x}]
## }
# 内容合并成一行输出到tmp.txt文件中
fpData = open("./training_data_dict_extracted.txt")
dataList = []
dataStr = ""
for line in fpData.readlines():
    line = line.strip()
    if line:
        line = line.split("\n")
        for one in line:
            one = one.split(",")
            for i in one:
               dataList.append(i)
    dataStr = " ".join(dataList)
# print dataStr.decode("utf-8")
print dataStr
fpTmp = open("./tmp.txt", 'w')
fpTmp.write(dataStr)
fpTmp.close()

fpData.close()
# 统计词频
frequencyData = {}
with open("./tmp.txt") as fp:
    contents = fp.read()
contentsList = contents.split(" ") 
# print contentsList
## 找出相同情绪的词语
for emotion in emotionList:
    ###  保存单一情绪词集用,不统计个数
    tempList = []
    for wordEmotion in contentsList:
        wordEmotion = wordEmotion.split("/")
        if emotion == wordEmotion[1]:
            tempList.append(wordEmotion[0])
    ### 统计字典初始化
    d = dict.fromkeys(tempList,0)
    ### 统计
    for x in tempList:
        d[x] +=1
    ### 结果存储到json
    frequencyData[emotion] = d 
#print json.dumps(frequencyData, ensure_ascii=False)
with open("./frequency_json.txt", "w") as f:
    json.dump(frequencyData, f, ensure_ascii=False)
