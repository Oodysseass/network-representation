import numpy as np
from sentence_transformers import SentenceTransformer
import networkx as nx


# generate graph based on the nlp model
def generateGraph(articles):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    nodes = range(len(articles))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)

    nodeAttributes = {node: articles[node]['ID'] for node in nodes}
    nx.set_node_attributes(graph, nodeAttributes, 'articleNum')

    embeddings = list(range(len(articles)))
    embeddings = [model.encode(article['ABSTRACT']) for article in articles]

    for i in range(len(articles)):
        embeddingI = embeddings[i]
        for j in range(i + 1, len(articles)):
            embeddingJ = embeddings[j]

            # euclidean distance similarity
            similarity = 1 / (1 + np.linalg.norm(embeddingI - embeddingJ))
            if similarity > 0.46:
                graph.add_edge(i, j, weight = 1 / similarity)

    return graph

def trueGraph(sets):
    graph = nx.Graph()

    for cluster in sets:
        for articleID in cluster:
            graph.add_node(articleID)

            for other in cluster:
                if articleID != other:
                    graph.add_edge(articleID, other)

        nodeAttributes = {articleID: articleID for articleID in cluster}
        nx.set_node_attributes(graph, nodeAttributes, 'articleNum')

    return graph
