# import the necessary packages
from sklearn import svm
import csv
import numpy as np
import pickle

fname1 = '/home/rakshit/PycharmProjects/AIProject/features_values.csv'
csvfile1 = open(fname1, 'rb')
csv_reader1 = csv.reader(csvfile1, delimiter=',')
feature_values = np.loadtxt(csvfile1, delimiter=',', dtype='uint8')

fname2 = '/home/rakshit/PycharmProjects/AIProject/features_id.csv'
csvfile2 = open(fname2, 'rb')
csv_reader2 = csv.reader(csvfile2, delimiter=',')
feature_id = np.loadtxt(csvfile2, delimiter=',', dtype='string')
print "abc"

classifier = svm.LinearSVC()
classifier.fit(feature_values, feature_id)
score = classifier.score(feature_values, feature_id)
print score
f = open('model.txt', 'wb')
s = pickle.dumps(classifier)
f.write(s)
f.close()
