import csv
import numpy as np
from scipy.optimize import linear_sum_assignment


# samples train.csv uniformly
def sampling(size):
    with open('train.csv', 'r') as trainFile:
        reader = csv.DictReader(trainFile)
        rows = list(reader)

    # return all the articles
    if size == 20000:
        print("Total size of sample:", len(rows))
        return rows

    # make size divisible by 6
    while size % 6 != 0:
        size = size + 1

    sample = size / 6
    sampled = {
        'Computer Science': 0,
        'Physics': 0,
        'Mathematics': 0,
        'Statistics': 0,
        'Quantitative Biology': 0,
        'Quantitative Finance': 0
    }

    # sample articles and keep track of the amount
    articles = []
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if sampled[key] < sample:
                    articles.append(article)
                    sampled[key] = sampled[key] + 1
                break

    print("Total size of sample:", len(articles))
    print(sampled)

    return articles

# returns list of sets of the true clustering
def makeSets(articles):
    topics = ['Computer Science', 'Physics', 'Mathematics', \
        'Statistics', 'Quantitative Biology', 'Quantitative Finance']

    sets = [set() for _ in range(len(topics))]

    for article in articles:
        for i, topic in enumerate(topics):
            if article[topic] == '1':
                sets[i].add(int (article['ID']))
                break

    return sets

# constructs a basic clustering matrix from a list of sets
# that represents a clustering
def basicClusteringMatrix(clustering):
    sortedClustering = sorted(clustering, key=lambda x: min(x))

    elements = set()
    for cluster in sortedClustering:
        elements.update(cluster)

    elements = list(sorted(elements))
    bcm = [[int(i in cluster) for i in elements] for cluster in sortedClustering]

    return np.array(bcm)

# calculates clustering distance from basic clustering matrices
def clusteringDistance(trueClustering, predictedClustering):
    trueBCM = basicClusteringMatrix(trueClustering)
    predictedBCM = basicClusteringMatrix(predictedClustering)
    k1, n = trueBCM.shape
    k2, _ = predictedBCM.shape
    k = min(k1, k2)

    C = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            C[i, j] = np.sum(np.abs(trueBCM[i] - predictedBCM[j]))

    _, p = linear_sum_assignment(C)
    S = predictedBCM[p, :]

    return len(diffColumns(trueBCM, S))

# finds columns of two arrays with different elements
def diffColumns(arr1, arr2):
    arr1 = arr1[:arr2.shape[0], :]

    diff = np.not_equal(arr1, arr2)
    diffCols = np.any(diff, axis = 0)

    return np.where(diffCols)[0]
