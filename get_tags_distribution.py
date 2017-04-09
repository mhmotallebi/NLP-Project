


tagset = ['ORG','PERS','LOC']
trainset_file_name = 'out.1'

for tag in tagset:
	
	trainset_file = open(trainset_file_name,'r')
	tagged_words_dict = {}
	for line in trainset_file:
		#print(line)
		if len(line.strip())==0:
			continue
		parts = line.strip().split('\t')
		if parts[1]!=tag:# lets only keep words that have this 'tag'
			continue
		if (parts[0],parts[1]) in tagged_words_dict:
			tagged_words_dict[(parts[0],parts[1])] += 1
		else:
			tagged_words_dict[(parts[0],parts[1])] = 1
	
	print('size of',tag,'dictionary is:',len(tagged_words_dict))
	sorted_words = sorted(tagged_words_dict.items(),key=lambda x:x[1], reverse= True)
	# lets save the result in a file, in descending order.
	output_file_name = trainset_file_name + '.dist.' + tag
	output_file = open(output_file_name,'w')
	for item in sorted_words:
		output_file.write(str(item) +'\n')
	output_file.close() 
	# lets generate numbers only to use them in the excel
	numbers_output_file_name = trainset_file_name + '.dist.' + tag + '.numbers'
	numbers_output_file = open(numbers_output_file_name,'w')
	for item in sorted_words:
		numbers_output_file.write(str(item[1]) +'\n')
	numbers_output_file.close() 
	


	trainset_file.close()