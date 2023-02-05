import os
from dataUtilities import sampling, makeSets, clusteringDistance
import networkx as nx
from community import community_louvain


size = 1254
articles = sampling(size)

# import graph if it exists, otherwise generate it
if os.path.isfile("graph.gml"):
    graph = nx.read_gml("graph.gml")
else:
    from generateGraph import generateGraph
    graph = generateGraph(articles)
    nx.write_gml(graph, "graph.gml")

# find communities based on modularity
communities = community_louvain.best_partition(graph)
numCommunities = max(communities.values()) + 1

# transform into list of sets
commSets = list(range(numCommunities))
for commID in range(numCommunities):
    nodes = list(filter(lambda i: communities[i] == commID, communities))
    commSets[commID] = set([int (articles[int (article)]['ID']) for article in nodes])

# calculate true clustering and distance
trueSets = makeSets(articles)
distance = clusteringDistance(trueSets, commSets)

print("Clustering Distance:", distance)
print("Distance / Nodes:", distance / len(articles))
