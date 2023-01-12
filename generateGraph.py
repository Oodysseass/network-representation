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