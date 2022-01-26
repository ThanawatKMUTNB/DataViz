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
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    return df

def getDataWithPandasByHead(head):

    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    data = pd.DataFrame(df,columns=[df.columns.tolist()],index=df["Row ID"])
    return df[head]

def setDimentionSort(data,dimention):
    sortedData = getDataWithPandasByHead(data)
    print(sortedData)
    new = sortedData.sort_values(by=dimention)
    return new

'''dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''
