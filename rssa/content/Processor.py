from rssa.dal import MySql
from rssa.utils.constants import *
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import pandas as pd

def get_graph(df):
    embeddings = None
    use_module = hub.Module(USE_MODEL_PATH)
    df['text'] = df['title'] + ' ' + df['summary']
    df = df[df['text'].apply(lambda x : isinstance(x, str) and len(x) >= MINIMUM_CHARACTER_THRESHOLD)]
    df['text'] = df['text'].apply(lambda x : x[:MAXIMUM_CHARACTER_THRESHOLD])
    df = df.reset_index(drop=True)
    with tf.Session() as sess:
        sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
        embeddings_tf = use_module(df['text'].valu
        embeddings = sess.run(embeddings_tf)
    similarities = cos_sim(embeddings)
    edges = np.argwhere(similarities >= SIMILARITY
        _THRESHOLD)
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

def get_clusters(components, df):
    clusters = []
    for component in components:
        cluster = dict()
        _df = df.iloc[component]
        cluster['publish_ts'] = _df['publish_ts'].min()
        cluster['publisher_count'] = len(_df)
        _df.sort_values(by='publish_ts', ascending=False)
        cluster['keys'] = ','.join(_df['key'].values)
        clusters.append(cluster)
    return clusters

def process_category(category):
    sql = MySql()
    df = sql.read_latest_ts(category)
    ts = df.iloc[0]['ts']
    graph = get_graph(df)
    components = get_connected_components(graph)
    clusters = get_clusters(components, df)
    clusterDf = pd.DataFrame(clusters)
    clusterDf['category'] = category
    clusterDf['ts'] = ts
    sql.write(clusterDf, 'clusters')

def create_clusters():
    for category in CATEGORIES:
        process_category(category)