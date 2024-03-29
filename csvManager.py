# from curses import meta
import datetime
import hashlib
from importlib.metadata import files, metadata
import json
from itertools import chain, count
from ntpath import join
import os
from re import S
import re
import numpy as np
import pandas as pd
import graphManager
gm = graphManager.graphManager()
#import mPageByCookie
class csvManager:
    def __init__(self):
        self.selectFile = ""
        self.path = ""
        self.df = ""
        self.Measure = {}
        self.typeDate = {}
        self.filter = {}
        self.Head = []
        self.usemes = []
        self.func = []
        self.di = []
        self.colHeader = []
        self.Dimen = []
        self.dataFiltered = {}
        self.RowChoose = []
        self.ColChoose = []
        self.MeaFunc = {}
        self.MeaFuncChoose = {}
        self.obj = ''
    
    def setPath(self):
        print("setPath : ",self.path,self.selectFile)
        pathBuf = os.path.join(self.path,self.selectFile) 
        self.df = self.readFile(pathBuf)
        self.Measure = self.readMeasure()
        self.typeDate = self.readDate()
        self.colHeader = self.getHead()
        self.di = self.getOnlyDi()
        
    def getOnlyDi(self):
        tmp = self.getHead()
        for i in list(self.Measure.keys()):
            tmp.remove(i)
        return tmp
        
    def isMeasure(self,di):
        if (self.df.dtypes[di] == 'int64' or self.df.dtypes[di] == 'float64'):
            return True
        else :
            return False

    def readFile(self,path):
        isdir = os.path.isdir(path)
        if isdir == False:
            fileExtension = path.split(".")
            # print(fileExtension[-1])
            if fileExtension[-1] == "csv":
                df = pd.read_csv(path, encoding='windows-1252')        #for superstore.csv
                #df = pd.read_csv(path, encoding='utf-8')
            else:
                print("Excel ",path)
                #print(fileExtension[-1])
                df = pd.read_excel(path, engine = "openpyxl")
            return df
        
    def readDate(self):
        # print(self.df.columns.tolist())
        dateDic = {}
        for i in self.df.columns.tolist():
            exam = self.df.loc[[0],[i]].values[0][0]
            intForm = re.findall('\d+', str(exam))
            strForm = re.findall('\W', str(exam))
            # print(intForm,strForm)
            if len(intForm) == 3 and len(set(strForm))==1: 
                # print(intForm)
                if int(intForm[0]) < int(intForm[2]):
                    formatSet = '%d'+list(set(strForm))[0]+'%m'+list(set(strForm))[0]+'%Y'
                else:
                    formatSet = '%Y'+list(set(strForm))[0]+'%m'+list(set(strForm))[0]+'%d'
                    # print(formatSet)
                try:
                    self.df[i] =  pd.to_datetime(self.df[i],format=str(formatSet))
                    # print(i)
                    dateDic[i] = 'year'
                except ValueError:
                    pass
        # print(dateDic)
        return dateDic
    
    def getHead(self):
        if type(self.df) != str:
            self.Head = list(self.df.columns)
            return list(self.df.columns)
        else:
            return []


    def getDateByFunc(self,head,func):
        dfD = self.filterDate(self.df,head,func)
        return list(dfD.drop_duplicates())
        

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
        data = self.df
        data = data.replace('',np.nan)
        #if data == data.sort_values(by=str(Dimension)):
        '''if oldDF == sorted(data[Dimension].tolist()):
            new = data.sort_values(by=str(Dimension),ascending=False)
        else :''' 
        new = data.sort_values(by=str(Dimension))
        new = new.replace(np.nan,'')
        return new

    def setDimensionSort(self,Dimension):
        sortedData = self.getDataWithPandasByHead(Dimension)
        #print(sortedData)
        #print(Dimension)
        new = sortedData.sort_values(by=Dimension)
        #new.set_index([Dimension[0]])
        #new[''] = pd.Series("abc", index=new.index)
        #print("---------",new)
        pd.MultiIndex.from_frame(new)
        return new
    
    def readMeasure(self):
        dic = {}
        # print(list(self.df.columns)[::-1])
        # print("-------------ERROR-----------")
        # print(self.df)
        
        if type(self.df) != None:
            for head in list(self.df.columns)[::-1]:
                if (self.df.dtypes[head] == 'int64' or self.df.dtypes[head] == 'float64'):
                    dic[head] = "sum"
                else:
                    break
            return dic
                
    def getMeasure(self): # is Measure
        #Dimen = []
        Meas = []
        for head in self.df.columns:
            if (self.df.dtypes[head] == 'int64' or self.df.dtypes[head] == 'float64') and head != 'Row ID' and head != 'Postal Code':
                Meas.append(head)
        return Meas
    
    # def getDimension(self):
    #     Dimen = []
    #     for head in self.df.columns:
    #         if (self.df.dtypes[head] == 'object' or head == 'Row ID' or head == 'Postal Code'): #and head != 'Order Date' or head != 'Ship Date':
    #             Dimen.append(head)
    #     return Dimen

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
            pathBuf = os.path.join(self.path,i) 
            df = self.readFile(pathBuf)
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame = frame.replace(np.nan, '')
        #frame.sort_values("Row ID", inplace = True)

        ##############################################
        frame.drop_duplicates(inplace= True) #delete same data
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
    
    def setMesInPrivot(self,listIndexName,listIndex):
        print(listIndex,listIndexName)
        buf = {}
        for i,j in zip(listIndex,listIndexName):
            buf[i] = self.MeaFunc[j]
        return buf
            
            
    def getMesFuncOnlyMes(self,mesFrame,useKey):
        # print(self.MeaFuncChoose)
        if self.MeaFuncChoose[useKey] == 'sum':
            buf = mesFrame[useKey].sum().round(1)
        elif self.MeaFuncChoose[useKey] == 'average':
            buf = mesFrame[useKey].mean().round(1)
        elif self.MeaFuncChoose[useKey] == 'median':
            buf = mesFrame[useKey].median().round(1)
        elif self.MeaFuncChoose[useKey] == 'count':
            buf = len(mesFrame[useKey])
        elif self.MeaFuncChoose[useKey] == 'max':
            buf = mesFrame[useKey].max().round(1)
        elif self.MeaFuncChoose[useKey] == 'min':
            buf = mesFrame[useKey].min().round(1)
        self.colList[useKey] = buf
    
    def setMesFunc(self,listOfMes):
        # print("setMesFunc ",listOfMes)
        self.MeaFuncChoose[listOfMes[0]] = listOfMes[1]
        if listOfMes[1] == 'sum':
            self.MeaFunc[listOfMes[0]] = np.sum
        elif listOfMes[1] == 'average':
            self.MeaFunc[listOfMes[0]] = np.average
        elif listOfMes[1] == 'median':
            self.MeaFunc[listOfMes[0]] = np.median
        elif listOfMes[1] == 'count':
            self.MeaFunc[listOfMes[0]] = len
        elif listOfMes[1] == 'max':
            self.MeaFunc[listOfMes[0]] = max
        elif listOfMes[1] == 'min':
            self.MeaFunc[listOfMes[0]] = min
        # print("Set Meas Func : ",self.MeaFunc)
        
    def unList(self,l):
        for i in range(len(l)):
            if type(l[i]) == list and ' '.join(l[i][:-1]) in list(self.typeDate.keys()):
                l[i] = ' '.join(l[i])
                # print(l[i])
                # self.setDateInColumn(l[i])
            if type(l[i]) == list and l[i][0] in list(self.Measure.keys()):
                self.setMesFunc(l[i])
                l[i] = l[i][0]
        return l
    
    def setDataFilter(self,data,Row,Col):
        self.dfFil = data
        print("\n\nFilter",self.filter,Row,Col,'\n')
        
        for i in Row+Col:
            if i not in self.dfFil.columns.tolist() and i != None:
                buf = i.split(" ")
                first = ' '.join(buf[:-1])
                if first in list(self.typeDate.keys()):
                    if i not in list(self.filter.keys()):
                        self.dfFil = self.filterDate(self.dfFil,first,self.typeDate[first])
                        self.filter[i] = self.dfFil[i].drop_duplicates().to_list()
                    self.filter[i] = [int(i) for i in self.filter[i]]
                    self.dfFil = self.filterDate(self.dfFil,first,buf[-1])
        # print("\n\nFilter",self.filter,Row,Col,'\n')
        
        for i in list(self.filter.keys()):
            if i not in self.Measure.keys():
                if i not in Row+Col:
                    self.filter.pop(i)
                    
        # for i in Row+Col:
        #     if type(i) != list:
        #         if i not in list(self.filter.keys()):
        #             self.filter[i] = ""
                    
        for i in list(self.filter.keys()):
            if type(self.filter[i]) != list:
                if self.filter[i] == "":
                    self.filter[i] = list(set(self.df[i].values))
        
        print("\n\nFilter",self.filter,Row,Col,'\n')
        
        # self.dfFil = self.df
        # print(self.filter)
        
        for i in self.filter.keys():
            if i not in self.Measure.keys():
                print("fil dimen : ",i)
                buf = i.split(" ")
                first = ' '.join(buf[:-1])
                if first in list(self.typeDate.keys()):
                    print("Time Date : ",self.filter[i])
                    self.filter[i] = [int(s) for s in self.filter[i]]
                    # print("Time Date : ",self.filter[i])
                    # for p in self.filter[i]:
                    # print(self.dfFil)
                    self.dfFil = self.dfFil[self.dfFil[i].isin(self.filter[i])]
                    # print(self.dfFil)
                    # self.dfFil = self.dfFil[self.dfFil[i].isin(self.filter[i])]
                    # print(self.dfFil)
                else:
                    self.dfFil = self.dfFil[self.dfFil[i].isin(self.filter[i])]
        # print(self.dfFil)
        # self.dfFil = self.filterMes(self.dfFil)
        return self.dfFil
    
    def filterMes(self,data):
        print("Filter Measure " ,self.filter)
        # print(max(data.values.tolist()[0]))
        
        for i in list(self.filter.keys()):
            if i in list(self.Measure.keys()):
                # print("i : ",i)
                # print(data.index.tolist())
                # print(data.columns.tolist())
                # print(type(data))
                if type(data.index) == pd.MultiIndex:
                    for j in list(data.index):
                        if i in j:
                            if float(data.loc[j]) < min(self.filter[i]) or float(data.loc[j]) > max(self.filter[i]):
                                data = data.drop(index =j)
                elif type(data.columns) == pd.MultiIndex:
                    for j in list(data.columns):
                        if i in j:
                            if float(data[j]) < min(self.filter[i]) or float(data[j]) > max(self.filter[i]):
                                data = data.drop(columns =j)
                else:
                    if i in data.index.tolist():
                        # print("Index")
                        s = data.loc[i].between(min(self.filter[i]), max(self.filter[i]), inclusive = True)
                        # print(s)
                        data = data.loc[s]
                    if i in data.columns.tolist():
                        # print("Columns")
                        # print(data[i])
                        s = data[i].between(min(self.filter[i]), max(self.filter[i]), inclusive = True)
                        data = data[s]
                    # print("\n",data.iloc[i])
        return data
            
    def filterDate(self,data,Dimension,typ): #Date only
        # print("filterDate --- ", Dimension,typ)
        tmpData = data
        s = str(Dimension+' '+typ)
        # print("----------------------------------------IN")
        tmpData[Dimension] = pd.to_datetime(tmpData[Dimension],format='%d/%m/%Y')
        tmpData[Dimension+' year'] = tmpData[Dimension].dt.year
        tmpData[Dimension+' month'] = tmpData[Dimension].dt.month
        tmpData[Dimension+' date'] = tmpData[Dimension].dt.day
        return tmpData
    
    def setRowCol(self,Row,Col):
        self.RowChoose = Row
        self.ColChoose = Col
    
    def getRow(self):
        return self.RowChoose
    
    def getCol(self):
        return self.ColChoose
    
    def setRowAndColumn(self,Row,Col):
        self.setRowCol(Row,Col)
        Row = self.getRow()
        Col = self.getCol()
        print("\n\nCMS")
        # print(self.filter)
        print(Row,Col)
        # print(self.df)
        
        Col = self.unList(Col)
        Row = self.unList(Row)
        
        ############## Filter di ############
        usedata = self.df
        # print("Before Filter\n",usedata)
        if self.filter != {}:
            usedata = self.setDataFilter(usedata,Row,Col)
            # self.dataFiltered = usedata
        # print(self.filter)
        
        ###################################
        oriRow = Row.copy()
        oriCol = Col.copy()
        # print("After Filter",usedata)
        
        ############## Filter date ############
        # print("-------",Row,Col)
        for i in range(len(Row)):
            if type(Row[i]) == list:
                s = ' '.join(Row[i])
                if Row[i][0] in list(self.typeDate.keys()):
                    if s not in usedata.columns.tolist():
                        usedata = self.filterDate(usedata,Row[i][0],Row[i][1])
                    Row[i] = s
                else:
                    Row[i] = Row[i][0]
            if Row[i] not in usedata.columns.tolist():
                buf = Row[i].split(" ")
                first = ' '.join(buf[:-1])
                if first in list(self.typeDate.keys()):
                    # print(self.filter)
                    if Row[i] in list(self.filter.keys()):
                        self.filter[Row[i]] = [int(i) for i in self.filter[Row[i]]]
                    usedata = self.filterDate(usedata,first,buf[-1])
        
        for i in range(len(Col)):
            if type(Col[i]) == list:
                # print("Col")
                s = ' '.join(Col[i])
                if Col[i][0] in list(self.typeDate.keys()):
                    if s not in usedata.columns.tolist():
                        usedata = self.filterDate(usedata,Col[i][0],Col[i][1])
                    Col[i] = s
                else:
                    Col[i] = Col[i][0]
            # print(Col[i])  
            if Col[i] not in usedata.columns.tolist():
                buf = Col[i].split(" ")
                first = ' '.join(buf[:-1])
                if first in list(self.typeDate.keys()):
                    if Col[i] in list(self.filter.keys()):
                        self.filter[Col[i]] = [int(i) for i in self.filter[Col[i]]]
                    usedata = self.filterDate(usedata,first,buf[-1])
        self.dataFiltered = usedata

            # print(Col[i])
        # print("\n",oriRow,oriCol)
        # print("-------",Row,Col)
        # print(usedata.columns.tolist())
        #####################################
        # print("\n\n",usedata)
        isInterRow = list(set(Row).intersection(set(self.Measure.keys())))
        isInterCol = list(set(Col).intersection(set(self.Measure.keys())))
        # if len(isInterRow+isInterCol) != []:
        #     usedata = self.setDataFilterMes(usedata,isInterRow+isInterCol)
        # print("****",isInterRow,isInterCol)
        print("-------",Row,Col)
        if isInterRow == [] and isInterCol == []: #No Mes
            Rowdi = Row.copy()
            Coldi = Col.copy()
            if Row != [] and Col == []:
                rowList = usedata[Row]
                packDf = [rowList]
            if Row == [] and Col != []:
                colList = usedata[Col]
                packDf = [colList]
            if Row != [] and Col != []:
                rowList = usedata[Row]
                colList = usedata[Col]
                packDf = [rowList,colList]
            results = pd.concat(packDf, axis=1,ignore_index=True)
            results[" "] = "abc"
            results = results.sort_values(by=results.columns.tolist())
            results = results.drop_duplicates()
            k = results.pivot(results.columns[len(Row):-1].tolist(),results.columns[:len(Row)].tolist())
            k = k.replace(np.nan, '')
            if type(k) == pd.Series :
                k = k.to_frame()
            if Row != [] and Col != []:
                k = k.T
            if Row == [] and Col != []:
                k = k.T
                
            if type(k.columns) == pd.MultiIndex:
                k.columns.names = Coldi

            if len(Coldi) == 1:
                k.columns.name = Col[0]
        else: # Have Mes 
            # print("c",Row,Col)
            # print("isin",isInterRow,isInterCol)
            intersecAt = ''
            Rowdi = Row.copy()
            Coldi = Col.copy()
            intersec = ''
            if isInterRow != []:
                # for i in Row:
                #     print("---*----",i)
                #     if i in self.Head:
                #         Rowdi.append(i)
                # print("c2",Row,Col)
                for i in isInterRow:
                    if i in Rowdi:
                        while Rowdi.count(i) >0:
                            Rowdi.remove(i)
                intersecAt = 'Row'
                intersec = isInterRow
                
            if isInterCol != []:
                # for i in Col:
                #     print("---*----",i)
                #     if i in self.Head:
                #         Coldi.append(i)
                for i in isInterCol:
                    if i in Coldi:
                        while Coldi.count(i) >0:
                            Coldi.remove(i)
                intersecAt = 'Col'
                intersec = isInterCol
            
            packDf = []
            # print("caf",Rowdi,Coldi)
            # print("isin ",isInterRow,isInterCol)
            if Rowdi == [] and Coldi == []: #Only mes
                print("Only mes")
                # print(Row+Col)
                # intersec = Row+Col
                # print(self.MeaFunc)
                self.colList = {}
                for i in intersec:
                    self.getMesFuncOnlyMes(usedata[intersec],i)
                self.colList = pd.Series(self.colList)
                self.colList = self.colList.to_frame()
                
                k = self.colList
                k = k[list(k.columns)].astype(str)
                if type(k) == pd.Series :
                    k = k.to_frame()
                
                # print(k.index.tolist())
                # print(k)
                changname = k.index.tolist()
                for i in range(len(changname)):
                    changname[i] = changname[i] +" "+ self.MeaFuncChoose[changname[i]]
                k.index = changname
                # print(k)
                if intersecAt == 'Col':
                    k = self.colList.T
                    k.columns = changname
                # print(k)
            else: # di mes
                # print(Row,Col)
                if Rowdi != [] and Coldi == []:
                    rowList = usedata[Rowdi]
                    colList = usedata[Coldi+intersec]
                    packDf = [rowList,colList]
                if Rowdi == [] and Coldi != []:
                    colList = usedata[Coldi+intersec]
                    packDf = [colList]
                if Rowdi != [] and Coldi != []:
                    rowList = usedata[Rowdi]
                    # print(Coldi,intersec)
                    # print(Coldi+intersec)
                    colList = usedata[Coldi+intersec]
                    packDf = [rowList,colList]
                    
                results = pd.concat(packDf, axis=1,ignore_index=True)
                results = results.sort_values(by=results.columns.tolist())
                colNum = results.columns.tolist()
                # print(colNum)
                beforMesual = (-1)*len(intersec)
                
                if isInterRow != [] and isInterCol == []: #mes in row
                    # print(Rowdi,Coldi)
                    print("\nmeas in row")
                    # print("isInterRow : ",isInterRow)
                    # print("beforMesual : ",colNum[beforMesual:])
                    # print(Rowdi,Coldi)
                    # print(colNum)
                    # print(self.MeaFunc)
                    Func = self.setMesInPrivot(isInterRow,colNum[beforMesual:])
                    # print("Func : ",Func)
                    k = pd.pivot_table(results,index = colNum[len(Rowdi):beforMesual], columns = colNum[:len(Rowdi)],values = colNum[beforMesual:],aggfunc=Func)
                    # k = pd.pivot_table(results,index = colNum[len(Rowdi):beforMesual], columns = colNum[:len(Rowdi)],values = colNum[beforMesual:])                    
                    k = k.round(1)
                    # print(k)
                    # print(k.index)
                    # k.index = isInterRow
                    # print("---- ",oriRow,oriCol)
                    if oriCol != [] and oriRow == []:
                        k=k.T
                        # print(dict(k.columns))
                        # print("----",isInterRow)
                        # print(k)
                        if len(isInterRow) > 1:
                            # print("M")
                            # isInterRow = isInterRow*len(k.index)
                            # k.index = isInterRow
                            if len(isInterCol) == 1:
                                # print("C")
                                # print("Cbbbbbbbbbbbbbbbbb")
                                
                                isInterCol = isInterCol*len(k.columns)
                                k.columns = isInterCol
                                # print(isInterCol)
                            else:
                                # print("Cbbbbbbbbbbbbbbbbb")
                                # print(oriRow,oriCol)
                                # print(k)
                                # print(Coldi,k.columns,isInterCol)
                                # print(Rowdi,k.index,isInterRow)
                                if isInterCol != []:
                                    # print("0000000000000")
                                    k.columns = isInterCol
                                if isInterRow != [] and Rowdi == []:
                                    # print("1111111111")
                                    # print(len(k.index))
                                    k.index = isInterRow
                                else:
                                    # print(dict(k.index))
                                    changname = dict(k.index)
                                    for i,j in zip(list(changname.keys()),isInterRow):
                                        changname[i] = j 
                                    k = k.rename(index = changname)
                            
                                    # k.index = Rowdi
                        else:
                            # print("Cbbbbbbbbbbbbbbbbb")
                            
                            if Coldi != []:
                                # print("c")
                                if Rowdi != []:
                                    if type(k.index) == pd.MultiIndex:
                                        print("Not fix yet")
                                        print(k.index.names)
                                        print(k.columns.names)
                                        # print(k)
                                    else:
                                        d = dict(k.index)
                                        d[list(d.keys())[0]] = isInterRow[0]
                                        k = k.rename(index=d)
                                else:
                                    k.index = isInterRow
                            if Rowdi != []:
                                # print("c")
                                # k.columns = Rowdi
                                if type(k.index) == pd.MultiIndex:
                                    dicName = k.index.tolist()
                                    resultsDict = {}
                                    for i in dicName:  
                                        resultsDict.setdefault(i[0],[]).append(i[1:])
                                    # print(resultsDict)
                                    # k = k.rename(index=d)
                                    # print(k)
                                else:
                                    d = dict(k.index)
                                    d[list(d.keys())[0]] = isInterRow[0]
                                    k = k.rename(index=d)
                                    # print(k)
                    else:
                        # print("in")
                        if len(k.index) == len(isInterRow):
                            k.index = isInterRow
                            k=k.unstack()
                        else:
                            # print("in")
                            # print(isInterRow)
                            # print(self.Measure)
                            # tmp = []
                            # for i in isInterRow:
                            #     tmp.append(i+" "+self.Measure[i])
                            k.columns = isInterRow
                            if Coldi != [] and Rowdi == [] and len(isInterRow) == 1:
                                k.index.names = Coldi
                                k=k.T
                            else:
                                k=k.unstack()
                else: #mes in col
                    print("meas in col")
                    # print(self.MeaFunc)
                    Func = self.setMesInPrivot(isInterCol,colNum[beforMesual:])
                    # print(Func)
                    k = pd.pivot_table(results,columns = colNum[len(Rowdi):beforMesual], index= colNum[:len(Rowdi)],values = colNum[beforMesual:],aggfunc=Func)
                    k = k.round(1)
                    # print(k)
                    if oriRow != []:
                        # print("c")
                        if len(isInterCol) == 1:
                            # print("c")
                            # print(k)
                            # print(type(k.columns))
                            if type(k.columns) == pd.MultiIndex:
                                # print("c")
                                olddi = [list(ele) for ele in k.columns]
                                # isInterCol = k.columns.tolist()
                                # print(isInterCol)
                                # isInterCol = isInterCol*len(k.columns)
                                for i in range(len(k.columns)):
                                    buf = str(isInterCol[0])+" "+str(olddi[i][1])
                                    olddi[i] = buf
                                # print(olddi)
                                # k.columns = olddi
                            else: 
                                # print(Rowdi,Coldi)
                                k.columns=isInterCol
                                if Coldi == [] and Rowdi != []:
                                    k.index.names = Rowdi
                                if Coldi != [] and Rowdi == []:
                                    k.index.names = Coldi
                        else:
                            # print(k.columns)
                            # print(oriRow,oriCol)
                            # print(k)
                            # print(Coldi,k.columns,isInterCol)
                            # print(Rowdi,k.index,isInterRow)
                            if isInterCol != [] and Coldi == []:
                                k.columns = isInterCol
                            if isInterCol != [] and Coldi != []:
                                # print(dict(k.index))
                                changname = dict(k.columns)
                                for i,j in zip(list(changname.keys()),isInterCol):
                                    changname[i] = j 
                                k = k.rename(columns = changname)
                        # print(k)
                    else :
                        # print("c")
                        # print("cc",beforMesual)
                        # if type(results) == pd.Series :
                        #     results = results.to_frame()
                        # results = results.groupby(0).sum().round(1).stack()
                        # print(self.MeaFunc)
                        Func = self.setMesInPrivot(isInterCol,colNum[beforMesual:])
                        
                        k = pd.pivot_table(results,columns = colNum[:beforMesual],values = colNum[beforMesual:],aggfunc=Func)
                        k = k.round(1)
                        
                        k.index = isInterCol
                        # print("-------")
                        k = k.unstack()
                        if type(k) == pd.Series :
                            k = k.to_frame()
                        k = k.T
                k = k.replace(np.nan, '')
        # print(type(k))
        #print(k.index.tolist())
        if type(k) == pd.Series :
            k = k.to_frame()
        # print(k)
        # print(self.MeaFunc)
        # print(self.filter)
        
        if isInterCol!=[] or isInterRow!=[]:
            # print(isInterCol, isInterRow)
            k = self.filterMes(k)
        # self.dataFiltered = k
        print(k)
        return k

    def setRowForSpan(self,data,Rowdi):
        k = data
        if type(k) == pd.Series :
            k = k.to_frame()
        # print(k.index.tolist())
        print(k)
        if type(k.index) == pd.MultiIndex:
            j = k.index.tolist()
            for i in range(len(j)):
                j[i] = ' '.join(j[i])
                # for s in list(j[i]):
                #     print(s)
                #     if s not in self.Measure.keys():
                #         j[i]=s
        else : j = k.index.tolist()
        if Rowdi != '':
            if len(Rowdi) == 1 :
                # print("-------",(k.index))
                k.insert(0, Rowdi[0], j)
            else:
                print(j)
                listOfValues = list(zip(*j))
                l = Rowdi
                print(l,listOfValues)
                # print(len(listOfValues))
                m = 0
                for i,p in zip(l,listOfValues):
                    # print(i,p)
                    # print(list(listOfValues[n]))
                    if type(p) == tuple:
                        # print("Y")
                        p = list(p)
                        for s in p:
                            if s not in self.Measure.keys():
                                p=s
                    k.insert(m, i, p, True)
                    m+=1
    def getSpan(data,MesKey):
        k = data
        if type(k) == pd.Series :
            k = k.to_frame()
        
        # print(k)
        indexSpan = []
        colindex = 0
        for i in k.columns.tolist():
            # print(list(self.Measure.keys()))
            if i not in MesKey:
                print(i)
                tmp = []
                span = []
                tmp.append(colindex)
                span.append(0)
                for p in range(len(k[i])-1):
                    if k[i][p] != k[i][p+1]:
                        # print(k[i][p], k[i][p+1])
                        span.append(p)
                        tmp.append(span)
                        if span[0] != span[1]:
                            # print(k[i][span[0]],k[i][span[0]])
                            indexSpan.append(tmp)
                        span = []
                        span.append(p+1)
                        tmp = []
                        tmp.append(colindex)
                    if p == len(k[i])-2:
                        span.append(p+1)
                        tmp.append(span)
                        if span[0] != span[1]:
                            indexSpan.append(tmp)
                colindex += 1
        return indexSpan
        
    def saveMetadata(self) :
        metadata = {}
        metadata["Path"] = self.path 
        HashFile = (hashlib.md5(self.selectFile.encode('UTF-8')).hexdigest())
        metadata["FileName"] = HashFile
        metadata["Dimension"] = self.getDimension()
        metadata["Measurement"] = self.getMeasure()
        #metadata["Date"] = self.getDate()
        #print(date)
        print(metadata)
        with open("metadata.json", 'w') as exportFile:
            saveFile = json.dumps(metadata , indent= 4)
            exportFile.write(saveFile)

    def loadMetadata(self) :
        with open('metadata.json') as metadata_json:
            metadata = json.load(metadata_json)
        self.path = metadata['Path']
        HashFile = metadata['Filename']
        #self.selectFile = hashlib.md5(self.selectFile.encode('UTF-8')).hexdigest()
        self.Dimen = metadata['Dimension']
        self.Measure = metadata['Measurement']
        '''Path = []
        FileName = []
        Dimension = []
        Measurment = []
        HashFile = (hashlib.md5(self.selectFile.encode('UTF-8')).hexdigest()) 
        if self.path == metadata["Path"] :        
            if "Path" in metadata :
                Path = (metadata["Path"])   
            if "FileName" in metadata :
                FileName = (metadata["FileName"])
                if metadata["FileName"] == HashFile :
                    if "Dimen" in metadata :
                        Dimension = (metadata["Dimen"])
                    if "Meas" in metadata :
                        Measurment = (metadata["Meas"])
                    return Path,FileName,Dimension, Measurment
                else :
                    print("Don't have file")
        else :
            print("Don't have file")'''
            
            #print(Path,Dimension,Measurment)
    def setObj(self,n):
        self.obj = str(n)
        self.SwapDiMeas()
        
    def SwapDiMeas(self):
        # print("SwapDiMeas",self.df.columns.tolist())
        # print("Mes",list(self.Measure.keys()))
        rdf = len(self.df.columns)
        if self.obj not in list(self.Measure.keys()):
            movecolumn = self.df.pop(self.obj)
            self.df.insert(rdf-1,self.obj,movecolumn)
            self.Measure[self.obj] = 'sum'
        else:
            movecolumn = self.df.pop(self.obj)
            self.df.insert(0,self.obj,movecolumn)
            # print("BF ",self.Measure)
            del self.Measure[self.obj]
            # print("AF ",self.Measure)
        self.di = self.getOnlyDi() 
        
        # return self.df

    # def print(self):
    #     print('\n--------------------------------------\n')
    #     print('path = ',self.path)
    #     print('hashfile =',(hashlib.md5(self.selectFile.encode('UTF-8')).hexdigest()))
    #     print('Dimen = ',self.getDimension())
    #     print('Meas = ',self.Measure)