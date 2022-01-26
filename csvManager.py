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

def isDimension(header):
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    Dimen = []
    Meas = []
    for head in df.columns:
        if (df.dtypes[head] == 'int64' or df.dtypes[head] == 'float64') and head != 'Row ID' and head != 'Postal Code':
            Meas.append(head)
        elif df.dtypes[head] == 'object' or head == 'Row ID' or head == 'Postal Code':
            Dimen.append(head)
    
    if header in Dimen:
        return True
    elif header in Meas:
        return False
    else:
        return 'No header in this file'


'''dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''

#dd = setAllDataByOneDimention("Sales")
#print(dd)

h = 'Order Date'
print(isDimension(h))
