#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
prioProb = {"happiness":0.15696837064886, "like":0.4610104184202159, "anger":0.0084357406056525, "sadness":0.0846192694012682, "fear":0.0320782597310289, "disgust":0.2435329106110768, "surprise":0.0133550305818978}
emotionList = ["happiness","like","anger","sadness","fear","disgust","surprise"]
# 统计数据集中每个词出现在每个情绪中的概率
## 先统计情绪词语集合,即
## {"emotion1":[{"word1":1,"word2":4,...,"wordn":x}]
##  "emotion2":[{"word1":1,"word2":4,...,"wordn":x}]
##  ......
##  "emotionn":[{"word1":1,"word2":4,...,"wordn":x}]
## }
frequencyData = {}
with open("./tmp.txt") as fp:
    contents = fp.read()
contentsList = contents.split(",") 
## 找出相同情绪的词语
for emotion in emotionList:
    print emotion
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
