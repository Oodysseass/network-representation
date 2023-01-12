import csv
import math
import numpy as np
from sentence_transformers import SentenceTransformer
import networkx as nx

def generateGraph(articles):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    nodes = range(len(articles))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    embeddings = {i: model.encode(articles[i]['ABSTRACT']) for i in range(len(articles))}
    nx.set_node_attributes(graph, embeddings, 'Embedding')

    embeddings = nx.get_node_attributes(graph, 'Embedding')

    for i in range(len(articles)):
        #for key in articles[i]:
        #    if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and articles[i][key] == '1':
        #        print("Checking for:", key)
        embeddingI = embeddings[i]
        for j in range(i + 1, len(articles)):
            embeddingJ = embeddings[j]
            similarity = 1 / (1 + np.linalg.norm(embeddingI - embeddingJ))

        #    for key in articles[j]:
        #        if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and articles[j][key] == '1':
        #            print(key)
        #    print(i, '-', j, ':', similarity)

            if similarity > 0.43:
                graph.add_edge(i, j)
        #print()

    nx.set_node_attributes(graph, "", 'Embedding')

    return graph

def sampling(size):
    with open('train.csv', 'r') as trainFile:
        reader = csv.DictReader(trainFile)
        rows = list(reader)

    if size == 20000:
        return rows

    while size % 6 != 0:
        size = size + 1

    sample = size / 6
    sampled = {
        'Computer Science': 0,
        'Physics': 0,
        'Mathematics': 0,
        'Statistics': 0,
        'Quantitative Biology': 0,
        'Quantitative Finance': 0
    }

    articles = list(range(size))
    j = 0
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if sampled[key] < sample:
                    articles[j] = article 
                    j = j + 1
                    sampled[key] = sampled[key] + 1
                break

    print("Total size of sample:", size)
    
    return articles