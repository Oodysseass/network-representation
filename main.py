import csv
from itertools import islice

from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

import networkx as nx
from networkx.algorithms import community


nodes = 100 

with open('train.csv', 'r') as trainFile:
    reader = csv.DictReader(trainFile)

    rows = list(islice(reader, nodes))

model = SentenceTransformer('all-MiniLM-L6-v2')

graph = nx.Graph()
for i in range(nodes):
    graph.add_node(i)

for i in range(nodes):
    for j in range(i, nodes):
        vectors = model.encode([rows[i]['ABSTRACT'], rows[j]['ABSTRACT']])
        count = 0
        for ii in range(len(vectors[0])):
            if vectors[0][ii] < vectors[1][ii] + 0.1 and vectors[0][ii] > vectors[1][ii] - 0.1:
                count = count + 1
        
        similarity = count / len(vectors[0])
        if similarity > 0.86:
            graph.add_edge(i, j)

communities = community.asyn_fluidc(graph, 6)

for c in communities:
    print(c)
    for i in c:
        for key in rows[i]:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and rows[i][key] == '1':
                print(key)
