#from __future__ import unicode_literals
import ner
from time import gmtime, strftime
import sys
from nltk.tag import StanfordNERTagger

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def are_match(x,y,min_size):
	for i in range(min_size):
		if x[i]!=y[i]:
			return False
	return True


def create_NE_dict(NE_file_name):

	NE_file = open(NE_file_name,'r')
	NE_list = NE_file.read().split('\n')
	NE_file.close()

	nes = {}
	seen_counter = 0
	for NE_entry in NE_list:
		if len(NE_entry)<2:
			break
		#print(NE_entry,len(NE_entry.split()))
		if len(NE_entry.split())>2:
			if NE_entry.split()[1] in nes:
				seen_counter +=1
				nes[NE_entry.split()[1]].append((1,NE_entry.split()[2:]))
			else:
				nes[NE_entry.split()[1]] = [(1,NE_entry.split()[2:])]
		else:
			if NE_entry.split()[1] in nes:
				seen_counter +=1
				nes[NE_entry.split()[1]].append((0,''))
			else:	
				nes[NE_entry.split()[1]] = [(0,'')]
	return nes,seen_counter
####

####
def get_valid_ones(ne_dicts,en_file_name):
	ne_counter = 0
	results = []
	results_line_numbers = set()
	en_file = open(en_file_name,'r')
	en_files_lines = en_file.readlines()

	#ne_found_count = [None]*len(en_files_lines)
	ne_found_count = [[] for x in range(len(en_files_lines))]
	#for i in range(len(en_files_lines)):
	# 	ne_found_count.append([])
	for nes in ne_dicts:
		for line_ind in range(len(en_files_lines)):
			try:
				d = []
				#print(line[0])
				#line[0]=line[0].lower()
				if en_files_lines[line_ind][0].isalpha():
					line = en_files_lines[line_ind][0].lower() + en_files_lines[line_ind][1:]
				else:
					line =en_files_lines[line_ind][:].strip()
				#print(line)
				words = line.split()
				for word_ind in range(len(words)):
					if words[word_ind] in nes:
						for ne in nes[words[word_ind]]:
							if ne[0]==0:#the case that it is only one word (0,'')
								#ne_found_count[line_ind] +=1
								ne_found_count[line_ind].append([words[word_ind]])
								#d.append([words[word_ind]])
								ne_counter +=1
								results.append((words[word_ind],line_ind))
								results_line_numbers.add(line_ind)
								break
							else:# multi-word, now only supports the ones with length=2
								if are_match(ne[1],words[word_ind+1:],len(ne[1])):
									#print('YES!')
									#ne_found_count[line_ind] +=1
									#d.append(words[word_ind:])
									ne_found_count[line_ind].append(words[word_ind:])
									ne_counter +=1
									results.append((" ".join(words[word_ind:word_ind+len(ne[1])+1]),line_ind))
									word_ind+=len(ne[1])# to skip the next word!
									results_line_numbers.add(line_ind)
									break
						#if ne_counter%10==0:
						#print(ne_counter)
			except:
				print('exception,continue!')
			finally:
				pass
				#if len(d)>0:
				#	ne_found_count[line_ind].append(d)
	en_file.close()
	print("total Named Entity ords found:",ne_counter)
	return ne_found_count
	#for word in results:
		#print(word)
	#print('this many sentences contained at least one NE:',len(results_line_numbers))

def are_match(stanford_NEs, gazetteer_NEs):
	if len(stanford_NEs)!=len(gazetteer_NEs):
		return False
	#print('for gazzetteer:', gazetteer_NEs)
	for item in gazetteer_NEs:
		if unicode(item[0].lower()) not in stanford_NEs:
			return False
		#if stanford_NEs[item_ind].lower()!=unicode(gazetteer_NEs[item_ind][0]).lower():
		#	return False
	return True

def create_set(st_dict):
	res = set()
	if u'PERSON' in st_dict:
		for item in st_dict[u'PERSON']:
			for word in item.split():
				res.add(word.lower())
	if u'LOCATION' in st_dict:
		for item in st_dict[u'LOCATION']:
			for word in item.split():
				res.add(word.lower())
	if u'ORGANIZATION' in st_dict:
		for item in st_dict[u'ORGANIZATION']:
			for word in item.split():
				res.add(word.lower())
	return res

