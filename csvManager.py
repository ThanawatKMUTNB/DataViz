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

def setRowAndColumn(Row,Column):
    sortKey = Row + Column
    #sortedRow = setDimentionSort(Row)
    sortedDataByKey = setDimentionSort(sortKey)
    #print(sortedRow)
    #print(sortedCol)
    #print(pd.DataFrame(sortedDataByKey))
    #df = sortedDataByKey.set_index(Column, Row)
    #df = sortedDataByKey.pivot_table(index=Row, columns=Column).swaplevel(axis=1).sort_index(1)
    
    df = sortedDataByKey.groupby(sortedDataByKey.columns.get_level_values(0), axis=1).sum()
    
    #df1 = pd.MultiIndex.from_frame(df)
    #dictPandas = df.to_dict('split')
    #df1 = pd.DataFrame(dictPandas)
    #print(df1)
    #print(df.columns.tolist())
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

'''dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''

#dd = setAllDataByOneDimention("Sales")
#print(dd)

#setRowAndColumn(["City","State"],["Row ID"])

'''h = 'Order Date'
print(isDimension(h))
'''