
import json
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
import nltk
import classifierAlgorithms as algs

client = MongoClient()
database = client.test_database
document = database.document
tokenizer = RegexpTokenizer(r'\w+')

path = "reviews_Cell_Phones_and_Accessories.json"

def populate_database():
    with open(path) as f:
        for line in f:
            document.insert_one(json.loads(line)).inserted_id

def clear_database():
    document.remove()

#clear_database()
#populate_database()

def writeFeatureFile(filename, total):
    
    f = open(filename,'w')
    
    instances = total
    
    iter = 1
    
    for res in database.document.find({"helpful": {'$ne' : [ 0, 0 ]}},{"_id":0,"reviewText":1, "overall":1, "helpful":1, "summary":1}, no_cursor_timeout = True):
    
        if(iter>=total):
            break
        iter = iter + 1
        
        string = str(res["summary"])
        tokens = tokenizer.tokenize(res["summary"])
        pos = nltk.pos_tag(tokens, tagset = "universal")
        
        key = "0"
        
        if float(res["overall"])>2.5 :
            key = "1"
        
        key = key + '\t'
        
        for i in pos:
            key = key + str(i[0])+"_"+str(i[1]) + " "
        
        helpdegree = ""
        helpful = res["helpful"]
        if helpful[0] == helpful[1]:
            helpdegree = "high"
        elif helpful[0] == 0:
            helpdegree = "low"
        else:
            helpdegree = "medium"
        
        key = key + '\t' + helpdegree + '\n'
        
        f.write(key)
    
    f.close()

if __name__ == '__main__':
    filename = 'features12.txt'
    
    total = 600
    split = 500
    
    #writeFeatureFile(filename,total)
    
    classalgs = {
                 'Naive Bayes': algs.NaiveBayes(filename),
                 'SVM': algs.SVM(filename)
                 }
        
    for learnername, learner in classalgs.iteritems():
        print 'Running learner = ' + learnername
        # Train model
        learner.runClassifier(total, split)

