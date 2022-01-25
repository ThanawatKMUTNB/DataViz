import csv

def getHeader():
    file = open('TableauDataAnalysis/Superstore.csv')
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    file.close()
    return header
