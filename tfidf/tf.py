
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector as sql
from nltk.corpus import stopwords
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch


db_connection = sql.connect(host='localhost', database='rss', user='root', password='Skenzo_Dev',use_pure=True)
df = pd.read_sql('SELECT * FROM sports', con=db_connection)


df['summary'] = df['summary'].str.slice(0, 256)
df = df[df.summary.str.len() >= 10].copy()

df['titlesum'] = df['title'] + "." +df['summary']

stop_words = set(stopwords.words('english'))

tfidf = TfidfVectorizer(
    min_df = 2,
    max_df = 0.5,
    stop_words = stop_words,
    ngram_range = (1,2)
)

tfidf.fit(df.titlesum)
text = tfidf.transform(df.titlesum)

print(tfidf.get_feature_names())
print (text.shape)

text = text.todense()

clustering = AgglomerativeClustering(n_clusters=None,distance_threshold=0.9,linkage='average',affinity='l2').fit(text)
brc = Birch(branching_factor=3, n_clusters=None, threshold=0.9,compute_labels=True,)

brc.fit(text)


nparray = brc.predict(text)
print (np.max(nparray))

#print (np.max(clustering.labels_))
#print (clustering.labels_)

c={}
for x in nparray:
    if x not in c.keys():
        c[x]=1
    else:
        c[x]+=1


print(sorted(c.items(), key =
             lambda kv:(kv[1], kv[0]))[::-1])

print ()


#result = np.where(clustering.labels_ == 12)[0]
result = np.where( nparray== 194)[0]
print (result)


for x in result:
    index = int(x) +1
    print ("Title: "+df.iloc[index]['title'])
    print ("Summary "+ df.iloc[index]['summary'])
    print()
    print()






