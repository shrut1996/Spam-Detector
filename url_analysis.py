#!/usr/bin/python

import re
import os
import urllib2
from xml.dom import minidom
from urlparse import urlparse

import numpy as np
import pandas as pd

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
html_tag_re = re.compile(r'<[^>]+>')


def extractURL(path):
    urlList = {'spam': [], 'notspam': []}
    dirs = os.listdir(path)
    for class_name in dirs:
        for f in os.listdir(os.path.join(path, class_name)):
            document = os.path.join(path, class_name, f)
            fle = open(document, 'r')
            words = fle.read().split()
            distinct_words = sorted(set(words))
            for word in distinct_words:
                tempWord = word.split(":")
                if len(tempWord) == 2:
                    if tempWord[0] == 'http' or tempWord[0] == 'https':
                        temp_url = urlparse(word)
                        host = temp_url.netloc
                        if html_tag_re.sub('', word) not in urlList['spam'] or html_tag_re.sub('', word) not in urlList['notspam']:
                            if class_name == 'spam':
                                urlList['spam'].append(html_tag_re.sub('', word))
                            else:
                                urlList['notspam'].append(html_tag_re.sub('', word))
            fle.close()
    return urlList


def extract_token_features(url):
    temp_url = urlparse(url)
    host = temp_url.netloc
    if url == '':
        return [0, 0, 0]
    token_word = re.split('\W+', host)
    no_element = sum_len = largest = 0
    for element in token_word:
        l = len(element)
        sum_len += l
        if element == 'http' or element == 'https':
            continue
        if l > 0:  # for empty element exclusion in average length
            no_element += 1
        if largest < l:
            largest = l
    try:
        return [round(float(sum_len)/no_element, 2), no_element, largest]
    except:
        return [0, no_element, largest]


def ip_address_presence(url):
    words = re.split('\W+', url)
    cnt = 0
    for element in words:
        if unicode(element).isnumeric():
            cnt += 1
        else:
            if cnt >= 4 :
                return 1
            else:
                cnt = 0;
    if cnt >= 4:
        return 1
    return 0


def popularity(url):
    temp_url = urlparse(url)
    host = temp_url.netloc
    xmlpath = 'http://data.alexa.com/data?cli=10&dat=snbamz&url=' + host
    print xmlpath
    try:
        xml = urllib2.urlopen(xmlpath)
        dom = minidom.parse(xml)
        rank_host = -1
        for sub in dom.getElementsByTagName('REACH'):
            if sub.hasAttribute('RANK'):
                rank_host = sub.attributes['RANK'].value
        # country=find_ele_with_attribute(dom,'REACH','RANK')
        # rank_country = find_ele_with_attribute(dom, 'COUNTRY', 'RANK')
        for sub in dom.getElementsByTagName('COUNTRY'):
            if sub.hasAttribute('RANK'):
                rank_country = sub.attributes['RANK'].value
        return [rank_host, rank_country]
    except:
        return [-1, -1]


def host_count(url, url_features):
    temp_url = urlparse(url)
    host = temp_url.netloc
    cnt = 0
    for hosts in url_features['host']:
        if hosts == host:
            cnt += 1;
    return cnt


def critical_words(url):
    words = re.split('\W+', url)
    words = [word.lower() for word in words]
    cri_words = ['adclick', 'login', 'signup', 'insurance', 'savings', 'free', 'click', 'confirm', 'account', 'banking', 'secure', 'warranty']
    cnt = 0
    for element in cri_words:
        if element in words:
            cnt += 1
    return cnt


def feature_extraction(path):
    urls = pd.Series(extractURL(path).get('spam') + extractURL(path).get('notspam'))

    # Spam/Malware = 1, Benign/Not Malware = 0
    url_labels = np.ones(len(ua.extractURL('dataset/test').get('spam'))).tolist() + np.zeros(len(ua.extractURL('dataset/test').get('notspam'))).tolist()

    url_features = pd.DataFrame()
    url_features['URLs'] = urls
    url_features['host'] = url_features['URLs'].apply(lambda x: urlparse(x).netloc)
    url_features['host_count'] = url_features['URLs'].apply(lambda x: host_count(x, url_features))
    url_features['avg_token_length'], url_features['token_count'], url_features['largest_token'] = zip(*url_features['URLs'].apply(extract_token_features))
    url_features['url_length'] = url_features['URLs'].apply(lambda x: len(x))
    url_features['ip_address'] = url_features['URLs'].apply(ip_address_presence)
    url_features['dots_count'] = url_features['URLs'].apply(lambda x: x.count('.'))
    url_features['critical_words'] = url_features['URLs'].apply(critical_words)
    url_features['host_rank'], url_features['host_country'] = zip(*url_features['URLs'].apply(popularity))

    url_features.drop(['URLs'], axis=1, inplace=True)
    url_features.drop(['host'], axis=1, inplace=True)

    return url_features, url_labels
