import sys
import re

def is_aligned_well_enough(alignment_threshold, alignment_exponent):
	if alignment_exponent<=alignment_threshold:
		return True
	return False

def are_NE_translations_consecutive(word_indices):
	word_indices = [int(x) for x in word_indices.strip().split()]
	for number_ind in range(1,len(word_indices)):
		if word_indices[number_ind]-1!=word_indices[number_ind-1]:
			return False
	return True

def generate_target_trainset(english_dict,giza_output_file_name,output_file_name,alignment_threshold,sequential_words):
	giza_output_file = open(giza_output_file_name,'r')
	output_file = open(output_file_name,'w')
	dbg_counter = -1
	while True:
		dbg_counter+=1
		line1 = next(giza_output_file,'END')
		if line1 == 'END':
			# we are done!
			break
		line2 = next(giza_output_file,'ERROR')
		line3 = next(giza_output_file,'ERROR')
		if line2=='ERROR' or line3=='ERROR':
			print('something went wrong while reading the file. is # of lines of the giza file multiply of 3?')
			break

		matches=re.search('(?<=\()\d+(?=\))',line1)
		sent_number = int(matches.group(0))
		print('sent_number is:',sent_number)
		if sent_number not in english_dict: # sentence does not contain any NE, lets skip it!
			continue
		try:		
			alignment_exponent = int(line1.strip().split('e-')[1])
		except:
			print(line1)
			#sys.exit(1)
			continue
		if is_aligned_well_enough(alignment_threshold,alignment_exponent)==False:
			continue
		target_words_list = line2.split()
		word_pairs_numbers = re.findall('(?<=\(\{).*?(?=\}\))',line3)
		if word_pairs_numbers==None or len(word_pairs_numbers)==0:# a word that there is no word in the translated side for. skipping
			continue
		print(dbg_counter)
		
		source_words_list = re.sub('\(\{.*?\}\)','',line3).strip().split()
		NE_translations_are_consecutive = True
		for word_ind,word in enumerate(source_words_list):
			if word =='NULL':
				print('NULL continued')
				continue
			if word.lower() in english_dict[sent_number]:# it is an NE,so lets find all corresponding target words
				print(word_ind,len(word_pairs_numbers),line3)
				
				temp = word_pairs_numbers[word_ind].strip()
				if sequential_words:# make sure words are consecutive in the translation side for each NE
					NE_translations_are_consecutive = are_NE_translations_consecutive(temp)	
					if NE_translations_are_consecutive==False:
						break			
				if len(temp)==0:
					continue
				for number in word_pairs_numbers[word_ind].strip().split():
					target_words_list[int(number)-1] = [target_words_list[int(number)-1],english_dict[sent_number][word.lower()]]
		if NE_translations_are_consecutive==False:
			continue
		print(len(target_words_list))
		
		for word_part in target_words_list:
			if isinstance(word_part,str):# not a NE
				output_file.write(word_part + '\t' + 'O' + '\n')
			else:
				output_file.write(word_part[0] + '\t' + word_part[1] + '\n')
		output_file.write('\n')

		print('sentence',sent_number,'is done')
	giza_output_file.close()
	output_file.close()


def retreive_all_tags(tags_dict,tag_name,new_dict,sent_number):
	# for a tagged sentence, creates a dictionary that keys are NEs (each of them is exactly one word)
	# and values are their corresponding tags
	''' example:
	{u'PERSON': [u'Paul Bartlett'], u'O': [u'-LRB- Photo by', u'-RRB-']}
	=>
	{'Paul': u'PERSON', 'Barlett': u'PERSON},...} '''

	if tag_name in tags_dict:
		for item in tags_dict[tag_name]:
			for word in item.split():
				if word.lower() in new_dict and new_dict[word.lower()]!=tag_name:
					# this word is tagged twice in a sentence, ERROR!!!
					print('error, this word is tagged twice in this sentence with different tags:',word.lower(),sent_number,new_dict[word.lower()],tag_name)
					raise 'different tags for one word in a sentence'
				else:
						new_dict[word.lower()] = tag_name
	return new_dict

def load_english_tagged_sentences(tagged_sentences_file_name):
	# input: name of a file containing output of detect_NER.py where we have sentence number in one line and tags in the next line for all sentences that NEs are found and matched
	# output: a dictionary where key is the sentence number and value is another dictionary where each word is a key and its tag is the value IF the tag is LOC/PER/ORG
	tagged_sentences_dict = {}
	tagged_sentences_file = open(tagged_sentences_file_name,'r')
	while True:
		line1 = next(tagged_sentences_file,'END')
		if line1=='END':
			# reached EOF, lets continue
			break
		line2 = next(tagged_sentences_file,'ERROR')
		line3 = next(tagged_sentences_file,'ERROR')
		if line2=='ERROR' or line3=='ERROR':
			print('error in readinf NEs file. Is the file length a multiply of 3?')
			sys.exit(1)
		sentence_number = eval(line1)[1] + 1 # since giza starts from 1, let's add a 1 to this one!
		tags_dict = eval(line2)
		if u'O' in tags_dict:
			del tags_dict[u'O']
		new_sentence_dict = {}
		# for each kind of NE, add their corresponding words to the dictionary.
		try:
			retreive_all_tags(tags_dict,U'LOCATION',new_sentence_dict,sentence_number)
			retreive_all_tags(tags_dict,U'ORGANIZATION',new_sentence_dict,sentence_number)
			retreive_all_tags(tags_dict,U'PERSON',new_sentence_dict,sentence_number)
		#except "different tags for one word in a sentence":
		#	print('skipping this sentence, since there is a word in it which is tagged with two different tags')
		except:
			print('something went wrong in creating dictionary of a sentence. skipping it')
		else:
			tagged_sentences_dict[sentence_number] = new_sentence_dict


	tagged_sentences_file.close()
	return tagged_sentences_dict

def main():
	english_tagged_file_name = '../Extracted English NEs/lists-conll2003/out-v4.final'
	giza_output_file_name = '../alignment/parallel_corpus/output.en_fa.dict.A3.final'
	output_file_name = 'out.4'
	alignment_threshold = 40# To keep more similar sentences
	sequential_words = True # if an English NE is aligned with n Target Language Words, these words should be consecutive
	english_tagged_dict = load_english_tagged_sentences(english_tagged_file_name)
	#for key,val in english_tagged_dict.items():
	#	print(key,val)
	generate_target_trainset(english_tagged_dict,giza_output_file_name,output_file_name,alignment_threshold,sequential_words)

if __name__ == "__main__":
	main()
