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
        self.df = self.readFile(self.path+"/"+self.selectFile)
        
    def readFile(self,path):
        fileExtension = path.split(".")
        if fileExtension[-1] == "csv":
            df = pd.read_csv(path, encoding='windows-1252')
        else:
            #print(fileExtension[-1])
            df = pd.read_excel(path, engine = "openpyxl")
        return df
    
    def getHead(self):
       return list(self.df.columns)

    def getDataWithPandas(self):
        return self.df

    def getDataWithPandasByHead(self,head):
        #print(head)
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
        if len(Dimension) == len(set(Dimension)):
            sortedData = self.getDataWithPandasByHead(Dimension)
            #print(sortedData)
            new = sortedData.sort_values(by=Dimension)
        else:
            sortedData = None
            dflist = []
            dflistdup = []
            for i in Dimension:
                if i not in dflist:
                    dflist.append(i)
                    sortedData = self.getDataWithPandasByHead(dflist)
                    sortedData = sortedData.sort_values(by=dflist)
                    #print("---",sortedData.loc[:,sortedData.columns[-1]])
                else:
                    #print(pd.DataFrame({i:sortedData[i]}))
                    dflistdup.append([len(dflist),pd.DataFrame({i:sortedData[i]})])
            for i in dflistdup:
                tmp = i[1]
                sortedData.insert(i[0], tmp.columns[-1] ,tmp.loc[:,tmp.columns[-1]],allow_duplicates=True)
            new = sortedData
        #print(new)
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
            df = self.readFile(self.path+"/"+i)
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.sort_values("Row ID", inplace = True)
        frame.drop_duplicates(inplace=True)
        self.df = frame
        return self.df
        
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
        #self.df = pd.read_csv("Superstore.csv", encoding='windows-1252')
        #self.df = pd.read_csv("SS_20lines.csv", encoding='windows-1252')
        '''baseList = self.setDimensionSort(list(set(Row+Col))).drop_duplicates()
        baseList[" "] = "abc"'''
        #print(Row,Col)
        rowList = self.getDataWithPandasByHead(Row)
        colList = self.getDataWithPandasByHead(Col)
        #colList.sort_values()
        '''for i in allChoose:
            allChoose.count(i)'''
        results = pd.concat([rowList, colList], axis=1,ignore_index=True)
        results[" "] = "abc"
        results = results.sort_values(by=results.columns.tolist())
        #print(len(results))
        #print(sorted(set(results["City"])))
        results = results.drop_duplicates()
        cl = results[results.iloc[:][:]=="Ann Arbor"].index.tolist()
        #print(cl)
        '''for i in cl:
            print(results[3][i])'''
        '''l = str(list(results.columns[len(Row):-1]))
        p = l.strip('][').split(', ')'''
        #print(p)
        #print(len(Row))
        
        k = results.pivot(results.columns[len(Row):-1].tolist(),results.columns[:len(Row)].tolist())
        k = k.replace(np.nan, '')
        #print(len(k.columns))
        print(k.T)
        return k.T

'''ex = csvManager()
ex.df = pd.read_csv("Superstore.csv", encoding='windows-1252')
#ex.setDimensionSort(["Region","Segment","Region","Region"])
ex.setRowAndColumn(["Region","Segment","Region","Region"],["Ship Mode"])'''