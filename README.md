# Spam Detector

The dataset has been split into the training and testing sets on which mail body text processing, url feature extraction and header file processing is performed separately. Two methods used while vectorizing the bag of words were: finding the presence of a certain word in the text and finding the frequncy of a certain word, further a probabilistic algorithm is used on the email content to distinguish between spam/non-spam. 

Whereas for the url classification, certain features have been extracted from the url performed in the url_analysis file. After a basic study, it was found that the LinearSVM and the Random Forest Algorithms were to be used on the links provided in the email for better performances.

* The results for content classifications were:

| Model           | Accuracy      |
| :-------------: |:-------------:|
| Word Presence   | 88.05%        |
| Word Frequency  | 83.71%        |

* The performance for the URL classifications were:

| Model           | Accuracy      | F1-Score  |
| :-------------: |:-------------:|:---------:|
| LinearSVM       | 91.23%        | 0.869     |
| Random Forest   | 88.89%        | 0.829     |


## References

> http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7346927

> Phishing Emails Dataset picked up from https://archive.ics.uci.edu/ml/machine-learning-databases/00327


