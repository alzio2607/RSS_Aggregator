import re
import os
import shutil
import time
import feedparser
import pandas as pd
import schedule
from BeautifulSoup import BeautifulSoup as bs
from datetime import datetime
import numpy as np

df=  pd.read_csv("Datasources.csv")
shutil.rmtree("./Data_CSV")
catmap={}
ts = str(int(time.time()))
hflag = 1
for row in df.iterrows():
    data = row[1]
    category = data.Category
    if catmap.has_key(category):
        hflag=0
    else:
        catmap[category] = 1
        hflag =1
    publisher = data.Publisher
    print publisher
    url= data['RSS Url']
    ctype = data['content type']
    thumb  =data.Thumbnail
    thumbpath=[]
    if pd.isna(thumb):
        thumbpath=[]
    else:
        thumbpath = thumb.split(">")
    feed = feedparser.parse(url)
    posts=[]
    for post in feed.entries:
        title = post.title
        link = post.link
        if 'published' not in post.keys():
            continue
        pubdate = post.published
        summary= bs(post.summary)
        summary_text = summary.text
        thumblink=""
        if len(thumbpath)>0 and thumbpath[0] in post.keys():
            if 'summary' in thumbpath[0]:
                if summary.find('img'):
                    thumblink  = summary.img['src']
            elif 'storyimage' in thumbpath[0]:
                thumblink = post.storyimage
            elif 'media' in thumbpath[0]:
                thumblink = post[thumbpath[0]][0][thumbpath[1]]
        posts.append((publisher,title,summary_text,pubdate,link,thumblink))

    df1 = pd.DataFrame(posts,columns=['publisher','title','summary','pubdate','link','thumblink'])
    outfile = category+"_data.csv"
    outdir = "./Data_CSV/"+category+"/"+ts
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfull = os.path.join(outdir,outfile)
    print outfull
    if hflag:
        df1.to_csv(outfull,encoding = 'utf-8',mode='a',header=True,index=False)
    else:
        df1.to_csv(outfull, encoding='utf-8', mode='a', header=False,index=False)












