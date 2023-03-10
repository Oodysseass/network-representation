import os, sys
from dataUtilities import sampling, makeSets, clusteringDistance
from generateGraph import trueGraph
import networkx as nx
from community import community_louvain


if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 1254
articles = sampling(size)

# import graph if it exists, otherwise generate it
read = False
if os.path.isfile("graph.gml"):
    graph = nx.read_gml("graph.gml")
    if len(articles) == graph.number_of_nodes():
        read = True
if not read:
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

# generate gml of true graph for visualization in gephi
nx.write_gml(trueGraph(trueSets), "true-graph.gml")
