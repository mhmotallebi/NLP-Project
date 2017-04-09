import sys
# this code finds sentences that their primary tags matches with the tags that
# are given by our model.
# output will be printed to stdout.

output_file_name = 'test_results.txt'
#output_file_name = 'test2'
include_misc_tags = False

output_file_obj = open(output_file_name,'r')
#sentences = output_file_obj.read().strip().split('\n')
while True:
	line1 = next(output_file_obj,'END')
	if line1=='END':
		break
	line2 = next(output_file_obj,'ERROR')
	line3 = next(output_file_obj,'ERROR')
	if line2 == 'ERROR' or line3 == 'ERROR':
		print('error in reading the file, terminating')
		sys.exit(1)
	output_true = line2.strip().split()[1:]
	output_predicted = line3.strip().split()[1:]
	#print('true',output_true)
	#print('pred',output_predicted)
	if include_misc_tags==False:
		for item in output_predicted:
			if item=='MISC':
				item = 'O'
	if len(output_predicted)!=len(output_true):
		print('diff lens')
		match=False
	else:
		match = len(output_true)== sum([1 for x,y in zip(output_true,output_predicted) if x==y])
	if match:
		print(line1[3:].strip())

output_file_obj.close()


