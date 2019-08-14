from rssa.dal import MySql, Rss
from rssa.utils.constants import *
from itertools import chain
import pandas as pd
import time
from datetime import datetime

def fetch_single_source(row):
    data = Rss.read(row['rss'], row['thumbnail'])
    return data

def fetch(datasource = 'datasources'):
    sql = MySql()
    df = sql.read(datasource)
    content = dict()
    for category in CATEGORIES:
        print(category, end = ' ')
        start = time.time()
        _df = df[df['category'] == category]
        categoryDf = pd.DataFrame(list(chain.from_iterable(_df.apply(fetch_single_source, axis=1))))
        categoryDf['category'] = category
        categoryDf['ts'] = datetime.utcnow().strftime("%Y%m%d%H")
        content[category] = categoryDf
        print('done in {} seconds with {} entries'.format(time.time() - start, len(categoryDf)))
    return content

if __name__ == "__main__":
    res = fetch()