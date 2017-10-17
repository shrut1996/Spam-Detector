# Phishing Detector 

The work done is towards my Study Project CS F266. Dataset has been split into the training and testing sets on which email content  processing and url feature extraction is performed. Two methods were used while vectorizing the bag of words of which firstly finding the presence of a certain word in an email and secondly finding the frequncy of a certain word in an email whereas for the url analysis a simple support vector machine has been utilized till now. The results for content classifications are:

| Model           | Accuracy 
| :-------------: |:-------------:|
| Word Presence   | 88.05%        |
| Word Frequency  | 83.71%        |

The results for URL classifications are:

| Model           | Accuracy 
| :-------------: |:-------------:|
| SVM             | 91.21%        |

## Aim
Retrieving information from inbox emails and performing NLP on the collected dataset. Various techniques utilized to detect any sort of phishing behaviour such as using a probabilistic algorithm over the email content and supervised multivariate classifcation for the URL analysis on any links provided for a better performance.

## References

> https://hackernoon.com/how-to-build-a-simple-spam-detecting-machine-learning-classifier-4471fe6b816e

> http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7346927

> Phishing Emails Dataset picked up from https://archive.ics.uci.edu/ml/machine-learning-databases/00327


