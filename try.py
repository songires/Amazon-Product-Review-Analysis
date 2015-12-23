<<<<<<< HEAD
import json
from pymongo import MongoClient



client = MongoClient()
db = client.test_database
document = db.document

path = "reviews_Cell_Phones_and_Accessories1.json"
with open(path) as f:
    for line in f:
        document.insert_one(json.loads(line)).inserted_id

d = document.find_one({'reviewerID': 'A3HVRXV0LVJN7'})
print d

=======
import json
from pymongo import MongoClient
import nltk
from nltk.tokenize import RegexpTokenizer

client = MongoClient()
db = client.test_database
document = db.document
tokenizer = RegexpTokenizer(r'\w+')

path = "reviews_Cell_Phones_and_Accessories1.json"

def populate_database():
	with open(path) as f:
		for line in f:
			document.insert_one(json.loads(line)).inserted_id

def clear_database():
	db.document.remove()

counter = 1
hashmap = {}
local_count = {}
f = open('train.txt','w')


for res in db.document.find({},{"_id":0,"reviewText":1, "overall":1}):
	
	local_count.clear()

	string = str(res["reviewText"])
	tokens = tokenizer.tokenize(res["reviewText"])
	pos = nltk.pos_tag(tokens)
	for i in pos:
		if i[0] == "fine":
			print "\\\\\\\\", i
		if(i[1] == "JJ" or i[1]=='JJS'):
			if(i[0] not in hashmap):
				hashmap[i[0]] = counter
				counter += 1

	for i in pos:
		if(i[1]=='JJ' or i[1]=='JJS'):
			if i[0] in local_count:
				local_count[i[0]] += 1
			else:
				local_count[i[0]] = 1
	
	line = "0"


	if(float(res["overall"])>=2.5):
		line = '1'

	for i in local_count:
		line = line+" "+str(hashmap[i])+':'+str(local_count[i])


	line = line + '\n'
	f.write(line)


#print hashmap

f.close()
>>>>>>> 9d09ffa4a46e46cee850acc9f8302fb14929c4b0
