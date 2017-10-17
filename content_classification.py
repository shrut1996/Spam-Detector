#!/usr/bin/python

import sys
import os
import re
import json
import string
from math import log
import nltk
# from nltk.stem import SnowballStemmer
# sb = SnowballStemmer('english')

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

spam_count = {}
ham_count = {}

class_dict = {}
model_words_count = {}


def buildWordVectorModel(path):
    # There are two kinds of models
    # 1) Binary representation, indicating presence/absence of words in doc so a word will only be counted once
    # 2) Continuous features, where the word frequency is counted

    print 'Vectorizing the bag of words'
    dirs = os.listdir(path)
    for class_name in dirs:
        for f in os.listdir(os.path.join(path, class_name)):
            document = os.path.join(path, class_name, f)
            fle = open(document, 'r')
            words = fle.read().split()
            distinct_words = sorted(set(words))
            distinct_words = [i.lower() for i in distinct_words if i.lower() not in stop_words]
            distinct_words = [s.translate(None, string.punctuation) for s in distinct_words]
            distinct_words = [re.sub(r'\d+', '', x) for x in distinct_words]
            distinct_words = filter(None, distinct_words)
            distinct_words = [reduce(lambda x,y: x+y if x[-2:] != y*2 else x, s, "") for s in distinct_words]
            distinct_words = [item for item in distinct_words if len(item) < 10]
            # distinct_words = [sb.stem(item) for item in distinct_words]
            for word in distinct_words:
                class_dict[class_name]['word_counts'][word]['frequency_count'] = class_dict.setdefault(class_name, {}).setdefault('word_counts', {}).setdefault(word, {}).setdefault('frequency_count', 0) + words.count(word)
                class_dict[class_name]['word_counts'][word]['presence_count'] = 1
            # print distinct_words
            class_dict[class_name]['total_count'] = class_dict.setdefault(class_name, {}).setdefault('total_count', 0) + 1


# laplace smoothing for word count
def wordPresenceLogProb(word, output_class):
    model_words_count = len(class_dict.get('spam').get('word_counts')) + len(class_dict.get('notspam').get('word_counts'))
    return log(float(class_dict[output_class]['word_counts'].get(word, {}).get('presence_count', 0) + 1.0) / (class_dict[output_class]['total_count'] + model_words_count))


# laplace smoothing for word count
def wordFrequencyLogProb(word, output_class):
    model_words_count = len(class_dict.get('spam').get('word_counts')) + len(class_dict.get('notspam').get('word_counts'))
    return log(float(class_dict[output_class]['word_counts'].get(word, {}).get('frequency_count', 0) + 1.0) / (class_dict[output_class]['total_count'] + model_words_count))


def getProb(output_class):
    total_count = 0
    for key in class_dict.keys():
        total_count = total_count + class_dict[key]['total_count']
    return log(float(class_dict[output_class]['total_count'])/total_count)


def predWithWordPresence(document):
        f =open(document, 'r')
        contents = f.read()
        words = set(contents.split())
        max_prob = -sys.maxint
        prob_class = None
        for output_class in ('spam', 'notspam'):
            prob = getProb(output_class)
            for word in words:
               prob = prob + wordPresenceLogProb(word, output_class)
            if prob > max_prob:
                max_prob = prob
                prob_class = output_class
        return prob_class


def predictWithWordFreq(document):
    fle = open(document, 'r')
    contents = fle.read()
    words = contents.split()
    max_prob = -sys.maxint
    prob_class = None
    for output_class in ('spam', 'notspam'):
        prob = getProb(output_class)
        for word in words:
            prob = prob + wordFrequencyLogProb(word, output_class)
        if prob> max_prob:
            max_prob = prob
            prob_class = output_class
    return prob_class


def train(path, model_file):
    print 'Training Naive Bayes Algorithm for the training data'
    buildWordVectorModel(path)
    saveToFile(model_file)


def predict(path, model_file):
    loadFromFile(model_file)
    dirs = os.listdir(path)
    total_test_cases = 0
    correct_predictions =0
    print 'Predicting using the word presence model : '
    for class_name in dirs:
        for f in os.listdir(os.path.join(path, class_name)):
            document = os.path.join(path, class_name, f)
            total_test_cases += 1
            predicted_class = predWithWordPresence(document)
            # print "Prediction for %s is %s" % (document, predicted_class)
            if predicted_class == class_name:
                correct_predictions += 1
    print 'Total test emails: %d ' % total_test_cases
    print 'Correctly classified: %d ' % correct_predictions
    print 'Accuracy : ', float(correct_predictions) / float(total_test_cases) * 100, '%'
    print ''

    total_test_cases = 0
    correct_predictions = 0
    print 'Predicting the word frequencies model : '
    for class_name in dirs:
        for f in os.listdir(os.path.join(path, class_name)):
            document = os.path.join(path, class_name, f)
            total_test_cases += 1
            predicted_class = predictWithWordFreq(document)
            # print "Prediction for %s is %s" % (document, predicted_class)
            if predicted_class == class_name:
                correct_predictions += 1
    print 'Total test emails: %d ' % total_test_cases
    print 'Correctly classified: %d ' % correct_predictions
    print 'Accuracy : ', float(correct_predictions) / float(total_test_cases) * 100, '%'
    print ''


def saveToFile(file_name):
    print 'Saving model to the storage json file'
    print ''
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    fle = open(file_name, 'w+')
    json.dump({'class_dict': class_dict}, fle, sort_keys=True, indent=4, ensure_ascii=False, encoding="utf-8")


def loadFromFile(file_name):
    print 'Loading model from the storage json file'
    print ''
    fle = open(file_name, 'r')
    model = json.load(fle, encoding="ISO-8859-1")
    class_dict = model['class_dict']
    model_words_count = len(class_dict.get('spam').get('word_counts')) + len(
        class_dict.get('notspam').get('word_counts'))


train('dataset/train', 'util/StorageUtil.json')
predict('dataset/test', 'util/StorageUtil.json')
