import os
from generateGraph import sampling
import networkx as nx
from community import community_louvain


size = 100
articles = sampling(size)
if os.path.isfile("graph.gml"):
    graph = nx.read_gml("graph.gml")
else:
    from generateGraph import generateGraph
    graph = generateGraph(articles)
    nx.write_gml(graph, "graph.gml")

communities = community_louvain.best_partition(graph)
numCommunities = max(communities.values()) + 1

test = {
    'Computer Science': 0,
    'Physics': 0,
    'Mathematics': 0,
    'Statistics': 0,
    'Quantitative Biology': 0,
    'Quantitative Finance': 0
}

for community in range(numCommunities):
    print("COMMUNITY", community)
    nodes = list(filter(lambda i: communities[i] == community, communities))
    for node in nodes:
        for key in articles[int (node)]:
            if key in ['Computer Science', 'Physics', 'Mathematics', \
             'Statistics', 'Quantitative Biology', 'Quantitative Finance'] \
              and articles[int (node)][key] == '1':
                test[key] = test[key] + 1
                break
    for key in test:
        if test[key] != 0:
            print(key, ":", test[key])
            test[key] = 0
    print()