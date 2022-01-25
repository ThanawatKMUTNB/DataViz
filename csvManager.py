import csv

def getHeader():
    file = open('TableauDataAnalysis/Superstore.csv')
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    file.close()
    return header

def getValueByHead(head):
    with open('TableauDataAnalysis/Superstore.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row[head])
    return data
