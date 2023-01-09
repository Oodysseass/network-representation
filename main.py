import csv
import math

import numpy as np
from sentence_transformers import SentenceTransformer

import networkx as nx
from networkx.algorithms import community


with open('train.csv', 'r') as trainFile:
    reader = csv.DictReader(trainFile)

    rows = list(reader)

model = SentenceTransformer('all-MiniLM-L6-v2')

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

sample = 500
for key in percentages:
    percentages[key] = math.ceil((percentages[key] / 20000) * sample)

nodes = 0
for key in percentages:
    nodes = nodes + percentages[key]

print(percentages)
print(nodes)

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

graph = nx.Graph()
for i in range(nodes):
    graph.add_node(i)

for i in range(nodes):
    for j in range(i + 1, nodes):
        vectors = model.encode([articles[i]['ABSTRACT'], articles[j]['ABSTRACT']])
        similarity = 1 / (1 + np.linalg.norm(vectors[0] - vectors[1]));

        if similarity > 0.43:
            graph.add_edge(i, j)

communities = community.asyn_fluidc(graph, 6)

for c in communities:
    print(c)
    for i in c:
        for key in rows[i]:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and rows[i][key] == '1':
                print(key)