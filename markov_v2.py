from sys import argv

import random

def main():

	filename = argv[1]

	f = open(filename)
	text = f.read()
	listed_sentence = text.split()
	f.close()
	n = int(raw_input("How long is the n-gram? (0-4)"))
	d = make_dictionary(listed_sentence, n)
	rest_program(d)

def make_dictionary(listed_sentence, n):
	a = 0 
	d = {}
	key = []
	for a in range(len(listed_sentence)-n-1):
		for i in range (0, n):
			dictionary_key = listed_sentence[i + a]
			key.append(dictionary_key)
		tuple_key = tuple(key)
		# print key
		d[tuple_key] = listed_sentence[a + i + 1]
		key = []
	return d

def rest_program(d):
	keylist = d.keys()
	bigram = random.choice(keylist)
	sentence = []
	separators = ['.', '!', '?']
		
	while bigram in d:
		bigram_as_list = list(bigram)
		next_word = d.get(bigram)
		bigram_as_list.append(next_word)
		bigram = tuple(bigram_as_list[1:])
		sentence.append(next_word)
		
		sentence_as_string = ' '.join(sentence)
		if len(sentence_as_string) >= 140:
			break
			print sentence_as_string[0:140]

		if next_word[-1] in separators:# and next_word != "Mr.": 
			break

	print ' '.join(sentence)
	print len(sentence_as_string)

main()