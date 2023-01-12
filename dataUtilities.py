import csv
from sklearn.metrics import jaccard_similarity_score

def sampling(size):
    with open('train.csv', 'r') as trainFile:
        reader = csv.DictReader(trainFile)
        rows = list(reader)

    if size == 20000:
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

    articles = list(range(size))
    j = 0
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if sampled[key] < sample:
                    articles[j] = article 
                    j = j + 1
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
                sets[i].add(article['ID'])

    return sets

def jaccard(set1, set2):
    return jaccard_similarity_score(set1, set2)