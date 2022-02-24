# from curses import meta
import datetime
import hashlib
from importlib.metadata import files, metadata
import json
from itertools import chain
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
    
    def setPath(self):
        # print(self.path,self.selectFile)
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
                df = pd.read_csv(path, encoding='windows-1252')
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
        print(dateDic)
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
    
    def getDimension(self):
        Dimen = []
        for head in self.df.columns:
            if (self.df.dtypes[head] == 'object' or head == 'Row ID' or head == 'Postal Code'): #and head != 'Order Date' or head != 'Ship Date':
                Dimen.append(head)
        return Dimen

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
    # Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
    
    def setDataFilter(self,Row,Col):
        # print("filter",self.filter,Row+Col)
        for i in list(self.filter.keys()):
            if i not in self.Measure.keys():
                if i not in Row+Col:
                    self.filter.pop(i)
        for i in Row+Col:
            if type(i) != list:
                if i not in list(self.filter.keys()):
                    self.filter[i] = ""
        for i in list(self.filter.keys()):
            if type(self.filter[i]) != list:
                if self.filter[i] == "":
                    self.filter[i] = list(set(self.df[i].values))
        self.dfFil = self.df
        # print(self.filter)
        for i in self.filter.keys():
            if i not in self.Measure.keys():
                print("fil dimen")
                self.dfFil = self.dfFil[self.dfFil[i].isin(self.filter[i])]
            
    def filterMes(self,data):
        print(self.filter)
        for i in self.filter.keys():
            if i in self.Measure.keys():
                print("fil mes")
                data = data.loc[data[i].between(min(self.filter[i]), max(self.filter[i]))]
        return data
            # else:
            #     # print(i)
            #     # print(self.filter[i][0])
            #     self.dfFil = self.dfFil.loc[self.dfFil[i] > self.filter[i][0]]
            #     self.dfFil = self.dfFil.loc[self.dfFil[i] < self.filter[i][1]] 
            #     # print(self.dfFil)
            
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
    
    def setRowAndColumn(self,Row,Col):
        # print(self.filter)
        # print("CMS")
        # print(Row,Col)
        
        ############## Filter di ############
        usedata = self.df
        if self.filter != {}:
            self.setDataFilter(Row,Col)
            usedata = self.dfFil
            self.dataFiltered = usedata
        ###################################
        oriRow = Row
        oriCal = Col
        # print(usedata.columns.tolist())
        
        ############## Filter date ############
        for i in range(len(Row)):
            if type(Row[i]) == list:
                if Row[i][0] in list(self.typeDate.keys()):
                    if Row[i][0]+" "+Row[i][1] not in usedata.columns.tolist():
                        usedata = self.filterDate(usedata,Row[i][0],Row[i][1])
                    s = Row[i][0]+" "+Row[i][1]
                    Row[i] = s
                    oriRow[i] = s
                else:
                    Row[i] = Row[i][0]
                    
        for i in range(len(Col)):
            # print(i)
            if type(Col[i]) == list:
                if Col[i][0] in list(self.typeDate.keys()):
                    if Col[i][0]+" "+Col[i][1] not in usedata.columns.tolist():
                        usedata = self.filterDate(usedata,Col[i][0],Col[i][1])
                    s = Col[i][0]+" "+Col[i][1]
                    Col[i] = s
                    oriCal[i] = s
                else:
                    Col[i] = Col[i][0]
        # print("\n",oriRow,oriCal)
        # print(Row,Col)
        # print(usedata.columns.tolist())
        #####################################
        
        isInterRow = list(set(Row).intersection(set(self.Measure.keys())))
        isInterCol = list(set(Col).intersection(set(self.Measure.keys())))
        # if len(isInterRow+isInterCol) != []:
        #     usedata = self.setDataFilterMes(usedata,isInterRow+isInterCol)
        # print("****",isInterRow,isInterCol)
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
        else: # Have Mes 
            # print("c",Row,Col)
            # print("isin",isInterRow,isInterCol)
            intersecAt = ''
            filterChoose = "sum"
            # Rowdi = Row.copy()
            # Coldi = Col.copy()
            # print(self.Head)
            Rowdi = Row.copy()
            Coldi = Col.copy()
            # print("caf",Rowdi,Coldi)
            intersec = ''
            if isInterRow != []:
                # for i in Row:
                #     print("---*----",i)
                #     if i in self.Head:
                #         Rowdi.append(i)
                # print("c2",Row,Col)
                for i in isInterRow:
                    if i in Rowdi:
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
                        Coldi.remove(i)
                intersecAt = 'Col'
                intersec = isInterCol
            packDf = []
            # print("caf",Rowdi,Coldi)
            # print("isin ",isInterRow,isInterCol)
            if Rowdi == [] and Coldi == []: #Only mes
                #print(Rowdi,Coldi)
                colList = usedata[intersec]
                if filterChoose == "sum":
                    colList = colList.sum().round(0)
                #print(colList.sum().round(0))
                
                if intersecAt == 'Row':
                    colList = colList.to_frame()
                    k = colList
                    # k = k.rename({0:"sum"})
                    k = k[list(k.columns)].astype(str)
                    # if filterChoose == "sum":
                    #     k.rename(in)
                    if type(k) == pd.Series :
                        k = k.to_frame()
                    changname = zip(list(k.columns), [filterChoose*len(list(k.columns))])
                    # print(dict(k.columns))
                else:
                    colList = colList.to_frame()
                    k = colList
                    k = k[list(k.columns)].astype(str)
                    if type(k) == pd.Series :
                        k = k.to_frame()
                    k = colList.T
                    # print(k.index)
                    changname = zip(list(k.index), [filterChoose*len(list(k.index))])
                
                changname = (dict(changname))
                
                k = k.rename(columns=changname,index=changname)
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
                    # print(Row,Col)
                    print("meas in row")
                    k = pd.pivot_table(results,index = colNum[len(Rowdi):beforMesual], columns = colNum[:len(Rowdi)],values = colNum[beforMesual:],aggfunc=np.sum)
                    k = k.round(0)
                    # print(k.unstack())
                    if oriCal != []:
                        k=k.T
                        # print(dict(k.columns))
                        # print("----",isInterRow)
                        # print(k)
                        if len(isInterRow) > 1:
                            # print("M")
                            # isInterRow = isInterRow*len(k.index)
                            # k.index = isInterRow
                            if len(isInterCol) == 1:
                                isInterCol = isInterCol*len(k.columns)
                                k.columns = isInterCol
                                # print(isInterCol)
                            else:
                                # print("CC")
                                # print(oriRow,oriCal)
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
                            if Coldi != []:
                                if Rowdi != []:
                                    print("Error",k.index)
                                    d = dict(k.index)
                                    d[list(d.keys())[0]] = isInterRow[0]
                                    k = k.rename(index=d)
                                else:
                                    k.index = isInterRow
                            if Rowdi != []:
                                # k.columns = Rowdi
                                d = dict(k.index)
                                d[list(d.keys())[0]] = isInterRow[0]
                                k = k.rename(index=d)
                                # print(k)
                    else:
                        k.index = isInterRow
                        k=k.unstack()
                else: #mes in col
                    print("meas in col")
                    k = pd.pivot_table(results,columns = colNum[len(Rowdi):beforMesual], index= colNum[:len(Rowdi)],values = colNum[beforMesual:],aggfunc=np.sum)
                    k = k.round(0)
                    # print(k)
                    if oriRow != []:
                        # print("c")
                        if len(isInterCol) == 1:
                            # print("c")
                            # print(k)
                            print(type(k.columns))
                            if type(k.columns) == pd.MultiIndex:
                                olddi = [list(ele) for ele in k.columns]
                                # isInterCol = k.columns.tolist()
                                # print(isInterCol)
                                # isInterCol = isInterCol*len(k.columns)
                                for i in range(len(k.columns)):
                                    buf = str(isInterCol[0])+" "+str(olddi[i][1])
                                    olddi[i] = buf
                                # print(olddi)
                                k.columns = olddi
                            # print(k.columns)
                        else:
                            # print(k.columns)
                            # print(oriRow,oriCal)
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
                        # results = results.groupby(0).sum().round(0).stack()
                        
                        k = pd.pivot_table(results,columns = colNum[:beforMesual],values = colNum[beforMesual:],aggfunc=np.sum)
                        k = k.round(0)
                        
                        k.index = isInterCol
                        # print("-------")
                        # k = k.unstack()
                k = k.replace(np.nan, '')
        # print(type(k))
        #print(k.index.tolist())
        if type(k) == pd.Series :
            k = k.to_frame()
        print(Row)
        print(Col)
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
    def SwapDiMeas(self,obj):
        rdf = len(self.df.columns)
        if obj in self.getDimension:
            movecolumn = self.df.pop(obj)
            self.df.insert(rdf-1,obj,movecolumn)
        elif obj in self.getMeasure:
            movecolumn = self.df.pop(obj)
            self.df.insert(0,obj,movecolumn)

        return self.df

    def print(self):
        print('\n--------------------------------------\n')
        print('path = ',self.path)
        print('hashfile =',(hashlib.md5(self.selectFile.encode('UTF-8')).hexdigest()))
        print('Dimen = ',self.getDimension())
        print('Meas = ',self.Measure)