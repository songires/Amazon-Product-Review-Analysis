
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
            tup = (line.split("\t")[0], line.split("\t")[1].lower())
            data_tuples.append(tup)
        except:
            continue

    return data_tuples


def get_three_column_data_dict(emotion_lines):
    shuffle(emotion_lines)

    classes = ['neg','pos']
    my_data = {pair[0]: [] for pair in emotion_lines}

    for cat in classes:
        for pair in emotion_lines:
            if pair[0] == cat:
                my_data[pair[0]].append(pair[1])
    return my_data


# Print some stats:
def get_data_stats(data):
    major_class = max([len(data[k]) for k in data])
    total_count = sum([len(data[k]) for k in data])
    #print "Majority class count: ", major_class
    #print "Total data point count: ", total_count
    #print "Majority class % in train data: ", round((major_class / float(total_count)) * 100, 2), "%"
    #print "*" * 50, "\n"


def get_labels_and_vectors(data_tuples):
    labels = []
    vectors = []
    ids = []
    c = 0

    for dataPoint in data_tuples:
        ids.append(c)
        c += 1
        label, vector = dataPoint[0], dataPoint[1].split()
        labels.append(label)
        vectors.append(vector)
    return ids, labels, vectors


def get_space(vectors):
    # get the dictionary of all words in train; we call it the space as it is the space of features for bag of words
    space = {}
    for dataPoint in vectors:
        words = dataPoint
        for w in words:
            if w not in space:
                space[w] = len(space)
    return space


def get_one_hot_vectors(ids, labels, vectors, space):
    one_hot_vectors = {}
    triples = zip(ids, labels, vectors)

    for triple in triples:
        idd, label, data_point = triple[0], triple[1], triple[2]
        vec = np.zeros((len(space)))

        for w in data_point:
            try:
                vec[space[w]] = 1
            except:
                continue
        
        one_hot_vectors[idd] = (vec, array(label))
    return one_hot_vectors


def get_one_hot_vectors_and_labels(one_hot_vectors_dict):
    vectors = array([one_hot_vectors_dict[k][0] for k in one_hot_vectors_dict])
    labels = array([one_hot_vectors_dict[k][1] for k in one_hot_vectors_dict])
    return vectors, labels


def main():
    data_tuples = read_file_data()
   # print "Length of data tuples is: ", len(data_tuples)
    shuffle(data_tuples)

    train_tuples = data_tuples[:800]
    test_tuples = data_tuples[800:]

    data = get_three_column_data_dict(data_tuples)

    total_count = sum([len(data[k]) for k in data])
   # print "total count: ", total_count

    get_data_stats(data)

    ids, labels, vectors = get_labels_and_vectors(train_tuples)

    space = get_space(vectors)
    one_hot_vectors = get_one_hot_vectors(ids, labels, vectors, space)

    vectors, labels = get_one_hot_vectors_and_labels(one_hot_vectors)

    train_vectors = vectors
    train_labels = labels

    del vectors
    del labels

    print train_vectors
    #clf = OneVsRestClassifier(SVC(C=1, kernel='linear', gamma=1, verbose=False, probability=True))
#     clf = SVC(kernel='linear', gamma=1, verbose=False, probability=False)
    clf = SVC()
    clf.fit(train_vectors, train_labels)
    print "\nDone fitting classifier on training data...\n"
#     clf = SVC(kernel='linear', gamma=1, verbose=False, probability=False)
    #clf = SVC()
#     clf.fit(train_vectors, train_labels)
    #print "\nDone fitting classifier on training data...\n"
    gnb = GaussianNB()
    y_pred = gnb.fit(train_vectors, train_labels)
    del train_vectors
    del train_labels

    ids, labels, vectors = get_labels_and_vectors(test_tuples)
    one_hot_vectors = get_one_hot_vectors(ids, labels, vectors, space)
    vectors, labels = get_one_hot_vectors_and_labels(one_hot_vectors)
    
    del one_hot_vectors
    test_vectors = vectors
    test_labels = labels
    predicted_test_labels = clf.predict(test_vectors)

    output = y_pred.predict(test_vectors)

    print "Done predicting on DEV data...\n"
    print "classification_report:\n", classification_report(test_labels, predicted_test_labels)
    print "accuracy_score:", round(accuracy_score(test_labels, predicted_test_labels), 2)


    print "Done predicting on DEV data...$$$$$$$$$$$$$naivebayes\n"
    print "classification_report:\n", classification_report(test_labels, output)
    print "accuracy_score:", round(accuracy_score(test_labels, output), 2)

if __name__ == "__main__":
    print "Hello!!"
    main()
