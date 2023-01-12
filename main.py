import os
from dataUtilities import sampling, makeSets, jaccard
import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt


size = 1000
articles = sampling(size)
if os.path.isfile("graph.gml"):
    graph = nx.read_gml("graph.gml")
else:
    from generateGraph import generateGraph
    graph = generateGraph(articles)
    nx.write_gml(graph, "graph.gml")

communities = community_louvain.best_partition(graph)
numCommunities = max(communities.values()) + 1

commSets = list(range(numCommunities))
for commID in range(numCommunities):
    nodes = list(filter(lambda i: communities[i] == commID, communities))
    commSets[commID] = set([int (articles[int (article)]['ID']) for article in nodes])

trueSets = makeSets(articles)

print(jaccard(trueSets, commSets))
