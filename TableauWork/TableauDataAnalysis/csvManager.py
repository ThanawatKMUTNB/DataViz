import pandas as pd

def getDataWithPandas():
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    return df

def setAllDataByOneDimention(Dimention): #sort each column
    data = getDataWithPandas()
    #print(type(data))
    new = data.sort_values(by=str(Dimention))
    return new

def getDataWithPandasByHead(head):
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    #data = pd.DataFrame(df,columns=[df.columns.tolist()],index=df["Row ID"])
    return df[head]

def setDimentionSort(dimention):
    sortedData = getDataWithPandasByHead(dimention)
    #print(sortedData)
    new = sortedData.sort_values(by=dimention)
    return new

'''dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''

#dd = setAllDataByOneDimention("Sales")
#print(dd)
