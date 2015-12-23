import json
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from __builtin__ import int

client = MongoClient()
database = client.small_database
document = database.document
tokenizer = RegexpTokenizer(r'\w+')

path = "reviews_Cell_Phones_and_Accessories1.json"

stopwords = stopwords.words('english')



def populate_database():
	with open(path) as f:
		for line in f:
			document.insert_one(json.loads(line)).inserted_id

def clear_database():
	database.document.remove()

populate_database()

counter = 1
hashmap = {}
local_count = {}


f = open('wordpos_train.txt','w')


for res in database.document.find({"helpful": {'$ne' : '[ 0, 0 ]'}},{"_id":0,"reviewText":1, "overall":1, "helpful":1}):
	
	local_count.clear()

	string = str(res["reviewText"])
	tokens = tokenizer.tokenize(res["reviewText"])
	pos = nltk.pos_tag(tokens, tagset = "universal")
	for i in pos:
		key = str(i[0])+"_"+str(i[1])
		if(key not in hashmap) and i[0] not in stopwords:
			hashmap[key] = counter
			counter += 1

	print hashmap
	for i in pos:
		key = str(i[0])+"_"+str(i[1])
		if key in local_count:
			local_count[key] += 1
		elif key not in local_count and i[0] not in stopwords:
			local_count[key] = 1

	line = "0"


	if(int(res["overall"])>=2.5):
		line = '1'

	for i in local_count:
		line = line+" "+str(hashmap[i])+':'+str(local_count[i])


	line = line + '\n'
	f.write(line)


#print hashmap

f.close()

