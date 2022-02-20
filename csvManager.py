from itertools import chain
import os
from re import S
import numpy as np
import pandas as pd
#import mPageByCookie
class csvManager:
    def __init__(self):
        self.selectFile = ""
        self.path = ""
        self.df = ""
        self.Measure = {}
        self.filter = {}
        self.Head = []
        self.usemes = []
        self.func = []
    
    def setPath(self):
        pathBuf = os.path.join(self.path,self.selectFile) 
        self.df = self.readFile(pathBuf)
    
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
    
    def getHead(self):
        self.Head = list(self.df.columns)
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
    Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
    
    def setDataFilter(self,Row,Col):
        for i in list(self.filter.keys()):
            if i not in Row+Col:
                self.filter.pop(i)
        for i in Row+Col:
            if i not in list(self.filter.keys()):
                self.filter[i] = ""
        for i in list(self.filter.keys()):
            if self.filter[i] == "":
                self.filter[i] = list(set(self.df[i].values))
        self.dfFil = self.df
        for i in self.filter.keys():
            self.dfFil = self.dfFil[self.dfFil[i].isin(self.filter[i])]
        # print(self.dfFil)
        
                
    def setRowAndColumn(self,Row,Col):
        # print("CMS")
        # print(Row,Col)
        usedata = self.df
        if self.filter != {}:
            self.setDataFilter(Row,Col)
            usedata = self.dfFil
        oriRow = Row
        oriCal = Col
        
        for i in range(len(Row)):
            # print(i)
            if type(Row[i]) == list:
                # print(Row[i])
                Row[i]=Row[i][0]
        
        for i in range(len(Col)):
            # print(i)
            if type(Col[i]) == list:
                # print(Col[i])
                Col[i]=Col[i][0]
                
        # print(Row,Col)
        
        # self.df = pd.DataFrame({'col1': [0, 1, 2], 'col2': [10, 11, 12]})
        # isInterRow = list(set.intersection(set(Row) & set(self.Measure.keys())))
        # isInterCol = list(set.intersection(set(Col) & set(self.Measure.keys())))
        isInterRow = list(set(Row).intersection(set(self.Measure.keys())))
        isInterCol = list(set(Col).intersection(set(self.Measure.keys())))
        # print("****",isInterRow,isInterCol)
        if isInterRow == [] and isInterCol == []: #No Mes
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
            #print(Row,Col)
            #print(type(k))
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
                                print(oriRow,oriCal)
                                print(k)
                                print(Coldi,k.columns,isInterCol)
                                print(Rowdi,k.index,isInterRow)
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
                    print("mes in col")
                    
                    if Rowdi != []:
                        k = pd.pivot_table(results,columns = colNum[len(Rowdi):beforMesual], index= colNum[:len(Rowdi)],values = colNum[beforMesual:],aggfunc=np.sum)
                        k = k.round(0)
                        if len(isInterCol) == 1:
                            isInterCol = isInterCol*len(k.columns)
                            k.columns = isInterCol
                            # print(isInterCol)
                        else:
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
                    else :
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
        
        #list_of_lists = [list(elem) for elem in k.index.tolist()]
        
        #print(list_of_lists)
        #print(len(k))
        # print(type(k))
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
        # print(Row,Col)
        print(k)
        return k