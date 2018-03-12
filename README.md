# Spam Detector

The work done is towards my Study Project CS F266. Dataset has been split into the training and testing sets on which text processing and url feature extraction is performed. Two methods were used while vectorizing the bag of words of which firstly finding the presence of a certain word in an email and secondly finding the frequncy of a certain word in an email, further a probabilistic algorithm is used on the email content to distinguish between spam/non-spam. Whereas for the url analysis many features, based on the training set, have been used for the supervised multi-class classifcations like Linear Support Vector Machine and the Random Forest Algorithms on any links provided for a better performance.

* The results for content classifications were:

| Model           | Accuracy      |
| :-------------: |:-------------:|
| Word Presence   | 88.05%        |
| Word Frequency  | 83.71%        |

* The performance for the URL classifications were:

| Model           | Accuracy      | Precision |
| :-------------: |:-------------:|:---------:|
| LinearSVM       | 91.23%        | 0.769     |
| Random Forest   | 88.89%        | 0.708     |


## References

> http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7346927

> Phishing Emails Dataset picked up from https://archive.ics.uci.edu/ml/machine-learning-databases/00327


