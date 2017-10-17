#!/usr/bin/python

import url_analysis as ua
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# features_train, labels_train = ua.feature_extraction('dataset/train')
# features_test, labels_test = ua.feature_extraction('dataset/test')

# features_train.to_csv('dataset/url_train_features.csv')
# features_test.to_csv('dataset/url_test_features.csv')

features_train = pd.read_csv('dataset/url_train_features.csv')
features_test = pd.read_csv('dataset/url_test_features.csv')
labels_train = np.ones(len(ua.extractURL('dataset/train').get('spam'))).tolist() + np.zeros(len(ua.extractURL('dataset/train').get('notspam'))).tolist()
labels_test = np.ones(len(ua.extractURL('dataset/test').get('spam'))).tolist() + np.zeros(len(ua.extractURL('dataset/test').get('notspam'))).tolist()


# def svc_param_selection(X, y, nfolds):
#     Cs = [0.001, 0.01, 0.1, 1, 10]
#     gammas = [0.001, 0.01, 0.1, 1]
#     param_grid = {'C': Cs, 'gamma' : gammas}
#     grid_search = GridSearchCV(svm.SVC(kernel='rbf'), param_grid, cv=nfolds)
#     grid_search.fit(X, y)
#     grid_search.best_params_
#     return grid_search.best_params_
#
# best_C, best_gamma = svc_param_selection(features_train, labels_train, 2)

clf = svm.SVC(kernel='linear')

clf.fit(features_train, labels_train)

url_true = clf.predict(features_test)

print 'Accuracy for the LinearSVM : ', accuracy_score(url_true, labels_test) * 100, '%'
