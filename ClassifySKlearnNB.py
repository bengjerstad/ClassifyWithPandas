print("Progress: Loading imports")

import pandas as pd
import nltk
import re
from random import shuffle
import pickle
import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

print("Progress: Loading Data")
# DataFrame from Data.xls
df = pd.read_csv('Data.csv')

#print(df.keys())
#drop any row that is missing the target col
df = df.dropna(how='any',subset=['TYPE'])
print(len(df))
#Might need to drop any other rows that you don't want to include or modify some of the categorizes from the original
#or you can ignore if the original data is good to go

#Clean Up Data Here

#some cleanup
def cleanup(x):
    x = x.lower()
    x = x.replace('can\'t','cant')
    x = x.replace('can not','cant')
    x = x.replace('cc&b','ccb')
    x = x.replace('account number','acct#')
    x = x.replace('account#','acct#')
    x = x.replace('active directory','ad')
    x = x.replace('pl/sql','plsql')
    x = x.replace('oracle access manager','oam')
    x = x.replace('e-business','ebusiness')
    x = x.replace('e business','ebusiness')
    x = x.replace('e-cis','ecis')
    x = x.replace('&','and')
    x = x.replace('please ','')
    x = x.replace('can you ','')
    x = x.replace('re: ','')
    x = x.replace('re:','')
    x = x.replace('fw: ','')
    x = x.replace('fw:','')
    x = x.replace('2018','RYear')
    x = x.replace('2019','RYear')
    x = x.replace('2020','RYear')
    x = x.replace('2021','RYear')
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/20[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-20[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-[1-2][0-9]', 'RDate', x)
    x = re.sub(r'\b\d{5}?\b', 'FiveDig', x)
    x = re.sub(r'\b\d{10}?\b', 'TenDig', x)
    x = x.replace(' - ',' ')
    return x
    
print("Progress: CleanUp")
df['TASKClean'] = df.TASK.apply(cleanup)

#Save Cleaned To review Later
df.to_csv("Cleaned.csv")

df['TASKToken'] = df['TASKClean'].apply(nltk.word_tokenize)

#might be cool to check it out:
#from nltk.stem import PorterStemmer
#stemmer = PorterStemmer()
#df['TASKToken'] = df['TASKToken'].apply(lambda x: [stemmer.stem(y) for y in x])
#Ref:  https://stackabuse.com/the-naive-bayes-algorithm-in-python-with-scikit-learn

# This converts the list of words into space-separated strings
df['TASKToken'] = df['TASKToken'].apply(lambda x: ' '.join(x))

count_vect = CountVectorizer()
counts = count_vect.fit_transform(df['TASKClean']).toarray()

X_train, X_test, y_train, y_test = train_test_split(counts, df['TYPE'], test_size=0.1, random_state=23)
model = MultinomialNB().fit(X_train, y_train)
predicted = model.predict(X_test)
print(np.mean(predicted == y_test))

test = "Test the input"
print(test+': ',model.predict(count_vect.transform([cleanup(test)]))[0]," Expect: OutPut")

print("Progress: Saving Module")
save_classifier = open("SKNBmodel.pickle","wb")
pickle.dump(model, save_classifier)
save_classifier.close()
save_classifier = open("SKNBcounts.pickle","wb")
pickle.dump(count_vect, save_classifier)
save_classifier.close()
