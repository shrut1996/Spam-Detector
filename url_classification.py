#!/usr/bin/python

import url_analysis as ua
import pandas as pd
import numpy as np
import math
import operator

from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# features_train, labels_train = ua.feature_extraction('dataset/train')
# features_test, labels_test = ua.feature_extraction('dataset/test')

# features_train.to_csv('dataset/url_train_features.csv')
# features_test.to_csv('dataset/url_test_features.csv')

features_train = pd.read_csv('dataset/url_train_features.csv')
features_test = pd.read_csv('dataset/url_test_features.csv')
labels_train = np.ones(len(ua.extractURL('dataset/train').get('spam'))).tolist() + np.zeros(len(ua.extractURL('dataset/train').get('notspam'))).tolist()
labels_test = np.ones(len(ua.extractURL('dataset/test').get('spam'))).tolist() + np.zeros(len(ua.extractURL('dataset/test').get('notspam'))).tolist()


# Support Vector Machine Classifier

clf = svm.SVC(kernel='linear', C=0.1)

clf.fit(features_train, labels_train)

url_true = clf.predict(features_test)

print 'Evaluation Metrics for LinearSVM are : '
print 'Accuracy score : ', accuracy_score(url_true, labels_test) * 100, '%'
print 'Precision score : ', precision_score(url_true, labels_test)
print ''

# Random Forest Classifier

clf = RandomForestClassifier(max_depth=2, random_state=0)

clf.fit(features_train, labels_train)

url_true = clf.predict(features_test)

print 'Evaluation Metrics for Random Forests are : '
print 'Accuracy score : ', accuracy_score(url_true, labels_test) * 100, '%'
print 'Precision score : ', precision_score(url_true, labels_test)
print ''