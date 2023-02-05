import numpy as np
from sentence_transformers import SentenceTransformer
import networkx as nx


def generateGraph(articles):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    nodes = range(len(articles))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)

    embeddings = list(range(len(articles)))
    embeddings = [model.encode(article['ABSTRACT']) for article in articles]

    for i in range(len(articles)):
        embeddingI = embeddings[i]
        for j in range(i + 1, len(articles)):
            embeddingJ = embeddings[j]

            similarity = 1 / (1 + np.linalg.norm(embeddingI - embeddingJ))
            if similarity > 0.46:
                graph.add_edge(i, j, weight = 1 / similarity)

    return graph
