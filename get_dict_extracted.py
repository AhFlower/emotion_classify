#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import sys
import os
pattern = "([一-龥！-～]|[a-z]|[A-Z])+/(PA|PE|PD|PH|PG|PB|PK|NA|NB|NJ|NH|PF|NI|NC|NG|NE|ND|NN|NK|NL|PC)"
fpInput = open("./training_data_dict.txt")
for line in fpInput.readlines():
    line = line.split(" ")
    rawTweetList = []
    rawTweetStr = ""
    for one in line:
        matchObj = re.search(pattern, one, 0)
        if matchObj:
            rawTweetList.append(matchObj.group())
    if not rawTweetList:
        print "rawTweetList is NULL"
    if rawTweetList:
        rawTweetStr = ",".join(rawTweetList)
    else:
        rawTweetStr = ""
    os.system("echo %s >> training_data_dict_extracted.txt"%(rawTweetStr))
