#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import json
import os
# 类别数
classNum = 6
# 平滑参数
smoothPara = 1
prioProb = {"happiness":0.15696837064886, "like":0.4610104184202159, "anger":0.0084357406056525, "sadness":0.0846192694012682, "fear":0.0320782597310289, "disgust":0.2435329106110768, "surprise":0.0133550305818978}
emotionList = ["happiness","like","anger","sadness","fear","disgust","surprise"]
# 打开统计的json文件
fp = open("./frequency_json.txt")
jsonStr = fp.read()
jsonDict = jsonStr.decode("utf-8").encode("utf-8")
jsonDict = json.loads(jsonDict)
# print jsonDict["like"]
# 计算每条tweet每种情绪的概率
fp =  open("./training_data_six_emotion.txt")
textSet = []
num = 0
for line in fp.readlines():
    # print line
    line = line.strip('\n').strip()
    eValue = {}
    ## 初始化每条tweet每个情绪的概率
    for emotion in emotionList:
        eValue[emotion] = 0
    # print eValue
    lineList = line.split(",")
    ## 更新每条tweet每个情绪的概率
    for emotion in emotionList:
        sumPWE = 0
        for wordEmotion in lineList:
            if wordEmotion:
                wordEmotionList= wordEmotion.split("/")
                if wordEmotionList[1] == emotion:
                    ### 统计情绪对应的单词在句子中出现的次数
                    tmp = {}
                    numWordEmotionTweet = tmp.get(wordEmotion, 0) + 1
                    ### 统计情绪对应的单词在全文中出现的次数 
                    numWordEmotionText = jsonDict[wordEmotionList[1]][wordEmotionList[0].decode("utf-8")]
                    ### 计算p(w|e)
                    probWordEmotion = (numWordEmotionTweet + smoothPara)/(numWordEmotionText + (smoothPara*classNum))
                    sumPWE += probWordEmotion 
        ### 更新每条tweet的单一情绪概率
        eValue[emotion] = prioProb[emotion] * sumPWE
    maxValue = eValue[max(eValue,key=eValue.get)]
    lineSet = []
    for key in eValue:
        if 5*eValue[key] > maxValue:
            lineSet.append(key)   
    textSet.append(lineSet)
    num += 1
print num
print textSet