def find_the_tag(word,st_dict):
	if u'PERSON' in st_dict:
		for word_occured in st_dict[u'PERSON']:
			if word==word_occured:
				return u'PERSON'
	if u'LOCATION' in st_dict:
		for word_occured in st_dict[u'LOCATION']:
			if word==word_occured:
				return u'LOCATION'
	if u'ORGANIZATION' in st_dict:
		for word_occured in st_dict[u'ORGANIZATION']:
			if word==word_occured:
				return u'ORGANIZATION'
	return u'O'


#-------------------------------#
## select the name of the file of NEs to be extracted from sentences
## this file determines the words that are to be tagged
## (shoul be of a same tag)

NE_files = []
## old model:
#st = StanfordNERTagger('../../stanford-ner-2016-10-31/classifiers/english.conll.4class.distsim.crf.ser.gz','../../stanford-ner-2016-10-31/stanford-ner-3.7.0.jar') 
## new model which uses server to have the speed up!
st = ner.SocketNER(host='localhost', port=9000, output_format='slashTags')
print(dir(st))
#NE_file_name = 'ned.list.ORG' #--> output3
#NE_file_name = 'ned.list.PER' #--> output4
#NE_file_name = 'ned.list.LOC' #--> output5
#NE_file_name = 'ned.list.MISC' #--> output6

en_file_name = '../English Text/pc_en_tokened.txt'
only_generate_english_trainset = True # to create a file for Neural Network input for English side 
NE_files.append('ned.list.ORG')
NE_files.append('ned.list.PER')
NE_files.append('ned.list.LOC')
NE_files.append('ned.list.MISC')

ne_dicts = []
for NE_file_name in NE_files:
	ne_dict, redundant_count = create_NE_dict(NE_file_name)
	print("dict size:",len(ne_dict))
	print("redundant_count:",redundant_count)
	ne_dicts.append(ne_dict)

valid_lines = get_valid_ones(ne_dicts,en_file_name)

en_file = open(en_file_name,'r')
en_files_lines = en_file.readlines()
print("this is the length:",len(valid_lines))
#exit(1)	

print strftime("%Y-%m-%d %H:%M:%S", gmtime())
for ind in xrange(0,len(valid_lines)):
	#print(valid_lines[ind])
	#if ind%100==0:
	#	print(ind)
	#	sys.stdout.flush()
	#print(valid_lines[ind])
	if len(valid_lines[ind])>=1:# and valid_lines[ind][0][0]!='Taliban':
		#print(valid_lines[ind])
		## old model:
		#res = st.tag(en_files_lines[ind].split())
		
		## new model:
		res = st.get_entities(en_files_lines[ind])

		#print(res)
		#continue
		st_set = create_set(res)
		#total_tagged = sum([1 for x in res if x[1]!='O'])
		#tagged_words_stanford = [x[0]for x in res if x[1]!='O']
		if are_match(st_set,valid_lines[ind]):
		#if total_tagged== len(valid_lines[ind][0]):
			#print('valid:',valid_lines[ind],en_files_lines[ind])
			if only_generate_english_trainset:
				for word in en_files_lines[ind].strip().split():
					tag = find_the_tag(word,res)
					print(word+'\t'+tag)
				print()
			else:
				print('matched',ind)
				#print('ST:',tagged_words_stanford,'NE:',valid_lines[ind])
				print(res)
				print(valid_lines[ind])
				#sys.stdout.flush()
	
en_file.close()

#-----------------
'''
//The idea is to create 3 (or 4) separate dictionaries for all categories,
then, iterate over all dictionaries, and for every sentence find how many NE it has. ie:
for each dictinary:
	for each line:
		for each word(and continuation):
			if in dict[i]:
				x[line_ind]++ --> list sized len(corpus), initially zero, every match increase by 1, to have # NEs in the sentence
now, just keep and extract sentences that their
'''
