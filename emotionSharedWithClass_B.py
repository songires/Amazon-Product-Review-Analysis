#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################
__version__ = "0.1"
__date__ = "Oct. 19, 2015"
__author__ = "Muhammad Abdul-Mageed"
####################################
import argparse
import codecs
import time
import sys
import os, re
import nltk
from collections import defaultdict
from random import shuffle

def getListOfLines():
    """
    Just takes a file and returns a list of its line
    """
    #hard-coding path to inputfile for now
    infileObject=codecs.open("ENGLISH.AUGUST2015.UNIQ", "r", "utf-8")
    listOfLines= infileObject.readlines()
    return listOfLines


lines=getListOfLines()
#print "Raw lines:               ", len(lines)
emotionLines= [line.lower() for line in lines if len(line.split("\t"))==4]
#print "Lines of len=4 fields:   ", len(emotionLines)
#print emotionLines[:3]
firstThreeLines=emotionLines[:3]
# TEST:
print"*"*50
#print firstThreeLines

# for i in firstThreeLines:
#     tweetId, screenName, userName, tweet = i.split("\t")
#     print tweetId, screenName, userName, tweet

#####################################
tags= ["#happy", "#sad", "#disgusted", "#fearful" , "#surprised", "#angry"] #"#scared"

def tagInSecondHalf(tag, tweet):
    """
    Conditioning position of tag in tweet.
    P.S. Won't consider a tag like #happyday.
    """
    tweet=tweet.split()
    if tag not in tweet:
        return False
    midPoint=(len(tweet)/2)
    tagIndex=tweet.index(tag)
    if tagIndex > midPoint:
        return True
    return False

def tagInLastThird(tag, tweet):
    """
    Conditioning position of tag in tweet.
    P.S. Won't consider a tag like #happyday.
    """
    tweet=tweet.split()
    if tag not in tweet:
        return False
    thirdPoint=(len(tweet)/4)
    tagIndex=tweet.index(tag)
    if tagIndex > thirdPoint*3:
        return True
    return False

def pure(tag, tweet):
    tagList= ["#happy", "#sad", "#disgusted", "#fearful" , "#surprised", "#angry", "#scared"]
    tagList.remove(tag)
    for t in tagList:
        if t in tweet: 
            return False
    return True


def removeSeed(seed, tweet):
    """
    """
    if type(seed)==str:
        tweet= re.sub(seed, " ", tweet)
    elif type(seed)==list:
        for t in seed:
            tweet= re.sub(t, " ", tweet)
    else:
        print type(seed)
        print "arg1/Tag must be a string or list, you provided ", type(tag), "."
        exit()
    #clean
    tweet=re.sub("\s+", " ", tweet)
    #tweet=tweet.trim()
    tweet=tweet.rstrip()
    tweet=tweet.lstrip()
    return tweet

def clean(tweet):
    """
    Example of a function where you can clean your data.
    You can add more code here
    """
    tweet= re.sub(".", " ", tweet)
    return tweet

def longTweet(tweet):
    """
    """
    if len(tweet.split()) > 10:
        return True
    return False
    
        

#----------------------------------------------
#shuffle the data
shuffle(emotionLines)
#emotionLines=emotionLines[:500000]

tagLexicon= ["happy", "sad", "disgusted", "fearful" , "surprised", "angry", "scared"] 
myData={}
for cat in tagLexicon:
    tag="#"+cat
    myData[cat]=[tweet for tweet in emotionLines if tag in tweet.split() and pure(tag, tweet)
                 and tagInLastThird(tag, tweet)  and len(tweet.split()) > 4
                 and removeSeed(tag, tweet) and clean(tweet) and longTweet(tweet)]
#----------------------------------------------
#----------------------------------------------
# lump "fearful" with "scared"
for k in myData:
    if k=="fearful":
        myData["scared"].append(myData[k])

myData.pop("fearful", None)

  
# Print some stats:
##########################
print "*"*50, "\n"

# for k in myData:
#     print k, len(myData[k]), "-->", myData[k]

majorClass=max([len(myData[k]) for k in myData])
totalCount=sum([len(myData[k]) for k in myData])
print "Majority class: ", majorClass
print "Total data point count: ", totalCount
 
print "Majority class in all the data: ", round((majorClass/float(totalCount))*100, 2), "%"
print "*"*50, "\n"
#newData=[(k, myData[k][i]) for k in myData for i in range(len(myData[k]))]
# The below gets me tweet body only (and filters out rest of each tweet line [e.g., tweetId.])
newData=[(k, "".join(myData[k][i]).split("\t")[-1]) for k in myData for i in range(len(myData[k]))]
shuffle(newData)
def getFeatures(dataPoint):
    features=defaultdict()
    # label is class name, of course, and feats is just a list of words in this case.
    label, feats=dataPoint[0], dataPoint[1].split()
    # I could also add some code to remove the seeds from the feature dict instead of the heavy computation in
    # the tweet cleaning in removeSeed
    ###########################################
    # Beautify the below, building "has(word): True/False" dict
    for i in feats:
        features[i]=i
    if "#fearful" in features:
        del features["#fearful"]
    if "#scared" in features:
        del features["#scared"]
    return features, label

featuresets=[getFeatures(i) for i in newData]

#print newData[0:3]
#print featuresets[0]
#print "*"*100, "\n"
#----------------------------------------------
# Divide Train, Dev, and Test.
# For now, I just create a train and a test. I actually include two test sets
#----------------------------------------------
#totalLength=len(myData[k])
train_set, test_set1, test_set2 = featuresets[2000:], featuresets[:1000], featuresets[1000:2000]
print "train_set:", len(train_set)#, type(train_set), train_set[0]
print "test_set:", len(test_set1), len(test_set2)
classifier = nltk.NaiveBayesClassifier.train(train_set)
print "Accuracy on test1: ", round((nltk.classify.accuracy(classifier, test_set1))*100, 2), "%"
print "Accuracy on test2: ", round((nltk.classify.accuracy(classifier, test_set2))*100, 2), "%"

print classifier.show_most_informative_features(50)

#print nltk.classify.predict(classifier, test_set)

##########################################
# Tod-Do: Get majority class from TRAIN
##########################################