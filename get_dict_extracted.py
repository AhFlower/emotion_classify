#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 将DUTIR标注的结果筛选出来, 依赖于情绪强度和词性
import re
import sys
import os
pattern = "([一-龥！-～]|[a-z]|[A-Z])+/(PA|PE|PD|PH|PG|PB|PK|NA|NB|NJ|NH|PF|NI|NC|NG|NE|ND|NN|NK|NL|PC)"
os.system("> ./training_data_dict_extracted.txt")
os.system("> ./training_data_six_only_emotion.txt")
emotionClass = {
"PA":"happiness", 
"PE":"happiness" ,
"PD":"like",
"PH":"like",
"PG":"like",
"PB":"like",
"PK":"like",
"NA":"anger", 
"NB":"sadness", 
"NJ":"sadness", 
"NH":"sadness", 
"PF":"sadness", 
"NI":"fear", 
"NC":"fear", 
"NG":"fear", 
"NE":"disgust",
"ND":"disgust",
"NN":"disgust",
"NK":"disgust",
"NL":"disgust",
"PC":"surprise" 
}

# 将词典存到json文件中
jsonDuit = {}
fpDuit = open("./duit_res.txt")
for line in fpDuit.readlines():
    line = line.strip("\n")
    lineList = line.split(",") 
    # print lineList
    data = lineList[0].decode("utf-8")
    jsonDuit[data] = lineList[1:]
# print jsonDuit
# 打开预先粗略标记的文件
fpInput = open("./training_data_mark_5.txt")
for line in fpInput.readlines():
    line = line.split(" ")
    rawTweetList = []
    rawTweetStr = ""
    for one in line:
        matchObj = re.search(pattern, one, 0)
        if matchObj:
            ## 再一次筛选前一次标注的结果, 依赖词性和强度
            matchItem = matchObj.group() 
            matchItem = matchItem.split("/")
            # print matchItem[0].decode("utf-8")
            # 如果匹配目标的情感强度大于7小于等于9,并且词不是中性词(0,1,2三个极性)
            if jsonDuit.has_key(matchItem[0].decode("utf-8")) \
            and ( jsonDuit[matchItem[0].decode("utf-8")][0] == matchItem[1] )\
            and ( int(jsonDuit[matchItem[0].decode("utf-8")][1]) >= 4 ) \
            and ( int(jsonDuit[matchItem[0].decode("utf-8")][1]) <= 9 ) \
            and (int(jsonDuit[matchItem[0].decode("utf-8")][2]) != 0): 
                #### 替换情绪标签
                if emotionClass.has_key(matchItem[1]):
                    item = matchObj.group()
                    item =  item.replace(matchItem[1],emotionClass[matchItem[1]])
                    rawTweetList.append(item)
    if not rawTweetList:
        rawTweetStr = ""
        # print "rawTweetList is NULL"
    if rawTweetList:
        rawTweetStr = ",".join(rawTweetList)

    os.system("echo %s >> training_data_dict_extracted.txt"%(rawTweetStr))
    ## 替换情绪前面的单词+/
    rawTweetStr = re.sub(r'([一-龥！-～]+/|([a-z]|[A-Z])+/)', "",  rawTweetStr)
    os.system("echo %s >> training_data_six_only_emotion.txt"%(rawTweetStr))
