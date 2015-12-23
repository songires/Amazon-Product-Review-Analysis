import json
from pymongo import MongoClient
import nltk
from nltk.tokenize import RegexpTokenizer

client = MongoClient()
db = client.test_database
document = db.document
tokenizer = RegexpTokenizer(r'\w+')

path = "Train_set.json"

def populate_database():
	with open(path) as f:
		for line in f:
			document.insert_one(json.loads(line)).inserted_id

def clear_database():
	db.document.remove()

counter = 1
hashmap = {}
local_count = {}


print document.count()

'''
Total = 3447275

traintotal = Total * 0.8
testtotal = Total-traintotal


q = open("Train_set.txt",'w')
p = open("Test_set.txt","w")


count = 0
with open(path) as f:
		for line in f:
			if(count<traintotal):
				q.write(str(line))
			else:
				p.write(str(line))
			count += 1

'''


f = open('Adjective_train.txt','w')


for res in db.document.find({},{"_id":0,"reviewText":1, "overall":1}, no_cursor_timeout=True):
	
	local_count.clear()

	string = str(res["reviewText"])
	tokens = tokenizer.tokenize(res["reviewText"])
	pos = nltk.pos_tag(tokens, tagset = "universal")
	for i in pos:
		#if i[0] == "fine":
			#print "\\\\\\\\", i
		if(i[1] == "ADJ"):
			if(i[0] not in hashmap):
				hashmap[i[0]] = counter
				counter += 1

	for i in pos:
		if(i[1] == "ADJ"):
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
