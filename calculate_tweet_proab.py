#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import json
import os
# 类别数
classNum = 6
# 平滑参数
smoothPara = 0.8
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
        if 2*eValue[key] > maxValue:
            lineSet.append(key)   
    textSet.append(lineSet)
    num += 1
## 保存计算的结果
for one in textSet:
    ## 词典标记且去重的结果
    os.system("echo %s >> calculate_emotion_set.txt"%(','.join(one))) 
# 比较人为标记的结果和计算出来的结果
## 人为标记的结果
fpRes = open("./training_data_res.txt")
resContents = fpRes.readlines()
listIndex = 0
## 统计本来没有情绪标记为有情绪,或者有情绪没标记出来的个数
mistaken = 0
## 两者有交集的个数(包含相等)
containNum = 0
## 都不为空且无交集的个数
notEqualNum = 0
for line in resContents:
    line = line.strip("\n")
    line = line.strip()
    if not line:
        line = []
    else:
        line = line.split(",")
    ## 两个列表相等
    ## if cmp(sorted(textSet[listIndex]),line) == 0:
    ## 都为空: 
    if ((not line) and (not textSet[listIndex])):
        containNum = containNum + 1
    ## 误标记: 本来为空,却被标记; 或者本来有标签,却没被标记出来
    if ((not line) and (textSet[listIndex])) or (line and (not textSet[listIndex])):
        mistaken = mistaken + 1 
    ## 两个列表包含
    if list(set(line).intersection(set(textSet[listIndex]))):
        containNum = containNum + 1
    ## 没有交集
    if ( (line) and (textSet[listIndex])) and not ( list(set(line).intersection(set(textSet[listIndex]))) ):
        notEqualNum = notEqualNum + 1
    listIndex = listIndex + 1
print "listIndex:", listIndex
print "mistaken:", mistaken
print "containNum:", containNum
print "notEqualNum:", notEqualNum


# 比较人为标记和词典标记的结果
## 词典标记的结果,去重
fpDict = open("./training_data_six_only_emotion.txt")
dictContents =  fpDict.readlines()
listIndex = 0
equalNum = 0
# 将人为标记结果存到列表中
manList = []
for one in resContents:
    one = one.strip("\n")
    one = one.split(",")
    one = sorted(one)
    manList.append(one)
# 遍历词典标记的结果,开始比较
dictList = []
for line in dictContents:
    line = line.strip("\n")
    line = line.split(",") 
    line = sorted(line)
    dictList.append(list(set(line)))
    if line: 
        line = list(set(line))
    ## 词典标记的序列是否包含人为标记的序列
    if set(line).issubset(set(manList[listIndex])):
        equalNum = equalNum + 1
    listIndex = listIndex + 1 
for one in dictList:
    ## 词典标记且去重的结果
    os.system("echo %s >> six_emotion_set.txt"%(','.join(one)))
print "man-made sign compares to dict:", equalNum
print "listIndex:", listIndex
fpDict.close()
fpRes.close()
