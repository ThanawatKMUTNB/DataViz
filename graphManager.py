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
        self.DateDict = {}
        self.Chart = None
        self.dataFiltered = None

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

    def setDate(self):
        for i in list(self.DateDict.keys()):
            tmp = []
            tmp.append(i)
            tmp.append(self.DateDict[i])
            self.Measure.append(tmp)

        for i in range(len(self.RowChoose)):
            tmp = []
            print("------>",i,self.RowChoose[i])
            if self.RowChoose[i] in list(self.DateDict.keys()):
                tmp.append(self.RowChoose[i])
                tmp.append(self.DateDict[self.RowChoose[i]])
                self.RowChoose[i] = tmp
                
        for i in range(len(self.ColChoose)):
            tmp = []
            if self.ColChoose[i] in list(self.DateDict.keys()):
                tmp.append(self.ColChoose[i])
                tmp.append(self.DateDict[self.ColChoose[i]])
                self.ColChoose[i] = tmp
        
    def setList(self,row,col,mes,dataSheet,dateDic,dfOriginal):
        self.MeasureDic = mes
        self.RowChoose = row
        self.ColChoose = col
        self.DateDict = dateDic
        self.df = dataSheet
        # self.Measure = list(self.MeasureDic.keys())
        self.setMes()
        #self.setDate()
        print("Graph")
        # print(self.MeasureDic,self.Measure,self.RowChoose,self.ColChoose)
        #self.df['Order Date'] = pd.to_datetime(self.df['Order Date'],format='%d/%m/%Y')
        #self.df['Ship Date'] = pd.to_datetime(self.df['Ship Date'],format='%d/%m/%Y')
        
        # for d in ['Order Date','Ship Date']:
        #     self.filterDate(d,'year')
        #     self.filterDate(d,'month')
        #     self.filterDate(d,'day')
    
    def chooseChart(self,chart):
        row = self.RowChoose
        column = self.ColChoose
        Measure = []
        for m in self.Measure:
            Measure.append(m[0])
        Measure = list(set(Measure))

        def checkMeasure(R,C):      #True when row is measure
            for r in R:
                if type(r) == type([]):
                    if r[0] in Measure:
                        return True
                    else:
                        return False
                else:
                    return False
        #print(self.MeasureDic,self.Measure,self.RowChoose,self.ColChoose)
        
        if chart == 'Bar':
            mes = 'col'
            for r in row:
                if type(r) == type(['list']):
                    if r[0] in Measure:
                        mes = 'row'
            print(row,column)
            if mes == 'row':
                chart = []
                if type(row[0]) == type(['list']):  #Datetime and Meas
                    if row[0][0] not in Measure:    #Datetime
                        if row[1][0] not in Measure:       #4Dimension (Can't plot)
                            print('4 Dimension')
                            l = [*column]
                            l.append(row[0])
                            l.append(row[1])
                            for r in range(len(row)-2):
                                chart.append(self.plotBar([row[0],row[1],row[r+2]],column,row[r+2],l,mes))
                            return alt.vconcat(*chart)
                        else:
                            l = [*column]
                            l.append(row[0])
                            for r in range(len(row)-1):
                                chart.append(self.plotBar([row[0],row[r+1]],column,row[r+1],l,mes))
                            return alt.vconcat(*chart)
                    else:                           #Measure
                        for r in range(len(row)):
                            chart.append(self.plotBar([row[r]],column,row[r],[*column],mes))
                        return alt.vconcat(*chart)
                else:                               #Dimension
                    if row[1][0] not in Measure:       #4Dimension
                        l = [*column]
                        l.append(row[0])
                        l.append(row[1])
                        for r in range(len(row)-2):
                            chart.append(self.plotBar([row[0],row[1],row[r+2]],column,row[r+2],l,mes))
                        return alt.vconcat(*chart)
                    else:
                        l = [*column]
                        l.append(row[0])
                        for r in range(len(row)-1):
                            chart.append(self.plotBar([row[0],row[r+1]],column,row[r+1],l,mes))
                        return alt.vconcat(*chart)
            else:
                chart = []
                if type(column[0]) == type(['list']):
                    if column[0][0] not in Measure:
                        if column[1][0] not in Measure:
                            l = [*row]
                            l.append(column[0])
                            l.append(column[1])
                            for c in range(len(column)-2):
                                chart.append(self.plotBar(row,[column[0],column[1],column[c+2]],column[c+2],l,mes))
                            return alt.vconcat(*chart)
                        else:
                            l = [*row]
                            l.append(column[0])
                            for c in range(len(column)-1):
                                chart.append(self.plotBar(row,[column[0],column[c+1]],column[c+1],l,mes))
                            return alt.vconcat(*chart)
                    else:
                        for c in range(len(column)):
                            chart.append(self.plotBar(row,[column[c]],column[c],[*row],mes))
                        return alt.vconcat(*chart)
                else:
                    if column[1][0] not in Measure:
                        l = [*row]
                        l.append(column[0])
                        l.append(column[1])
                        for c in range(len(column)-2):
                            chart.append(self.plotBar(row,[column[0],column[1],column[c+2]],column[c+2],l,mes))
                        return alt.vconcat(*chart)
                    else:
                        l = [*row]
                        l.append(column[0])
                        for c in range(len(column)-1):
                            chart.append(self.plotBar(row,[column[0],column[c+1]],column[c+1],l,mes))
                        return alt.vconcat(*chart)


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
            mes = 'col'
            for r in row:
                if type(r) == type(['list']):
                    if r[0] in Measure:
                        mes = 'row'
            #print(mes)
            if mes == 'row':
                chart = []
                if type(row[0]) == type(['list']):  #Datetime and Meas
                    if row[0][0] not in Measure:    #Datetime
                        l = [*column]
                        l.append(row[0])
                        for r in range(len(row)-1):
                            chart.append(self.plotLine([row[0],row[r+1]],column,row[r+1],l,mes))
                        return alt.vconcat(*chart)
                    else:                           #Measure
                        for r in range(len(row)):
                            chart.append(self.plotLine([row[r]],column,row[r],[*column],mes))
                        return alt.vconcat(*chart)
                else:                               #Dimension
                    l = [*column]
                    l.append(row[0])
                    for r in range(len(row)-1):
                        chart.append(self.plotLine([row[0],row[r+1]],column,row[r+1],l,mes))
                    return alt.vconcat(*chart)
            else:
                chart = []
                if type(column[0]) == type(['list']):
                    if column[0][0] not in Measure:
                        l = [*row]
                        l.append(column[0])
                        for c in range(len(column)-1):
                            chart.append(self.plotLine(row,[column[0],column[c+1]],column[c+1],l,mes))
                        return alt.vconcat(*chart)
                    else:
                        for c in range(len(column)):
                            chart.append(self.plotLine(row,[column[c]],column[c],[*row],mes))
                        return alt.vconcat(*chart)
                else:
                    l = [*row]
                    l.append(column[0])
                    for c in range(len(column)-1):
                        chart.append(self.plotLine(row,[column[0],column[c+1]],column[c+1],l,mes))
                    return alt.vconcat(*chart)
    
    def filterDate(self,Dimension,typ): #Date inly
        # print(Dimension,typ)
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
        if fil == 'average':
            fil = 'mean'
        df = self.df
        if len(Di) == 1:
            if (type(Di[0]) == type(['list'])):
                x = str(Di[0][0]+' '+Di[0][1])
            else:
                x = Di[0]
            #print([x])
            tmax = df.groupby([x], as_index=False)[Meas[0]].agg(fil).max()[1]
            tmin = df.groupby([x], as_index=False)[Meas[0]].agg(fil).min()[1]
            
            if tmin > 0:
                tmin = 0
            elif tmax < 0 :
                tmax = 0
            return [tmin,tmax]

        elif (type(Di[0]) == type(['list'])) and (type(Di[1]) == type(['list'])):
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
        #print(col,x,Meas[0])
        #print(df.columns.tolist())
        tmax = df.groupby([col,x], as_index=False)[Meas[0]].agg(fil).max()[2]
        tmin = df.groupby([col,x], as_index=False)[Meas[0]].agg(fil).min()[2]
        
        if tmin > 0:
            tmin = 0
        elif tmax < 0 :
            tmax = 0
        
        return [tmin,tmax]

    def functionRC(self,row,column):
        lr = []
        lc = []

        for r in row:
            if type(r) == type(['list']):
                s = str(r[1]+'('+r[0]+')')
                lr.append(s)
            else:
                lr.append(r)

        for c in column:
            if type(c) == type(['list']):
                s = str(c[1]+'('+c[0]+')')
                lc.append(s)
            else:
                lc.append(c)
        
        return [lr,lc]

    def plotBar(self,row,column,meas,di,mes):
        print('\n\n\n',row,column)
        df = self.df
        Measure = self.Measure
        l = self.functionRC(row,column)
        lr = l[0]
        lc = l[1]
        if len(lr) == 2 and len(lc) == 0:           # 1 dimension and Measurement on row
            c = alt.Chart(df).mark_bar().encode(
                y= alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                tooltip = [lr[-2],lr[-1]]
            ).facet(row=lr[-2]
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c
        
        elif len(lr) == 0 and len(lc) == 2:         # 1 dimension and Measurement on column
            c = alt.Chart(df).mark_bar().encode(
                x= alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                tooltip = [lc[-2],lc[-1]]
            ).facet(column=lc[-2]
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c
        
        elif len(lr) == 1 and len(lc) == 1:         #1 dimension and Measurement with row and column
            c = alt.Chart(df).mark_bar().encode(
                x=lc[-1],
                y=lr[-1],
                tooltip = [lc[-1],lr[-1]]
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c
            
        elif len(lr) == 2 and len(lc) == 1:             
            if mes == 'row':
                c = alt.Chart(df).mark_bar().encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lr[-2],lr[-1],lc[-1]]
                ).facet(row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lr[-2],lr[-1],lc[-1]]
                ).facet(row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c

        elif len(lr) == 1 and len(lc) == 2:     #dimension2 date error
                    
            if mes == 'row':   
                c = alt.Chart(df).mark_bar().encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lc[-2],lr[-1],lc[-1]]
                ).facet(column=lc[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lc[-2],lr[-1],lc[-1]]
                ).facet(column=lc[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c

        elif len(lr) == 2 and len(lc) == 2:             ###################
            if mes == 'row':
                c = alt.Chart(df).mark_bar().encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lc[-2],lr[-1],lc[-2],lc[-1]]
                ).facet(column=lc[-2],row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lc[-2],lr[-1],lc[-2],lc[-1]]
                ).facet(column=lc[-2],row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c


        elif len(lr) == 1 and len(lc) == 3:
            if mes == 'row':                
                c = alt.Chart(df).mark_bar().encode(        #all Dimen on Col or Row
                    x=lc[-2],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    color = lc[-1],
                    tooltip = [lc[-3],lc[-2],lc[-1],lr[-1]]
                ).facet(column=lc[-3]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                if column[2][0] in Measure:
                    print('x=',lc[-2],'y=',lr[-1],'color=',lc[-1],'col=',lc[-3])
                    c = alt.Chart(df).mark_bar().encode(
                        x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                        y=lr[-1],
                        color = lc[-2],
                        tooltip = [lc[-3],lc[-2],lc[-1],lr[-1]]
                    ).facet(column=lc[-3]
                    ).resolve_scale(x = 'independent',y = 'independent')
                    self.Chart = c
                    
                else:
                    c = alt.Chart(df).mark_bar().encode(
                        x=alt.X(lc[-2],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                        y=lr[-1],
                        color = lc[-1],
                        tooltip = [lc[-3],lc[-2],lc[-1],lr[-1]]
                    ).facet(column=lc[-3]
                    ).resolve_scale(x = 'independent',y = 'independent')
                    self.Chart = c

        elif len(lr) == 3 and len(lc) == 1:
            if mes == 'row':
                if row[2][0] in Measure:
                    c = alt.Chart(df).mark_bar().encode(
                        x=lc[-1],
                        y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                        color = lr[-2],
                        tooltip = [lc[-1],lr[-3],lr[-2],lr[-1]]
                    ).facet(row=lr[-3]
                    ).resolve_scale(x = 'independent',y = 'independent')
                    self.Chart = c
                else:
                    c = alt.Chart(df).mark_bar().encode(
                        x=lc[-1],
                        y=alt.Y(lr[-2],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                        color = lr[-1],
                        tooltip = [lc[-1],lr[-3],lr[-2],lr[-1]]
                    ).facet(row=lr[-3]
                    ).resolve_scale(x = 'independent',y = 'independent')
                    self.Chart = c
            else:
                #print('x=',lc[-1],'y=',lr[-2],'color=',lr[-1],'row=',lr[-3])
                #print(di,meas)
                c = alt.Chart(df).mark_bar().encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-2],
                    color = lr[-1],
                    tooltip = [lc[-1],lr[-3],lr[-2],lr[-1]]
                ).facet(row=lr[-3]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c

        elif len(lr) == 3 and len(lc) == 2:
            #print('x=',lc[-1],'y=',lr[-1],'color=',lr[-2],'row=',lr[-3],'column=',lc[-2])
            c = alt.Chart(df).mark_bar().encode(
                x=lc[-1],
                y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                color = lr[-2],
                tooltip = [lc[-1],lr[-3],lr[-2],lr[-1]]
            ).facet(row=lr[-3] , column = lc[-2]
            ).resolve_scale(y = 'independent')
            self.Chart = c

        elif len(lr) == 2 and len(lc) == 3: 
            c = alt.Chart(df).mark_bar().encode(
                x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                y=lr[-1],
                color = lc[-2],
                tooltip = [lc[-3],lc[-2],lc[-1],lr[-1]]
            ).facet(column=lc[-3] , row = lr[-2]
            ).resolve_scale(x = 'independent')
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
        self.Chart = c
        return self.Chart
    
    def plotLine(self,row,column,meas,di,mes):
        df = self.df
        l = self.functionRC(row,column)
        lr = l[0]
        lc = l[1]

        if len(lr) == 1 and len(lc) == 1:         #1 dimension and Measurement with row and column
            c = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(lc[-1]),
                y=alt.Y(lr[-1]),
                tooltip = [lc[-1],lr[-1]]
            ).resolve_legend(size='independent')
            self.Chart = c
            
        elif len(lr) == 2 and len(lc) == 1:             
            if mes == 'row':
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lc[-1],lr[-1]]
                ).facet(row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lr[-1],lc[-1]]
                ).facet(row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c

        elif len(lr) == 1 and len(lc) == 2:     #dimension2 date error
            if mes == 'row':   
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lc[-1],lr[-1]]
                ).facet(column=lc[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lr[-1],lc[-1]]
                ).facet(column=lc[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c

        elif len(lr) == 2 and len(lc) == 2:             ###################
            if mes == 'row':
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=lc[-1],
                    y=alt.Y(lr[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    tooltip = [lc[-1],lr[-1]]
                ).facet(column=lc[-2],row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
            else:
                c = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X(lc[-1],scale=alt.Scale(domain=self.rangeScale(di,meas))),
                    y=lr[-1],
                    tooltip = [lr[-1],lc[-1]]
                ).facet(column=lc[-2],row=lr[-2]
                ).resolve_scale(x = 'independent',y = 'independent')
                self.Chart = c
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