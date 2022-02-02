from itertools import chain
from re import S
import numpy as np
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
    #df = pd.read_csv('SS_20lines.csv', encoding='windows-1252')
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    #data = pd.DataFrame(df,columns=[df.columns.tolist()],index=df["Row ID"])
    df = df[head]
    return df

def setDimentionSort(dimention):
    sortedData = getDataWithPandasByHead(dimention)
    #print(sortedData)
    #print(oneList)
    new = sortedData.sort_values(by=dimention)
    new.set_index([dimention[0]])
    #print(new)
    #new[''] = pd.Series("abc", index=new.index)
    pd.MultiIndex.from_frame(new)
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

def unionFile(oldfilename,newfilename):
    li = []
    df1 = pd.read_csv(oldfilename, encoding='windows-1252')
    df2 = pd.read_csv(newfilename, encoding='windows-1252')
    li.append(df1)
    li.append(df2)
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.sort_values("Row ID", inplace = True)
    frame.drop_duplicates(inplace=True)
    return frame

def setAvgGraphX(Row,Col):
    k = setDimentionSort(Row+Col)
    k = k.T
    sumK = k.sum(axis=1)

def getsizeDimention(dimention):
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    tmp = []
    for i in df[dimention].values:
        if i not in tmp:
            tmp.append(i)
    return len(tmp)

def getValueDimention(dimention):
    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    Val = []
    for i in df[dimention].values:
        if i not in Val:
            Val.append(i)
    return Val
    
dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
'''sortedData = setDimentionSort(dimention,"Postal Code")
print(sortedData)'''

#dd = setAllDataByOneDimention("Sales")
#print(dd)

#dd = setRowAndColumn(["City","State"],["Row ID","Product ID"])
#print(dd)

def setRowAndColumn(Row,Col):
    sortedDataByRow = setDimentionSort(Row)
    sortedDataByCol = setDimentionSort(Col)
    #print(sortedDataByCol)
    df = pd.DataFrame(sortedDataByRow).drop_duplicates()
    dfCol = pd.DataFrame(sortedDataByCol).drop_duplicates()
    #print(dfCol)
    
    oneList = list(chain.from_iterable(np.array([df.T])))
    oneListCol = list(chain.from_iterable(np.array([dfCol.T])))
    
    #print(dataF)
    #s2 = pd.merge(df, dfCol, how="inner", on=list(set(Row) & set(Col)))
    #s = pd.Series('ss', index=oneList)
    s = pd.DataFrame(" ",index = oneList,columns=oneListCol)
    #print(s)
    sameDimention = list(set(Row) & set(Col))
    for j in sameDimention:
        valueSameDimen = getDataWithPandasByHead(j).drop_duplicates()
        for i in valueSameDimen:
            s.at[[i],[i]] = "abc"


    #s = s.iloc[Row, Col] = "abc"
    #s2 = pd.concat([df, dfCol], axis=1, ignore_index=True)
    
    '''listRow = [list(row) for row in s.index]
    subRow = np.array(listRow).T.tolist()
    for i,j in zip(reversed(subRow),Row):
        s.insert(0,j,i)'''
    #s2 = df.join(dfCol,on=list(set(Row) & set(Col)))
    #s2 = pd.concat(df,dfCol, on = list(set(Row) & set(Col)), how = 'outer')
    #merged[merged['population'].isnull()]
    #s2 = s2.drop('abbreviation', 1) # drop duplicate info
    #s2 = s2.head()
    
    '''listCol = [list(col) for col in s.head()]
    subCol = np.array(listCol).T.tolist()
    for i in reversed(subCol):
        print(i)
        s.loc[-1] = i  # adding a row
        print(s)
        #s.index = s.index + 1# shifting index
        #s.sort_index(inplace=True)'''
    return s


#dd = pd.MultiIndex.from_frame(dd)
#index = pd.MultiIndex.from_tuples(dd)
