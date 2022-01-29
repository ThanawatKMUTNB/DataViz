from itertools import chain
import pandas as pd
def getHead():
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    return list(df.columns)

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
    df = df[head]
    return df

def setDimentionSort(dimention):
    sortedData = getDataWithPandasByHead(dimention)
    #print(sortedData)
    new = sortedData.sort_values(by=dimention)
    new[''] = pd.Series("abc", index=new.index)
    return new

def setRowAndColumn(Row,Column):
    sortKey = Row + Column
    sortedDataByKey = setDimentionSort(sortKey)
    df = sortedDataByKey
    return df
    
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

def getAxisYName(dimention):
    k = setDimentionSort(dimention)
    head = k[dimention].drop_duplicates()
    reg2 = head.drop_duplicates()
    reg2 = reg2[::-1].values.tolist()
    return reg2

def getDataForBar(Row,Col):
    k = setDimentionSort(Row+Col)
    grouped = k.groupby(Row)
    sumK = grouped.sum()
    listsumk = sumK.values.tolist()
    oneList = list(chain.from_iterable(listsumk))
    return oneList[::-1]

def setAvgGraphX(Row,Col):
    k = setDimentionSort(Row+Col)
    k = k.T
    sumK = k.sum(axis=1)
    
dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
'''sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''

#dd = setAllDataByOneDimention("Sales")
#print(dd)

#dd = setRowAndColumn(["City","State"],["Row ID","Product ID"])
#print(dd)

dd = setDimentionSort(dimention)
print(type(dd))
