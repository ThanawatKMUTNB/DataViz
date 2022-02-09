from itertools import chain
from re import S
import numpy as np
import pandas as pd
import main as m
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
    Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
    def setRowAndColumn(self,Row,Col):
        isInterRow = list(set.intersection(set(Row),set(self.Measure)))
        isInterCol = list(set.intersection(set(Col),set(self.Measure)))
        #print(isInterRow,isInterCol)
        if isInterRow == [] and isInterCol == []:
            rowList = self.getDataWithPandasByHead(Row)
            colList = self.getDataWithPandasByHead(Col)
            results = pd.concat([rowList, colList], axis=1,ignore_index=True)
            results[" "] = "abc"
            results = results.sort_values(by=results.columns.tolist())
            results = results.drop_duplicates()
            k = results.pivot(results.columns[len(Row):-1].tolist(),results.columns[:len(Row)].tolist())
            k = k.replace(np.nan, '')
            k = k.T
            #print(k.columns.names)
        else:
            intersecAt = ''
            filterChoose = "sum"
            if isInterRow != []:
                for i in isInterRow:
                    Row.remove(i)
                intersecAt = 'Row'
                intersec = isInterRow
            else:
                for i in isInterCol:
                    Col.remove(i)
                intersecAt = 'Col'
                intersec = isInterCol
            packDf = []
            if Row == [] and Col == []:
                #print(Row,Col)
                colList = self.getDataWithPandasByHead(intersec)
                colList = colList.sum().round(0)
                #print(colList.sum().round(0))
                if intersecAt == 'Row':
                    colList = colList.to_frame()
                    return colList
                else:
                    colList = colList.to_frame()
                    return colList.T
            else:
                #print(Row,Col)
                if Row != [] and Col == []:
                    rowList = self.getDataWithPandasByHead(Row)
                    colList = self.getDataWithPandasByHead(Col+intersec)
                    packDf = [rowList,colList]
                if Row == [] and Col != []:
                    colList = self.getDataWithPandasByHead(Col+intersec)
                    packDf = [colList]
                if Row != [] and Col != []:
                    rowList = self.getDataWithPandasByHead(Row)
                    colList = self.getDataWithPandasByHead(Col+intersec)
                    packDf = [rowList,colList]
                #print(packDf)
            #print(intersecAt,intersec)

            #DiList = self.getDataWithPandasByHead(intersec)
            results = pd.concat(packDf, axis=1,ignore_index=True)
            results = results.sort_values(by=results.columns.tolist())
            #print(intersec)
            #print(results)
            colNum = results.columns.tolist()
            beforMesual = (-1)*len(intersec)
            '''DiList = results.groupby(colNum[:beforMesual])[colNum[beforMesual:]].sum()
            print(DiList)'''
            #print("-----------",colNum[beforMesual:])
            if isInterRow != []:
                k = pd.pivot_table(results,index = colNum[len(Row):beforMesual], columns = colNum[:len(Row)],values = colNum[beforMesual:],aggfunc=np.sum)
                k = k.round(0)
                k=k.T
                #k.columns.names = Col
                #k.index.names = [None]+Row
            else:
                k = pd.pivot_table(results,columns = colNum[len(Row):beforMesual], index= colNum[:len(Row)],values = colNum[beforMesual:],aggfunc=np.sum)
                k = k.round(0)
                #k.columns.names = [None]+Col
                #k.index.names = Row
            k = k.replace(np.nan, '')
        print(k)
        '''tmp = [list(ele) for ele in k.index]
        eachList = []
        for j in range(len(tmp[0])):
            eachList.append([i[j] for i in tmp[:]])
        for i in range(len(eachList)):
            for j in range(len(eachList[i])-1,0,-1):
                if eachList[i][j] == eachList[i][j-1] :
                    eachList[i][j]=''
        changIndex = pd.MultiIndex.from_arrays(eachList, names=k.index.names)
        k.index = changIndex
        print(k)'''
        return k

'''ex = csvManager()
ex.df = pd.read_csv("Superstore.csv", encoding='windows-1252')
#ex.df = pd.read_csv("SS_20lines.csv", encoding='windows-1252')
#ex.setDimensionSort(["Region","Segment","Region","Region"])
ex.setRowAndColumn(["Segment","Sales"],["Segment","Region"])
#ex.setRowAndColumn(["Region","Region","Segment"],["Region","Sales","Profit"])'''