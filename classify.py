import pandas as pd
import nltk
import re
from random import shuffle

# DataFrame From from Data.xls
df = pd.read_excel('Data.xls',sheet_name="Data")
#drop any row that is missing the target col
df = df.dropna(how='any',subset=['Type'])

#Might need to drop any other rows that you don't want to include or modify some of the catigories from the orignal
#or you can ignore if the orginal data is good to go
#
#TypeTranslation = pd.read_excel('Data.xls',sheet_name="DataTranslation",index_col="Name")
#TranslationLookUp = TypeTranslation['Action'].to_dict()
#def Translate(x):
#    CurrentType = x['Type']
#    if CurrentType in list(TranslationLookUp.keys()):
#        x['Type'] = TranslationLookUp[CurrentType]
#    if x['Type'] != 'Drop' and type(x['Summary']) == type(""):
#        return x
#
#df = df.apply(Translate,axis=1).dropna(how='all')
#print(len(df))

#some cleanup
def cleanup(x):
    x = x.lower()
    x = x.replace('can\'t','cant')
    x = x.replace('&','and')
    x = x.replace('re:','')
    x = x.replace('fw:','')
    #FixDates
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/20[1-2][0-9]', '[date]', x)
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/[1-2][0-9]', '[date]', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-20[1-2][0-9]', '[date]', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-[1-2][0-9]', '[date]', x)
    return x
 
df['SummaryClean'] = df.Summary.apply(cleanup)

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
featuresets = []
for index, row in df.iterrows():
    featuresets.append((row['Features'], row['Type']))
shuffle(featuresets)
 
#Split into test groups
train_set = featuresets[1900:]
testing_set = featuresets[:1900]

#NaiveBayesClassifier
bayesclassifier = nltk.NaiveBayesClassifier.train(train_set)
bayesclassifier.show_most_informative_features(200)
print("Classifier accuracy percent:",(nltk.bayesclassifier.accuracy(classifier, testing_set))*100)

#DecisionTreeClassifier
dtclassifer = nltk.DecisionTreeClassifier.train(train_set)
dtclassifer.show_most_informative_features(200)
print("Classifier accuracy percent:",(nltk.classify.accuracy(dtclassifer, testing_set))*100)
