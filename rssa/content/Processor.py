from itertools import repeat

from rssa.dal import MySql, Thumbnail
from rssa.utils.constants import *
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import pandas as pd
from multiprocessing import Pool
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
    graph = {i:[] for i in range(len(df))}
    for x in edges:
        if x[0] != x[1]:
            graph[x[0]].append(x[1])
            graph[x[1]].append(x[0])
    return graph

def dfs(graph, node, visited, temp):
    visited[node] = True
    temp.append(node)
    for next in graph[node]:
        if visited[next] == False:
            dfs(graph, next, visited, temp)

def get_connected_components(graph):
    n = len(graph)
    visited = [False] * n
    cc = []
    for node in range(n):
        if visited[node] == False:
            temp = []
            dfs(graph, node, visited, temp)
            cc.append(temp)
    return cc

def process_component(df):
    df['publish_ts'] = df['publish_ts'].astype(str)
    return dict(
        publish_ts=df['publish_ts'].min(),
        publisher_count=len(df),
        ids=','.join(df['id'].values),
        thumbnail=Thumbnail(df['thumbnail_link'].values).get_blob()
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
    graph = get_graph(df)
    print('graph created')
    components = get_connected_components(graph)
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