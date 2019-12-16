import pandas as pd
import nltk
import re
from random import shuffle

# DataFrame From from Data.xls
df = pd.read_excel('Data.xls',sheet_name="Data")
#drop any row that is missing the target col
df = df.dropna(how='any',subset=['Type'])

#Do some Cleanup here
#See CleanUp.py

#Tokenize:
df['SummaryToken'] = df.SummaryClean.apply(nltk.word_tokenize)

#Word distrobution and feature list:
dist = nltk.FreqDist(df['SummaryToken'].sum())
word_features = list(dist)[:3000]

#for each line, create a true/false dict
def find_features(x):
    words = set(x)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

df['Features'] = df.SummaryToken.apply(find_features)

#Create featuresets from each row:
featuresets = df[['Features','TYPE']].to_numpy()
shuffle(featuresets)
 
#Split into test groups
train_set = featuresets[1900:]
testing_set = featuresets[:1900]

#NaiveBayesClassifier
bayesclassifier = nltk.NaiveBayesClassifier.train(train_set)
bayesclassifier.show_most_informative_features(200)
print("Classifier accuracy percent:",(nltk.classify.accuracy(bayesclassifier, testing_set))*100)

#DecisionTreeClassifier
dtclassifer = nltk.DecisionTreeClassifier.train(train_set)
dtclassifer.show_most_informative_features(200)
print("Classifier accuracy percent:",(nltk.classify.accuracy(dtclassifer, testing_set))*100)

#Saved Modules for later
import pickle
save_classifier = open("naivebayes.pickle","wb")
pickle.dump(bayesclassifier, save_classifier)
save_classifier.close()
save_classifier = open("dt.pickle","wb")
pickle.dump(dtclassifer, save_classifier)
save_classifier.close()
