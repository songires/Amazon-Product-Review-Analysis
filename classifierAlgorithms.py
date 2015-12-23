from sklearn.metrics import classification_report, accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
import codecs
from random import shuffle
import numpy as np
from numpy import array
import sys
import nltk
from nltk.tokenize import word_tokenize # or use some other tokenizer
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

class Classifier:
    """
    Generic classifier interface; returns random classification
    """
    
    def __init__( self, filename):
        """ Params can contain any useful parameters for the algorithm """
    
        
            
class NaiveBayes(Classifier):

    def __init__( self , filename):
        self.filename = filename
                
    def read_file_data(self, total):
        print "*********", total
        print self.filename

        #with codecs.open("features1.txt", "r", "utf-8") as my_file:
        #    lines = [next(my_file) for x in xrange(600)]
    
        f = codecs.open(self.filename, "r", "utf-8")
        lines = f.readlines()

        data_tuples = []
    
        for line in lines:
            try:
                tup = (line.split("\t")[1].lower(), line.split("\t")[0])
                data_tuples.append(tup)
            except:
                continue
    
        return data_tuples
    
    def runClassifier(self, total, split):
        
        data_tuples = self.read_file_data(total)

        all_words = set(word for review in data_tuples for word in word_tokenize(review[0]))
        featuresets = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in data_tuples]
        
        train_set, test_set1 = featuresets[:split], featuresets[split:]
        print "train_set:", len(train_set)#, type(train_set), train_set[0]
        print "test_set:", len(test_set1)
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print "Accuracy on test1: ", round((nltk.classify.accuracy(classifier, test_set1))*100, 2), "%"
        
        print classifier.show_most_informative_features(50)

class SVM(Classifier):

    def __init__( self , filename):
        self.filename = filename
        
    def read_file_data(self , total):

        #with codecs.open(self.filename, "r", "utf-8") as my_file:
        #    lines = [next(my_file) for x in xrange(600)]
        f = codecs.open(self.filename, "r", "utf-8")
        lines = f.readlines()

        data_tuples = []
    
        for line in lines:
            try:
                tup = (line.split("\t")[0], line.split("\t")[1].lower())
                data_tuples.append(tup)
            except:
                continue
    
        return data_tuples
    
    
    def get_three_column_data_dict(self, emotion_lines):
        shuffle(emotion_lines)
    
        classes = ['0','1']
        my_data = {pair[0]: [] for pair in emotion_lines}
    
        for cat in classes:
            for pair in emotion_lines:
                if pair[0] == cat:
                    my_data[pair[0]].append(pair[1])
        return my_data
    
    
    # Print some stats:
    def get_data_stats(self, data):
        major_class = max([len(data[k]) for k in data])
        total_count = sum([len(data[k]) for k in data])
        #print "Majority class count: ", major_class
        #print "Total data point count: ", total_count
        #print "Majority class % in train data: ", round((major_class / float(total_count)) * 100, 2), "%"
        #print "*" * 50, "\n"
    
    
    def get_labels_and_vectors(self, data_tuples):
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
    
    
    def get_space(self, vectors):
        # get the dictionary of all words in train; we call it the space as it is the space of features for bag of words
        space = {}
        for dataPoint in vectors:
            words = dataPoint
            for w in words:
                if w not in space:
                    space[w] = len(space)
        return space
    
    
    def get_one_hot_vectors(self, ids, labels, vectors, space):
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
    
    
    def get_one_hot_vectors_and_labels(self, one_hot_vectors_dict):
        vectors = array([one_hot_vectors_dict[k][0] for k in one_hot_vectors_dict])
        labels = array([one_hot_vectors_dict[k][1] for k in one_hot_vectors_dict])
        return vectors, labels

    def runClassifier(self, total, split):
        data_tuples = self.read_file_data(total)
       # print "Length of data tuples is: ", len(data_tuples)
        shuffle(data_tuples)
    
        train_tuples = data_tuples[:split]
        test_tuples = data_tuples[split:]
    
        data = self.get_three_column_data_dict(data_tuples)
    
        total_count = sum([len(data[k]) for k in data])
       # print "total count: ", total_count
    
#         self.get_data_stats(data)
    
        ids, labels, vectors = self.get_labels_and_vectors(train_tuples)
    
        space = self.get_space(vectors)
        one_hot_vectors = self.get_one_hot_vectors(ids, labels, vectors, space)
    
        vectors, labels = self.get_one_hot_vectors_and_labels(one_hot_vectors)
    
        train_vectors = vectors
        train_labels = labels
    
        del vectors
        del labels
    
        print train_vectors
        
        clf = SVC(kernel='linear', gamma=1, verbose=False, probability=False)
        clf.fit(train_vectors, train_labels)

        #print ".............", train_vectors
        #visuals
   
        w = clf.coef_[0]

        print '*' * 50
        print(w)

        a = - w[1] / w[2]

        xx = np.linspace(0,3)
        yy = a * xx - clf.intercept_[0] / w[1]
        h0 = plt.plot(xx, yy, 'k-', label="non weighted div")


        plt.scatter( train_vectors[:, 0], train_vectors[:, 1], c = train_labels)
        plt.legend()
        plt.show()
   
        print "\nDone fitting classifier on training data...\n"
        del train_vectors
        del train_labels
    
        ids, labels, vectors = self.get_labels_and_vectors(test_tuples)
        one_hot_vectors = self.get_one_hot_vectors(ids, labels, vectors, space)
        vectors, labels = self.get_one_hot_vectors_and_labels(one_hot_vectors)
        
        '''
        w = clf.coef_[0]
        print '*' * 50
        print(w)

        a = -w[0] / w[1]

        xx = np.linspace(0,8)
        yy = a * xx - clf.intercept_[0] / w[1]

        h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

        plt.scatter(test_vectors[:, 0], test_vectors[:, 1], c = test_labels)
        plt.legend()
        plt.show()
        '''

        del one_hot_vectors
        test_vectors = vectors
        test_labels = labels
        predicted_test_labels = clf.predict(test_vectors)
    
        print "Done predicting on DEV data...\n"
        print "classification_report:\n", classification_report(test_labels, predicted_test_labels)
        print "accuracy_score:", round(accuracy_score(test_labels, predicted_test_labels), 2)

