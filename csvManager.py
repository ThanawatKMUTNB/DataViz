from itertools import chain
from re import S
import numpy as np
import pandas as pd
#import mPageByCookie
class csvManager:
    def __init__(self):
        self.selectFile = ""
        self.path = ""
        self.df = ""
    
    def setPath(self):
        self.df = pd.read_csv(self.path+"/"+self.selectFile, encoding='windows-1252')

    def getHead(self):
       return list(self.df.columns)

    def getDataWithPandas(self):
        return self.df

    def getDataWithPandasByHead(self,head):
        return self.df[head]

    def getAxisYName(self,Dimension):
        k = self.setDimensionSort(Dimension)
        head = k[Dimension].drop_duplicates()
        reg2 = head.drop_duplicates()
        reg2 = reg2[::-1].values.tolist()
        return reg2

    def getDataForBar(self,Row,Col):
        k = self.setDimensionSort(Row+Col)
        grouped = k.groupby(Row)
        sumK = grouped.sum()
        listsumk = sumK.values.tolist()
        oneList = list(chain.from_iterable(listsumk))
        return oneList[::-1]

    def getsizeDimension(self,Dimension):
        tmp = []
        for i in self.df[Dimension].values:
            if i not in tmp:
                tmp.append(i)
        return len(tmp)

    def getValueDimension(self,Dimension):
        Val = []
        for i in self.df[Dimension].values:
            if i not in Val:
                Val.append(i)
        return Val

    def setAllDataByOneDimension(self,Dimension): #sort each column
        data = self.getDataWithPandas()
        #print(type(data))
        new = data.sort_values(by=str(Dimension))
        return new

    def setDimensionSort(self,Dimension):
        sortedData = self.getDataWithPandasByHead(Dimension)
        #print(sortedData)
        print(Dimension)
        new = sortedData.sort_values(by=Dimension)
        #new.set_index([Dimension[0]])
        #new[''] = pd.Series("abc", index=new.index)
        #print("---------",new)
        pd.MultiIndex.from_frame(new)
        return new

    def getMeasure(self):
        Dimen = []
        Meas = []
        for head in self.df.columns:
            if (self.df.dtypes[head] == 'int64' or self.df.dtypes[head] == 'float64') and head != 'Row ID' and head != 'Postal Code':
                Meas.append(head)
        return Meas

    def isDimension(self,header):
        Dimen = []
        Meas = []
        for head in self.df.columns:
            if (self.df.dtypes[head] == 'int64' or self.df.dtypes[head] == 'float64') and head != 'Row ID' and head != 'Postal Code':
                Meas.append(head)
            elif self.df.dtypes[head] == 'object' or head == 'Row ID' or head == 'Postal Code':
                Dimen.append(head)
        
        if header in Dimen:
            return True
        elif header in Meas:
            return False
        else:
            return 'No header in this file'

    def unionFile(self,Listfilename):
        li = []
        #print(Listfilename)
        for i in Listfilename:
            #print(i)
            df = pd.read_csv(self.path+"/"+i, encoding='windows-1252')
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.sort_values("Row ID", inplace = True)
        frame.drop_duplicates(inplace=True)
        return frame

    def setAvgGraphX(self,Row,Col):
        k = self.setDimensionSort(Row+Col)
        k = k.T
        sumK = k.sum(axis=1)
        
    def getsizeDimension(self,Dimension):
        tmp = []
        for i in self.df[Dimension].values:
            if i not in tmp:
                tmp.append(i)
        return len(tmp)

    def setRowAndColumn(self,Row,Col):
        sortedDataByRow = self.setDimensionSort(Row)
        sortedDataByCol = self.setDimensionSort(Col)
        #print(sortedDataByCol)
        df = pd.DataFrame(sortedDataByRow).drop_duplicates()
        dfCol = pd.DataFrame(sortedDataByCol).drop_duplicates()
        #print(dfCol)
        
        oneList = list(chain.from_iterable(np.array([df.T])))
        oneListCol = list(chain.from_iterable(np.array([dfCol.T])))
        
        s = pd.DataFrame(" ",index = oneList,columns=oneListCol)
        sameDimension = list(set(Row) & set(Col))
        valueSameDimen = self.setDimensionSort(sameDimension).drop_duplicates().values.tolist()
        for i in valueSameDimen:
            s.loc[tuple(i),tuple(i)] = "abc"
        return s

