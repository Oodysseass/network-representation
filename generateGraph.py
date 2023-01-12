import numpy as np
from sentence_transformers import SentenceTransformer
import networkx as nx

def generateGraph(articles):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    nodes = range(len(articles))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)

    embeddings = {i: model.encode(articles[i]['ABSTRACT']) for i in range(len(articles))}

    for i in range(len(articles)):
        embeddingI = embeddings[i]
        for j in range(i + 1, len(articles)):
            embeddingJ = embeddings[j]

            similarity = 1 / (1 + np.linalg.norm(embeddingI - embeddingJ))
            if similarity > 0.43:
                graph.add_edge(i, j)

    return graph