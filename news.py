import json
import urllib
from pprint import pprint
import csv
import re
import time


def make_word_dict():
	word_dict = {}

	with open('SentiWordNet.txt', 'rU') as csv_file:
		lexicon = csv.DictReader(csv_file, dialect=csv.excel_tab)

		for row in lexicon:
			for word in re.split(r'#[0-9] ', row['SynsetTerms']):
				word = re.sub(r'#[0-9]', '', word)
				if float(row['PosScore']) + float(row['NegScore']) != 0:
					word_dict[word] = float(row['PosScore']) + float(row['NegScore'])
	return word_dict


def get_emotion(text):
	if text == None: #TODO learn python typing + comparisons
		return 0

	total = 0

	for word in text.split(' '):
		if word in word_dict.keys():
			total += word_dict[word]

	return total



def get_subjectivity_index(source):
	subjectivity = 0
	for x in range(1, 11):
		news = json.load(urllib.urlopen('https://newsapi.org/v2/everything?domains=' + source + '&pageSize=100&page=' + str(x) +'&apiKey=348e41366eab46dfb1221e84d6c6d8df'))
		for article in news['articles']:
			subjectivity += get_emotion(article['description']) + get_emotion(article['content'])

	return subjectivity

word_dict = make_word_dict()
print('Fox News Subjectivity Index: %0f' % get_subjectivity_index('foxnews.com'))
print('CNN Subjectivity Index: %0f' % get_subjectivity_index('cnn.com'))
print('BBC Subjectivity Index: %0f' % get_subjectivity_index('bbc.com'))
print('Reuters Subjectivity Index: %0f' % get_subjectivity_index('bbc.com'))
print('Reuters Subjectivity Index: %0f' % get_subjectivity_index('reuters.com'))
print('Wall Street Journal Subjectivity Index: %0f' % get_subjectivity_index('wsj.com'))

'''

with open('news2.json') as fp:
    for i, line in enumerate(fp):
        if "\xe2" in line:
            print i, repr(line)
'''
#TODO find out if news is actually sensational using grouping ML
#TODO do sensationality over time
#TODO use more hard science