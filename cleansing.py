# This program removes sentences that contain Nim Faseleh in them
# AND it is tagged other than 'O'
# This program only prints to the stdout, make sure to redirect it to the output


def count_tag(sent,tags):
	count = 0
	for tag in tags:
		count+=sent.count(tag)
	return count

# if a sentence contains less NEs than this threshold, do not add it.
threshold = 2
tags = ['PERS','LOC','ORG']

# Let's read Nim Faseleh from input
ch = input('please enter nim faseleh')

# Read the input file
file_name = 'out.2'
file_obj = open(file_name,'r')

sentences = file_obj.read().strip().split('\n\n')
for sentence in sentences:
	if str(ch+'\t'+'PERS') in sentence or \
	   str(ch+'\t'+'ORG') in sentence or \
	   str(ch+'\t'+'LOC') in sentence:
		continue
	count = count_tag(sentence,tags)
	if count == 0:
		continue
	if count<threshold:
		continue
	else:
		print(sentence+'\n')

file_obj.close()
