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
    embeddings = {i: model.encode(articles[i]['ABSTRACT'])[0] for i in range(len(articles))}
    nx.set_node_attributes(graph, embeddings, 'Embedding')

    embeddings = nx.get_node_attributes(graph, 'Embedding')

    for i in range(len(articles)):
        embeddingI = embeddings[i]
        for j in range(i + 1, len(articles)):
            embeddingJ = embeddings[j]
            similarity = 1 / (1 + np.linalg.norm(embeddingI - embeddingJ))

            if similarity > 0.43:
                graph.add_edge(i, j)

    nx.set_node_attributes(graph, "", 'Embedding')


    return graph

def sampling(size):
    with open('train.csv', 'r') as trainFile:
        reader = csv.DictReader(trainFile)

        rows = list(reader)

    percentages = {
        'Computer Science': 0,
        'Physics': 0,
        'Mathematics': 0,
        'Statistics': 0,
        'Quantitative Biology': 0,
        'Quantitative Finance': 0
    }

    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                percentages[key] = percentages[key] + 1
                break

    sample = size
    for key in percentages:
        percentages[key] = math.ceil((percentages[key] / 20000) * sample)

    nodes = 0
    for key in percentages:
        nodes = nodes + percentages[key]

    print("Total number of sample:", nodes)
    print(percentages)

    articles = list(range(nodes))
    j = 0
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if percentages[key] > 0:
                    articles[j] = article 
                    j = j + 1
                    percentages[key] = percentages[key] - 1
                break
    
    return articles