
#######################
from sklearn.metrics import classification_report, accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

__version__ = "0.2"
__date__ = "Nov. 16, 2015"
__author__ = "Muhammad Abdul-Mageed"
__modified__ = "Mrunal Pagnis"
"""
This code is distributed in SMM Z639.
Although this code runs, it may have bugs and is sub-optimal.
You can use the code, change it., etc. but please do not re-distribute.
Let me know if you catch any bugs.
"""
####################################

import codecs
from random import shuffle
import numpy as np
from numpy import array
import sys
import nltk
from nltk.tokenize import word_tokenize # or use some other tokenizer


reload(sys)
sys.setdefaultencoding('utf8')


def read_file_data():
    """
    """
    with codecs.open("naivefeatures.txt", "r", "utf-8") as my_file:
        lines = [next(my_file) for x in xrange(1000)]

    data_tuples = []

    for line in lines:
        try:
            tup = (line.split("\t")[1].lower(), line.split("\t")[0])
            data_tuples.append(tup)
        except:
            continue

    return data_tuples

data_tuples = read_file_data()

all_words = set(word for review in data_tuples for word in word_tokenize(review[0]))
featuresets = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in data_tuples]

train_set, test_set1, test_set2 = featuresets[:800], featuresets[800:900], featuresets[900:1000]
print "train_set:", len(train_set)#, type(train_set), train_set[0]
print "test_set:", len(test_set1), len(test_set2)
classifier = nltk.NaiveBayesClassifier.train(train_set)
print "Accuracy on test1: ", round((nltk.classify.accuracy(classifier, test_set1))*100, 2), "%"
print "Accuracy on test2: ", round((nltk.classify.accuracy(classifier, test_set2))*100, 2), "%"

print classifier.show_most_informative_features(50)