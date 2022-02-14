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
        self.Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
        self.RowChoose = []
        self.ColChoose = []
        #self.Chart = None

    def setList(self,row,col,dataSheet):
        self.RowChoose = row
        self.ColChoose = col
        self.df = dataSheet
        self.df['Order Date'] = pd.to_datetime(self.df['Order Date'],format='%d/%m/%Y')
        self.df['Ship Date'] = pd.to_datetime(self.df['Ship Date'],format='%d/%m/%Y')
    
    def chooseChart(self,chart):
        row = self.RowChoose
        column = self.ColChoose
        f = 'sum'
        def checkMeasure(R,C):      #True when row is measure
            for r in R:
                if r in self.Measure:
                    return True
                else:
                    return False
        if chart == 'Bar':
            if checkMeasure(row,column):    #row is measure
                if len(row) == 1:
                    return alt.vconcat(self.plotBar(row[0],column,f))
                elif len(row) == 2:
                    return alt.vconcat(self.plotBar(row[0],column,f),self.plotBar(row[1],column,f))
                elif len(row) == 3:
                    return alt.vconcat(self.plotBar(row[0],column,f),self.plotBar(row[1],column,f),self.plotBar(row[2],column,f))
                elif len(row) == 4:
                    return alt.vconcat(self.plotBar(row[0],column,f),self.plotBar(row[1],column,f),self.plotBar(row[2],column,f),self.plotBar(row[3],column,f))
            else:
                if len(column) == 1:
                    return alt.hconcat(self.plotBar(row,column[0],f))
                elif len(column) == 2:
                    return alt.hconcat(self.plotBar(row,column[0],f),self.plotBar(row,column[1],f))
                elif len(column) == 3:
                    return alt.hconcat(self.plotBar(row,column[0],f),self.plotBar(row,column[1],f),self.plotBar(row,column[2],f))
                elif len(column) == 4:
                    return alt.hconcat(self.plotBar(row,column[0],f),self.plotBar(row,column[1],f),self.plotBar(row,column[2],f),self.plotBar(row,column[3],f))
        elif chart == 'Pie':
            return self.plotPie(row,column,f)
        elif chart == 'Line':
            if checkMeasure(row,column):    #row is measure
                if len(row) == 1:
                    return alt.vconcat(self.plotLine(row[0],column,f))
                elif len(row) == 2:
                    return alt.vconcat(self.plotLine(row[0],column,f),self.plotLine(row[1],column,f))
                elif len(row) == 3:
                    return alt.vconcat(self.plotLine(row[0],column,f),self.plotLine(row[1],column,f),self.plotLine(row[2],column,f))
                elif len(row) == 4:
                    return alt.vconcat(self.plotLine(row[0],column,f),self.plotLine(row[1],column,f),self.plotLine(row[2],column,f),self.plotLine(row[3],column,f))
            else:                       #column is Measurement
                if len(column) == 1:
                    return self.plotLine(row,column[0],f)
                elif len(column) == 2:
                    return alt.hconcat(self.plotLine(row,column[0],f),self.plotLine(row,column[1],f))
                elif len(column) == 3:
                    return alt.hconcat(self.plotLine(row,column[0],f),self.plotLine(row,column[1],f),self.plotLine(row,column[2],f))
                elif len(column) == 4:
                    return alt.hconcat(self.plotLine(row,column[0],f),self.plotLine(row,column[1],f),self.plotLine(row,column[2],f),self.plotLine(row,column[3],f))
    
    def filterDate(self,Dimension,typ): #Date inly

        self.df[Dimension] = pd.to_datetime(self.df['Order Date'],format='%d/%m/%Y')

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

    def plotBar(self,row,column,f):

        fd = 'month'                                ###month
        fil = f             ###sum
        if len(column) == 1 or len(row) == 1:     #column 1 , row 1
            if type(row) == type('string'):               #Measure in Row
                sy = str(fil+'('+row+')')
            else:
                if self.df[row[0]].dtypes == 'datetime64[ns]':   #Dimension(Datetime) in Row
                    sy = str(fd+'('+row[0]+')')
                else:
                    sy = str(row[0])                        #normal Dimension in Row

            if type(column) == type('string'):           #Measure in Column
                sx = str(fil+'('+column+')')
            else:
                if self.df[column[0]].dtypes == 'datetime64[ns]':    #Dimension(Datetime) in column
                    sx = str(fd+'('+column[0]+')')
                else:
                    sx = str(column[0])                     #normal Dimension in Column
            #print(row,column,sx,sy)
            
            c = alt.Chart(self.df).mark_bar().encode(
                x=sx,
                y=sy,
                tooltip = [sy,sx]
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c
            return self.Chart
        else:
                                            #2 Dimension
            if type(row) == type('string') :               #2 Column (Dimension)
                Di = column
                Me = row
                if self.df[Di[-2]].dtypes == 'datetime64[ns]':
                    scol = str(fd+'('+Di[-2]+')')           
                    sx = str(Di[-1])
                elif self.df[Di[-1]].dtypes == 'datetime64[ns]':
                    scol = str(Di[-2])
                    sx = str(fd+'('+Di[-1]+')')
                else:
                    scol = str(Di[-2])                      #column > x
                    sx = str(Di[-1])

                c = alt.Chart(self.df).mark_bar().encode(
                    x=sx,
                    y=str(fil+'('+Me+')'),
                    #color=scol,
                    tooltip = [sx,str(fil+'('+Me+')')]
                ).facet(column=scol
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            elif type(column) == type('string'):                 #2 Row (Dimension)
                Di = row    
                Me = column
                if self.df[Di[-2]].dtypes == 'datetime64[ns]':            #year,date error (large data)
                    srow = str(fd+'('+Di[-2]+')')
                    sy = str(Di[-1])

                elif self.df[Di[-1]].dtypes == 'datetime64[ns]':
                    srow = str(Di[-2])
                    sy = str(fd+'('+Di[-1]+')')
                else:
                    srow = str(Di[-2])
                    sy = str(Di[-1])
                c = alt.Chart(self.df).mark_bar().encode(
                    x=str(fil+'('+Me+')'),
                    y=sy,
                    #color=srow,
                    tooltip = [sy,str(fil+'('+Me+')')]
                ).facet(row=srow
                ).resolve_scale(y = 'independent',x = 'independent')
                self.Chart = c
            return self.Chart
    
    def exam(self):
        print(self.RowChoose,self.ColChoose)
        #print(self.df)
        c = alt.Chart(self.df).mark_bar().encode(
            x=str(self.ColChoose[0]),
            y=str(self.RowChoose[0]),
            #color=str(self.RowChoose[0]+':N')
        ).facet(column=str(self.RowChoose[0]+':N')
        ).resolve_scale(x = 'independent')
        return c
    
    def plotLine(self,row,column,f):

        fil = f                                        ###sum
        fd = 'month'                                        ###month
        if type(column) == type('string'):                 #column is Measure
            if len(row) == 1:
                #if df[row[0]].dtypes == 'datetime64[ns]':
                Di = row[0]
                Me = column
                ch = alt.Chart(self.df).mark_line(point=True).encode(
                    alt.X(str(fil+'('+Me+'):Q')),
                    alt.Y(str(fd+'('+Di+'):T')),
                    tooltip = [str(fd+'('+Di+'):T'),str(fil+'('+Me+'):Q')]
                )
                self.Chart = ch
            else:
                Me = column
                ch = alt.Chart(self.df).mark_line(point=True).encode(
                    alt.X(str(fil+'('+Me+'):Q')),
                    alt.Y(
                        alt.repeat('layer'),timeUnit = fd,type='temporal',
                    ),
                    color = alt.datum(alt.repeat('layer')),
                    tooltip = [str(fil+'('+Me+')')]
                ).repeat(layer=[row[0],row[1]]
                ).resolve_legend(
                    size='independent'
                )
                self.Chart = ch
        else:   #row is Measure

            #elif df[c].dtypes == 'datetime64[ns]':
            if len(column) == 1:
                Me = row
                Di = column[0]
                ch = alt.Chart(self.df).mark_line(point=True).encode(
                    alt.X(str(fd+'('+Di+'):T')),
                    alt.Y(str(fil+'('+Me+'):Q')),
                    tooltip = [str(fd+'('+Di+'):T'),str(fil+'('+Me+'):Q')]
                )
                self.Chart = ch
            else:
                Me = row
                ch = alt.Chart(self.df).mark_line(point=True).encode(
                    alt.X(
                        alt.repeat('layer'),timeUnit = fd,type='temporal',
                    ),
                    alt.Y(str(fil+'('+Me+'):Q')),
                    color = alt.datum(alt.repeat('layer')),
                    tooltip = [str(fil+'('+Me+')')]
                ).repeat(layer=[column[0],column[1]]
                ).resolve_legend(
                    size='independent'
                )
                self.Chart = ch
            #self.plotChart()
        return self.Chart

    def plotPie(self,row,column,f):
        row = self.RowChoose
        column = self.ColChoose
        if not (len(column) == 1 and len(row) == 1):
            return 0
        fil = f                                       ####sum
        fd = 'year'                                       ####year
        if row[0] in self.Measure:
            Mes = row[0]
            Di = column[0]
        elif column[0] in self.Measure:
            Mes = column[0]
            Di = row[0]

        if self.df[Di].dtypes == 'datetime64[ns]':
            s = str(fd+'('+Di+'):T')
        else:
            s = str(Di+':N')

        pie = alt.Chart(self.df).mark_arc().encode(
            theta=alt.Theta(str(fil+'('+Mes+'):Q')), 
            color=alt.Color(s, type="nominal"), 
            tooltip = [s,str(fil+'('+Mes+'):Q')]
        )
        self.Chart = pie
        return self.Chart
        #self.plotChart()