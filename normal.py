


'''
1. 80-20
2. adjective with one name on big database and small
3. normal all words only stop words removed
4. insert word+_+pos 
'''
import json
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk

client = MongoClient()
db = client.test_database
document = db.document
tokenizer = RegexpTokenizer(r'\w+')

path = "reviews_Cell_Phones_and_Accessories1.json"

stopwords = stopwords.words('english')



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




f = open('allwords_train.txt','w')


for res in db.document.find({},{"_id":0,"reviewText":1, "overall":1}, no_cursor_timeout=True):
	
	local_count.clear()

	string = str(res["reviewText"])
	tokens = tokenizer.tokenize(res["reviewText"])
	pos = nltk.pos_tag(tokens, tagset = "universal")
	for i in pos:
		if(i[0] not in hashmap) and i[0] not in stopwords:
			hashmap[i[0]] = counter
			counter += 1


	for i in pos:
		if i[0] in local_count:
			local_count[i[0]] += 1
		elif i[0] not in local_count and i[0] not in stopwords:
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

