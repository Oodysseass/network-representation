import csv
from itertools import islice


nodes = 100

with open('train.csv', 'r') as trainFile:
    reader = csv.DictReader(trainFile)

    rows = list(islice(reader, nodes))

keys = list(rows[0].keys())

for key in range(3, 9):
    print(keys[key])
    for dictionary in rows:
        if dictionary[keys[key]] == '1':
            print(int(dictionary['ID']) - 1)
