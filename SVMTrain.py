import json
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk

client = MongoClient()
database = client.test_database
document = database.document
tokenizer = RegexpTokenizer(r'\w+')

path = "reviews_Cell_Phones_and_Accessories.json"

stopwords = stopwords.words('english')



def populate_database():
    with open(path) as f:
        for line in f:
            document.insert_one(json.loads(line)).inserted_id

def clear_database():
    document.remove()

#clear_database()
#populate_database()

counter = 1
hashmap = {}
local_count = {}


f = open('svm_train_big.txt','w')


for res in database.document.find({"helpful": {'$ne' : [ 0, 0 ]}},{"_id":0,"reviewText":1, "overall":1, "helpful":1}, no_cursor_timeout = True):

    string = str(res["reviewText"])
    tokens = tokenizer.tokenize(res["reviewText"])
    pos = nltk.pos_tag(tokens, tagset = "universal")
    key = str(int(res["overall"])) + '\t'
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

