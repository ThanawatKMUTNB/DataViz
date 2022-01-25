import csv
import pandas as pd
def getHeader():
    file = open('SS_100lines.csv')
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    file.close()
    return header

def getValueByHead(head):
    with open('SS_100lines.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        i = 0
        for row in reader:
            data.append(row[head])
            i+=1
            #if i == 3: break
    return data

def showByChoose(dimention):
    data = []
    for i in dimention:
        data.append(getValueByHead(i))
    return data

def getDataWithPandas():
    df = pd.read_csv('SS_20lines.csv', encoding='windows-1252')
    return df

def getDataWithPandasByHead(head):
    df = pd.read_csv('SS_20lines.csv', encoding='windows-1252')
    return df[head]