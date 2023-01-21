import csv

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
    j = 0
    for article in rows:
        for key in article:
            if key in ['Computer Science', 'Physics', 'Mathematics', 'Statistics', 'Quantitative Biology', 'Quantitative Finance'] and article[key] == '1':
                if sampled[key] < sample:
                    articles.append(article)
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