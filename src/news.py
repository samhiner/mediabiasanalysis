import json
import urllib.request
from pprint import pprint
import csv
import re
import time
import numpy as np
import matplotlib.pyplot as plt


def make_word_dict():
	word_dict = {}

	with open('../data/SentiWordNet.txt', 'rU') as csv_file:
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
		news = json.load(urllib.request.urlopen('http://newsapi.org/v2/everything?domains=' + source + '&pageSize=100&page=' + str(x) +'&apiKey=9b8e51b1ad0640eba7d7c4eb99217de3'))
		for article in news['articles']:
			subjectivity += get_emotion(article['description']) + get_emotion(article['content'])

	return subjectivity

word_dict = make_word_dict()


subjectivity_indexes = {
	'fox': get_subjectivity_index('foxnews.com'),
	'cnn': get_subjectivity_index('cnn.com'),
	'bbc': get_subjectivity_index('bbc.com'),
	'reuters': get_subjectivity_index('reuters.com'),
	'wsj': get_subjectivity_index('wsj.com')
}

'''
Fox News Subjectivity Index: 5557.250000			4
CNN Subjectivity Index: 2562.250000					4
BBC Subjectivity Index: 1472.875000					0
Reuters Subjectivity Index: 3568.375000				1
Wall Street Journal Subjectivity Index: 5474.250000	2
'''


print('Fox News Subjectivity Index: %0f' % subjectivity_indexes['fox'])
print('CNN Subjectivity Index: %0f' % subjectivity_indexes['cnn'])
print('BBC Subjectivity Index: %0f' % subjectivity_indexes['bbc'])
print('Reuters Subjectivity Index: %0f' % subjectivity_indexes['reuters'])
print('Wall Street Journal Subjectivity Index: %0f' % subjectivity_indexes['wsj'])

###

pro_bias_ratings = {
	'fox': 2+2,
	'cnn': 2+2,
	'bbc': 0+0,
	'reuters': 1+0,
	'wsj': 1+1
}

plt.plot([subjectivity_indexes[x] for x in subjectivity_indexes])
#plt.ylabel([pro_bias_ratings[x] for x in pro_bias_ratings])
plt.show()

'''

with open('news2.json') as fp:
    for i, line in enumerate(fp):
        if "\xe2" in line:
            print i, repr(line)
'''
#TODO find out if news is actually sensational using grouping ML
#TODO do sensationality over time
#TODO *IMPORTANT* use more hard science
#TODO get all articles not just recent
#TODO get better database