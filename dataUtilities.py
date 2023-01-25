import csv
import numpy as np
from scipy.optimize import linear_sum_assignment

def sampling(size):
    with open('train.csv', 'r') as trainFile:
        reader = csv.DictReader(trainFile)
        rows = list(reader)

    if size == 20000:
        print("Total size of sample:", len(rows))
        return rows

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

    articles = []
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if sampled[key] < sample:
                    articles.append(article)
                    sampled[key] = sampled[key] + 1
                break

    print("Total size of sample:", size)
    
    return articles

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

def jaccard(list1, list2):
    sum = 0
    for setI in list1:
        max = -1
        for setJ in list2:
            jaccardScore = len(setI.intersection(setJ)) / len(setI.union(setJ))
            if  jaccardScore > max:
                max = jaccardScore
        sum = sum + max
    return sum / len(list1)

def basicClusteringMatrix(clustering):
    sortedClustering = sorted(clustering, key=lambda x: min(x))

    elements = set()
    for cluster in sortedClustering:
        elements.update(cluster)

    elements = list(sorted(elements))
    bcm = [[int(i in cluster) for i in elements] for cluster in sortedClustering]

    return np.array(bcm)

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

def diffColumns(arr1, arr2):
    arr1 = arr1[:arr2.shape[0], :]

    diff = np.not_equal(arr1, arr2)
    diffCols = np.any(diff, axis = 0)

    return np.where(diffCols)[0]
