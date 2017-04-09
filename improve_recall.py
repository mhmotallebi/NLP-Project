# (This approach is failed!)
# This program tries to extract sentences from parallel corpus (Persian side)
# which none of their words has occured in the gold training set as a tag.
import sys

gold_trainset_file_name = '../baseline-preparation/sentences_prep/train-1p-3tag.txt'
parallel_target_trainset_file_name = 'out.2.v3_thrsh_2'
output_file_name = 'out.3.v1_thrsh_2'
NE_tags = ['PERS','ORG','LOC']
NE_words_in_gold_set = set()

# First: extract all NE words from gold train set:
gold_trainset_file = open(gold_trainset_file_name,'r')
for line in gold_trainset_file:
	if len(line.strip())==0:
		continue
	try:
		word,tag = line.strip().split('\t')
	except:
		print('error in splitting this line:',line)
		sys.exit(1)	
	if tag in NE_tags:
		NE_words_in_gold_set.add(word)
gold_trainset_file.close()
print('size of NE in goldset is:', len(NE_words_in_gold_set))
parallel_target_trainset_file = open(parallel_target_trainset_file_name,'r')
parallel_sentences = parallel_target_trainset_file.read().strip().split('\n\n')
parallel_target_trainset_file.close()
output_file = open(output_file_name,'w')
for sentence in parallel_sentences:
	invalid = False
	for token in sentence.strip().split('\n'):
		word = token.strip().split('\t')[0]
		if word in NE_words_in_gold_set:
			invalid = True
			break
	if invalid:
		continue
	output_file.write(sentence+'\n\n')
output_file.close()


