import altair as alt
from altair import pipe, limit_rows, to_values
import altair_viewer
import pandas as pd

'''t = lambda data: pipe(data, limit_rows(max_rows=10000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')'''
alt.data_transformers.disable_max_rows()
altair_viewer._global_viewer._use_bundled_js = False
alt.data_transformers.enable('data_server')

'''df = pd.read_csv('Superstore.csv', encoding='windows-1252')
df['Order Date'] = pd.to_datetime(df['Order Date'],format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'],format='%d/%m/%Y')'''

class graphManager():

    def __init__(self):
        self.df = None
        self.Measure = []
        self.MeasureDic = {}
        self.RowChoose = []
        self.ColChoose = []
        self.Chart = None

    def setMes(self):
        for i in list(self.MeasureDic.keys()):
            tmp = []
            tmp.append(i)
            tmp.append(self.MeasureDic[i])
            self.Measure.append(tmp)
            
        for i in range(len(self.RowChoose)):
            tmp = []
            print("------>",i,self.RowChoose[i])
            if self.RowChoose[i] in list(self.MeasureDic.keys()):
                tmp.append(self.RowChoose[i])
                tmp.append(self.MeasureDic[self.RowChoose[i]])
                self.RowChoose[i] = tmp
                
        for i in range(len(self.ColChoose)):
            tmp = []
            if self.ColChoose[i] in list(self.MeasureDic.keys()):
                tmp.append(self.ColChoose[i])
                tmp.append(self.MeasureDic[self.ColChoose[i]])
                self.ColChoose[i] = tmp
        
    def setList(self,row,col,mes,dataSheet):
        self.MeasureDic = mes
        self.RowChoose = row
        self.ColChoose = col
        # self.Measure = list(self.MeasureDic.keys())
        self.setMes()
        self.df = dataSheet
        print("Graph")
        print(self.MeasureDic,self.Measure,self.RowChoose,self.ColChoose)
        #self.df['Order Date'] = pd.to_datetime(self.df['Order Date'],format='%d/%m/%Y')
        #self.df['Ship Date'] = pd.to_datetime(self.df['Ship Date'],format='%d/%m/%Y')
        
        for d in ['Order Date','Ship Date']:
            self.filterDate(d,'year')
            self.filterDate(d,'month')
            self.filterDate(d,'day')
    
    def chooseChart(self,chart):
        row = self.RowChoose
        column = self.ColChoose
        def checkMeasure(R,C):      #True when row is measure
            for r in R:
                if type(r) == type([]):
                    if r[0] in self.Measure:
                        return True
                    else:
                        return False
                else:
                    return False
        print(self.MeasureDic,self.Measure,self.RowChoose,self.ColChoose)
        
        if chart == 'Bar':
            #return self.exam()
            #print(self.df)
            if checkMeasure(row,column):    #row is measure
                print('row is measurement')
                if len(column) > 2:
                    print('column 3 Dimen')
                    return self.plotBar(row,column,'row',len(column))
                chart = []
                for r in row:
                    chart.append(self.plotBar(r,column,'row',len(column)))
                return alt.vconcat(*chart)
            else:
                print('column is measurement')
                if len(row) > 2:
                    print('row is 3 Dimen')
                    return self.plotBar(row,column,'column',len(row))
                chart = []
                for c in column:
                    chart.append(self.plotBar(row,c,'column',len(row)))
                return alt.hconcat(*chart)

        elif chart == 'Pie':
            if checkMeasure(row,column):    #row is measure
                print('row is measurement')
                chart = []
                for r in row:
                    chart.append(self.plotPie(r,column,'row'))
                return alt.vconcat(*chart)
            else:
                print('column is measurement')
                chart = []
                for c in column:
                    chart.append(self.plotPie(row,c,'column'))
                return alt.hconcat(*chart)
        elif chart == 'Line':
            if checkMeasure(row,column):    #row is measure
                print('row is measurement')
                chart = []
                for r in row:
                    chart.append(self.plotLine(r,column,'row',len(column)))
                return alt.vconcat(*chart)
            else:                       #column is Measurement
                print('column is measurement')
                chart = []
                for c in column:
                    chart.append(self.plotLine(row,c,'column',len(row)))
                return alt.hconcat(*chart)
    
    def filterDate(self,Dimension,typ): #Date inly

        self.df[Dimension] = pd.to_datetime(self.df[Dimension],format='%d/%m/%Y')

        if typ == 'year':
            s = str(Dimension+' year')
            self.df[s] = self.df[Dimension].dt.year
            return self.df[s]
        elif typ == 'month':
            s = str(Dimension+' month')
            self.df[s] = self.df[Dimension].dt.month
            return self.df[s]
        elif typ == 'day':
            s = str(Dimension+' day')
            self.df[s] = self.df[Dimension].dt.day
            return self.df[s]

    def rangeScale(self,Di,Meas):
        fil = Meas[1]
        df = self.df
        if len(Di) == 2:
            if (type(Di[0]) == type(['list'])) and (type(Di[1]) == type(['list'])):
                x = str(Di[1][0]+' '+Di[1][1])
                col = str(Di[0][0]+' '+Di[0][1])
            elif type(Di[0]) == type(['list']):
                x = Di[1]
                col = str(Di[0][0]+' '+Di[0][1])
            elif type(Di[1]) == type(['list']):
                x = str(Di[1][0]+' '+Di[1][1])
                col = Di[0]
            else:
                x = Di[1]
                col = Di[0]
            
            if fil == 'average':
                fil = 'mean'

            tmax = df.groupby([col,x], as_index=False)[Meas[0]].agg(fil).max()[2]
            tmin = df.groupby([col,x], as_index=False)[Meas[0]].agg(fil).min()[2]
        
            if tmin > 0:
                tmin = 0
            elif tmax < 0 :
                tmax = 0
            
            return [tmin,tmax]
        return

    def plotBar(self,row,column,mes,dimen):

        print(row,column)
        df = self.df
        if dimen == 1:     #column 1 , row 1
            print('1 Dimension')
            if mes == 'row':               #Measure in Row
                sy = str(row[1]+'('+row[0]+')')
            else:
                if type(row[0]) == type(['datetime']):
                #if df[row[0]].dtypes == 'datetime64[ns]':   #Dimension(Datetime) in Row
                    sy = str(row[0][1]+'('+row[0][0]+')')
                else:
                    sy = str(row[0])                        #normal Dimension in Row

            if mes == 'column':           #Measure in Column
                sx = str(column[1]+'('+column[0]+')')
            else:
                if type(column[0]) == type(['datetime']):
                #if df[column[0]].dtypes == 'datetime64[ns]':    #Dimension(Datetime) in column
                    sx = str(column[0][1]+'('+column[0][0]+')')
                else:
                    sx = str(column[0])                     #normal Dimension in Column
            
            c = alt.Chart(df).mark_bar().encode(
                x=sx,
                y=sy,
                tooltip = [sy,sx]
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c

        elif dimen == 2:
            print('2 Dimension')                                  #2 Dimension
            if mes == 'row' :               #2 Column (Dimension)
                Di = column
                Me = row[0]
                fil = row[1]

                if (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])):   #index 0 is Dimension , index 1 is function
                    Col = Di[-2][0]
                    X = Di[-1][0]
                    scol = str(Di[-2][1]+'('+Col+')')           
                    sx = str(Di[-1][1]+'('+X+')')
                elif type(Di[-2]) == type(['datetime']):
                    Col = Di[-2][0]
                    scol = str(Di[-2][1]+'('+Col+')')           
                    sx = str(Di[-1])
                elif type(Di[-1]) == type(['datetime']):
                    X = Di[-1][0]
                    scol = str(Di[-2])
                    sx = str(Di[-1][1]+'('+X+')')
                else:
                    scol = str(Di[-2])                      #column > x
                    sx = str(Di[-1])

                c = alt.Chart(df).mark_bar().encode(
                    x=sx,
                    y=alt.Y(str(fil+'('+Me+')'),scale=alt.Scale(domain=self.rangeScale(Di,row))),
                    #color=scol,
                    tooltip = [sx,str(fil+'('+Me+')')]
                ).facet(column=scol
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            elif mes == 'column':                 #2 Row (Dimension)
                Di = row    
                Me = column[0]
                fil = column[1]

                if (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])):
                    srow = str(Di[-2][1]+'('+Di[-2][0]+')')           
                    sy = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif type(Di[-2]) == type(['datetime']):            #year,date error (large data)
                    srow = str(Di[-2][1]+'('+Di[-2][0]+')')
                    sy = str(Di[-1])
                elif type(Di[-1]) == type(['datetime']):
                    srow = str(Di[-2])
                    sy = str(Di[-1][1]+'('+Di[-1][0]+')')
                else:
                    srow = str(Di[-2])
                    sy = str(Di[-1])
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(str(fil+'('+Me+')'),scale=alt.Scale(domain=self.rangeScale(Di,column))),
                    y=sy,
                    #color=srow,
                    tooltip = [sy,str(fil+'('+Me+')')]
                ).facet(row=srow
                ).resolve_scale(y = 'independent',x = 'independent')
                self.Chart = c
        elif dimen == 3:   #3 Dimension
            print('3 Dimension')
            if mes == 'row' :               #2 Column (Dimension)
                Di = column
                Me = row[0][0]
                fil = row[0][1]

                if (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    scol = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sx = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])):
                    scol = str(Di[-3])
                    sx = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-1]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    scol = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sx = str(Di[-2])
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-2]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    scol = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sx = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1])
                elif type(Di[-2]) == type(['datetime']):          
                    scol = str(Di[-3])
                    sx = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1])
                elif type(Di[-1]) == type(['datetime']):
                    scol = str(Di[-3])
                    sx = str(Di[-2])
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif type(Di[-3]) == type(['datetime']):
                    scol = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sx = str(Di[-2])
                    scolor = str(Di[-1])
                else:
                    scol = str(Di[-3])                      #column > x > color
                    sx = str(Di[-2])
                    scolor = str(Di[-1])
                c = alt.Chart(df).mark_bar().encode(
                    x=sx,
                    y=alt.Y(str(fil+'('+Me+')'),scale=alt.Scale(domain=self.rangeScale([Di[1],Di[2]],row[0]))),
                    color=scolor,
                    tooltip = [scolor,sx,str(fil+'('+Me+')')]
                ).facet(column=scol
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            elif mes == 'column':                 #2 Row (Dimension)
                Di = row    
                Me = column[0][0]
                fil = column[0][1]

                if (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    srow = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sy = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-1]) == type(['datetime'])) and (type(Di[-2]) == type(['datetime'])):
                    srow = str(Di[-3])
                    sy = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-1]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    srow = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sy = str(Di[-2])
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif (type(Di[-2]) == type(['datetime'])) and (type(Di[-3]) == type(['datetime'])):
                    srow = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sy = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1])
                elif type(Di[-2]) == type(['datetime']):        
                    srow = str(Di[-3])
                    sy = str(Di[-2][1]+'('+Di[-2][0]+')')
                    scolor = str(Di[-1])
                elif type(Di[-1]) == type(['datetime']):
                    srow = str(Di[-3])
                    sy = str(Di[-2])
                    scolor = str(Di[-1][1]+'('+Di[-1][0]+')')
                elif type(Di[-3]) == type(['datetime']):
                    srow = str(Di[-3][1]+'('+Di[-3][0]+')')
                    sy = str(Di[-2])
                    scolor = str(Di[-1])
                else:
                    srow = str(Di[-3])                      #column > x > color
                    sy = str(Di[-2])
                    scolor = str(Di[-1])
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(str(fil+'('+Me+')'),scale=alt.Scale(domain=self.rangeScale([Di[1],Di[2]],column[0]))),
                    y=sy,
                    color=scolor,
                    tooltip = [scolor,sy,str(fil+'('+Me+')')]
                ).facet(row=srow
                ).resolve_scale(y = 'independent',x = 'independent')
                self.Chart = c
        return self.Chart
    
    def exam(self):
        print(self.RowChoose,self.ColChoose)
        #print(self.df)
        c = alt.Chart(self.df).mark_bar().encode(
            x=str('Category'),
            y=str('sum(Profit)'),
            #color=str(self.RowChoose[0]+':N')
        ).resolve_scale(x = 'independent')
        return c
    
    def plotLine(self,row,column,mes,Dimen):

        print(row,column)
        df = self.df
        if mes == 'column':                 #column is Measure
            fil = column[1]
            Me = column[0]
            if Dimen == 1:
                Di = row[0][0]
                fd = row[0][1]
                ch = alt.Chart(df).mark_line(point=True).encode(
                    alt.X(str(fil+'('+Me+'):Q')),
                    alt.Y(str(fd+'('+Di+'):T')),
                    tooltip = [str(fd+'('+Di+'):T'),str(fil+'('+Me+'):Q')]
                )
                self.Chart = ch
            elif Dimen == 2:
                ch = alt.Chart(df).mark_line(point=True).encode(
                    alt.X(str(fil+'('+Me+'):Q'),scale=alt.Scale(domain=self.rangeScale([row[0],row[1]],column))),
                    alt.Y(str(row[-1][1]+'('+row[-1][0]+'):T')),
                    row = str(row[-2][1]+'('+row[-2][0]+'):T'),
                    tooltip = [str(row[-1][1]+'('+row[-1][0]+'):T'),str(fil+'('+Me+')')]
                ).resolve_legend(
                    size='independent'
                ).resolve_scale(
                    y = 'independent',x = 'independent'
                )
                self.Chart = ch

        elif mes == 'row':   #row is Measure
            Me = row[0]
            fil = row[1]
            #elif df[c].dtypes == 'datetime64[ns]':
            if Dimen == 1:
                Di = column[0][0]
                fd = column[0][1]
                ch = alt.Chart(df).mark_line(point=True).encode(
                    alt.X(str(fd+'('+Di+'):T')),
                    alt.Y(str(fil+'('+Me+'):Q')),
                    tooltip = [str(fd+'('+Di+'):T'),str(fil+'('+Me+'):Q')]
                )
                self.Chart = ch
            elif Dimen == 2:
                ch = alt.Chart(df).mark_line(point=True).encode(
                    alt.Y(str(fil+'('+Me+'):Q'),scale=alt.Scale(domain=self.rangeScale([column[0],column[1]],row))),
                    alt.X(str(column[-1][1]+'('+column[-1][0]+'):T')),
                    column = str(column[-2][1]+'('+column[-2][0]+'):T'),
                    tooltip = [str(column[-1][1]+'('+column[-1][0]+'):T'),str(fil+'('+Me+')')]
                ).resolve_legend(
                    size='independent'
                ).resolve_scale(
                    y = 'independent',x = 'independent'
                )
                self.Chart = ch
        return self.Chart

    def plotPie(self,row,column,mes):
        if mes == 'row':
            Mes = row[0]
            fil = row[1]
            Di = column[0]
        elif mes == 'column':
            Mes = column[0]
            fil = column[1]
            Di = row[0]

        if type(Di) == type([]):
            s = str(Di[1]+'('+Di[0]+'):T')
        else:
            s = str(Di+':N')

        base = alt.Chart(self.df).mark_arc().encode(
            theta=alt.Theta(str(fil+'('+Mes+'):Q')), 
            color=alt.Color(s, type="nominal"), 
            tooltip = [s,str(fil+'('+Mes+'):Q')]
        )

        self.Chart = base
        return self.Chart
        #self.plotChart()