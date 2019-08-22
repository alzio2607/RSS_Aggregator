from itertools import repeat

from rssa.dal import MySql, Thumbnail
from rssa.utils.constants import *
from rssa.utils import DSU
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import pandas as pd
from multiprocessing import Pool
from operator import itemgetter
def get_graph(df):
    embeddings = None
    use_module = hub.Module(USE_MODEL_PATH)
    df['text'] = df['title'] + ' ' + df['summary']
    df = df[df['text'].apply(lambda x : isinstance(x, str) and len(x) >= MINIMUM_CHARACTER_THRESHOLD)]
    df['text'] = df['text'].apply(lambda x : x[:MAXIMUM_CHARACTER_THRESHOLD])
    df = df.reset_index(drop=True)
    with tf.Session() as sess:
        sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
        embeddings_tf = use_module(df['text'].values)
        embeddings = sess.run(embeddings_tf)
    similarities = cos_sim(embeddings)
    edges = np.argwhere(similarities >= SIMILARITY_THRESHOLD)
    weights = [(u,v,similarities[u,v]) for u,v in edges]
    weights.sort(key = itemgetter(2), reverse=True)
    return weights

def dfs(graph, node, visited, temp):
    visited[node] = True
    temp.append(node)
    for next in graph[node]:
        if visited[next] == False:
            dfs(graph, next, visited, temp)

def get_connected_components(weights, n):
    dsu = DSU(n)
    for u,v,w in weights:
        if dsu.size(u) + dsu.size(v) <= MAXIMUM_CLUSTER_SIZE:
            dsu.connect(u, v)
    return dsu.get_components()

def process_component(df):
    df['publish_ts'] = df['publish_ts'].astype(str)
    return dict(
        publish_ts=df['publish_ts'].min(),
        publisher_count=len(df),
        ids=','.join(df['id'].values),
        thumbnail=Thumbnail(df['thumbnail_link'].values, df.iloc[0]['title']).get_blob()
    )

def get_clusters(components, df):
    chunks = []
    for component in components:
        chunks.append(df.iloc[component].sort_values(by='publish_ts', ascending=False))
    threadpool = Pool(processes=4)
    clusters = threadpool.map(process_component, chunks)
    return clusters

def process_category(category):
    sql = MySql()
    df = sql.read_latest_ts(category)
    print('read done')
    ts = df.iloc[0]['ts']
    weights = get_graph(df)
    print('graph created')
    components = get_connected_components(weights, len(df))
    print('components identified')
    clusters = get_clusters(components, df)
    print('clusters made')
    clusterDf = pd.DataFrame(clusters)
    clusterDf['category'] = category
    clusterDf['ts'] = ts
    sql.write(clusterDf, 'clusters')

def create_clusters():
    for category in CATEGORIES:
        print("{} STARTED".format(category))
        process_category(category)
        print("{} DONE".format(category))