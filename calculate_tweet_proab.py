#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import json
import os
# 类别数
classNum = 7
# 平滑参数
smoothPara = 1
os.system("> ./six_emotion_set.txt")
os.system("> ./calculate_emotion_set.txt")
prioProb = {"happiness":0, "like":0, "anger":0,"sadness":0,"fear":0, "disgust":0, "surprise":0}
numRes = {"happiness":0, "like":0, "anger":0,"sadness":0,"fear":0, "disgust":0, "surprise":0}
numCal = {"happiness":0, "like":0, "anger":0,"sadness":0,"fear":0, "disgust":0, "surprise":0}
# 统计其中情绪标签的先验概率
fpPrio = open("tmp.txt")
contents = fpPrio.readlines()
allList = []
for line in contents:
    line = line.split(",")
    for one in line:
        one = one.split(" ")
        for i in one:
            i = i.split("/")
            for j in i: 
                allList.append(j) 
# print allList
happinessNum = allList.count("happiness")
likeNum = allList.count("like")
angerNum = allList.count("anger")
sadnessNum = allList.count("sadness")
fearNum = allList.count("fear")
disgustNum = allList.count("disgust")
surpriseNum = allList.count("surprise")
totalNum = happinessNum + likeNum + angerNum + sadnessNum + fearNum + disgustNum + surpriseNum
prioProb["happiness"] = happinessNum/totalNum
prioProb["like"] = likeNum/totalNum
prioProb["anger"] = angerNum/totalNum
prioProb["sadness"] = sadnessNum/totalNum
prioProb["fear"] = fearNum/totalNum
prioProb["disgust"] = disgustNum/totalNum
prioProb["surprise"] = surpriseNum/totalNum

emotionList = ["happiness","like","anger","sadness","fear","disgust","surprise"]
# 打开统计的json文件
fp = open("./frequency_json.txt")
jsonStr = fp.read()
jsonDict = jsonStr.decode("utf-8").encode("utf-8")
jsonDict = json.loads(jsonDict)
# print jsonDict["like"]
# 计算每条tweet每种情绪的概率
fp =  open("./training_data_dict_extracted.txt")
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
    line = line.strip("\n")
    lineList = line.split(",")
    ## 更新每条tweet每个情绪的概率
    for emotion in emotionList:
        sumPWE = 0
        for wordEmotion in lineList:
            if wordEmotion:
                wordEmotionList= wordEmotion.split("/")
                # print wordEmotionList
                if wordEmotionList[1] == emotion:
                    ### 统计情绪对应的单词在句子中出现的次数
                    tmp = {}
                    numWordEmotionTweet = tmp.get(wordEmotion, 0) + 1
                    ### 统计情绪对应的单词在全文中出现的次数 
                    # print wordEmotionList[0],wordEmotionList[1] 
                    numWordEmotionText = jsonDict[wordEmotionList[1]][wordEmotionList[0].decode("utf-8")]
                    ### 计算p(w|e)
                    probWordEmotion = (numWordEmotionTweet + smoothPara)/(numWordEmotionText + (smoothPara*classNum))
                    sumPWE += probWordEmotion 
        ### 更新每条tweet的单一情绪概率
        eValue[emotion] = prioProb[emotion] * sumPWE
    maxValue = eValue[max(eValue,key=eValue.get)]
    lineSet = []
    for key in eValue:
        if 40*eValue[key] > maxValue:
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
## 计算的结果
# fpRes = open("./calculate_emotion_set.txt")
resContents = fpRes.readlines()
listIndex = 0
## 统计本来没有情绪标记为有情绪,或者有情绪没标记出来的个数
mistaken = 0
## 两者有交集的个数(包含相等)
equalNum = 0
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
    # if ((not line) and (not textSet[listIndex])):
    #     containNum = containNum + 1
    ## 误标记: 本来为空,却被标记; 或者本来有标签,却没被标记出来
    # if ((not line) and (textSet[listIndex])) or (line and (not textSet[listIndex])):
    if (line and (not textSet[listIndex])) or (not line and textSet[listIndex]):
        mistaken = mistaken + 1 
    ## 两个列表包含
    # if sorted(line) == sorted(textSet[listIndex]):
    if (set(line)) == (set(textSet[listIndex])):
        equalNum = equalNum + 1
    ## 没有交集且都不为空
    if line and textSet and not ( list(set(line).intersection(set(textSet[listIndex]))) ):
        notEqualNum = notEqualNum + 1
    ## 没有交集且都为空
    if not line and not textSet[listIndex]:
        print set(line),set(textSet[listIndex])
        equalNum = equalNum + 1
    listIndex = listIndex + 1
print "listIndex:", listIndex
print "mistaken:", mistaken
print "equalNum:", equalNum 
print "notEqualNum:", notEqualNum
print "subSet correct:", equalNum/listIndex
# 保存标记子集中每个情绪的个数
for line in resContents:
    if line:
        line = line.strip("\n").strip()
        lineList = line.split(",")
        for one in lineList:
            if one:
                numRes[one] = numRes[one] + 1
# 保存计算子集中每个情绪的个数
for lineList in textSet:
    if lineList:
        for one in lineList:
            if one:
                numCal[one] = numCal[one] + 1
# 计算每个情绪预测的正确率
print "cal num:%d",numCal
print "res num:%d",numRes
emotionRate = {"happiness":0,"like":0,"anger":0,"sadness":0,"fear":0,"disgust":0,"surprise":0}
for key in emotionRate:
    emotionRate[key] = numCal[key]/numRes[key]
print "every emotion correct rate:", emotionRate
# # 比较人为标记和词典标记的结果
# ## 词典标记的结果,去重
# fpDict = open("./training_data_six_only_emotion.txt")
# dictContents =  fpDict.readlines()
# listIndex = 0
# equalNum = 0
# notEqualNum = 0
# # 将人为标记结果存到列表中
# manList = []
# for one in resContents:
#     one = one.strip("\n")
#     one = one.split(",")
#     one = sorted(one)
#     manList.append(one)
# # 遍历词典标记的结果,开始比较
# dictList = []
# for line in dictContents:
#     line = line.strip("\n")
#     line = line.split(",") 
#     line = sorted(line)
#     dictList.append(list(set(line)))
#     if line: 
#         line = list(set(line))
#     ## 词典标记的序列是否包含人为标记的序列
#     if set(manList[listIndex]).issubset(set(line)) or set(line).issubset(set(manList[listIndex])):
#         equalNum = equalNum + 1
#         # print manList[listIndex], line, listIndex
#     else:
#         notEqualNum = notEqualNum + 1        
#         # print manList[listIndex], line, listIndex
#     listIndex = listIndex + 1 
# # for one in dictList:
# #     ## 词典标记且去重的结果
# #     os.system("echo %s >> six_emotion_set.txt"%(','.join(one)))
# print "man-made sign compares to dict:", equalNum
# print "listIndex:", listIndex
# print "notEqualNum:", notEqualNum
# fpDict.close()
# fpRes.close()
