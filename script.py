import os
import string
from itertools import chain
from glob import glob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import obo

path = 'H:/ml project/files'
path_token = 'H:/ml project/tokenisedfiles'
path_lower = 'H:/ml project/loweredfiles'
path_swr = 'H:/ml project/swrfiles'
path_lemm = 'H:/ml project/lemmatisedfiles'
path_wfv = 'H:/ml project/wfv'

#deleting the files to empty the above linked folders
for filename in os.listdir(path_token):
	os.remove(path_token+'/'+filename)
for filename in os.listdir(path_lower):
	os.remove(path_lower+'/'+filename)
for filename in os.listdir(path_swr):
	os.remove(path_swr+'/'+filename)
for filename in os.listdir(path_lemm):
	os.remove(path_lemm+'/'+filename)
for filename in os.listdir(path_wfv):
	os.remove(path_wfv+'/'+filename)



#tokenise the words in each file
for filename in os.listdir(path):
	with open(path+'/'+filename, 'r') as myfile:
	    data=myfile.read().replace('\n', ' ')
	with open(path_token+'/'+filename.replace(' ', '')[:-4], 'w') as out:
		for i in word_tokenize(data):
			out.write(i+" ")


#lowercasing the words in each file
for filename in os.listdir(path_token):
	lines = list(chain.from_iterable(open(f, 'r') for f in glob(path_token+'/'+filename)))
	lines = [line.lower() for line in lines]
	with open(path_lower+'/'+filename.replace(' ', '')[:-4]+"_lower", 'w') as out:
		out.writelines(lines)


#stop word removal

#stoplist1
stop_words = set(stopwords.words("english"))

#stoplist2
stoplist = set(map(chr, range(ord('a'),ord('z')+1)))
stoplist.update(set(map(str,range(1,101))))

srcfile = open('H:/ml project/stoplist.regex')
srcfile.readline()
for line in srcfile:
	stoplist.add(line[5:-4].lower().replace(']',''))

stop_words = stop_words.union(stoplist)
my_set = {'.',';',',','(',')','[',']','"','%','0',"''","``","'","=",":"}
stop_words = stop_words.union(my_set)

for filename in os.listdir(path_lower):
	with open(path_lower+'/'+filename,'r') as f:
		nf = f.read()
		with open(path_swr+'/'+filename.replace(' ', '')[:-4]+"_stopword_removed", 'w') as out:
			for word in nf.split():
				if word not in stop_words:
					out.write(word+" ")


'''

#word stemming
ps = PorterStemmer()
with open(path_edited+'/'+filename.replace(' ', '')[:-4]+"_stopword_removed",'r') as f:
	nf = f.read()
	with open(path_edited+'/'+filename.replace(' ', '')[:-4]+"_stemmed", 'w') as out:
		for word in nf.split():
			out.write(ps.stem(word)+" ")

'''


#lemmantization
lemmantizer = WordNetLemmatizer()
for filename in os.listdir(path_swr):
	with open(path_swr+'/'+filename,'r') as f:
		nf = f.read()
		with open(path_lemm+'/'+filename.replace(' ', '')[:-4]+"_lemmatized", 'w') as out:
			for word in nf.split():
				out.write(lemmantizer.lemmatize(word)+" ")



#forming word frequency vectors
for filename in os.listdir(path_lemm):
	wordlist = []
	with open(path_lemm+'/'+filename,'r') as f:
		nf = f.read()
		for word in nf.split():
			wordlist.append(word)

	dictionary = obo.wordListToFreqDict(wordlist)
	sorteddict = obo.sortFreqDict(dictionary)

	with open(path_wfv+'/'+filename.replace(' ', '')[:-4]+"_WFV", 'w') as out:
		for s in sorteddict: 
			out.write(str(s) + '\n')
