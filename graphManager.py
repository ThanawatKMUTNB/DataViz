import altair as alt
from altair import pipe, limit_rows, to_values
import altair_viewer
t = lambda data: pipe(data, limit_rows(max_rows=10000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')
alt.data_transformers.disable_max_rows()
altair_viewer._global_viewer._use_bundled_js = False
alt.data_transformers.enable('data_server')

class graphManager(object):

    def __init__(self):
        self.df = None
        self.Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
        self.RowChoose = []
        self.ColChoose = []
        self.Chart = None

    def plotBar(self):
        row = self.RowChoose
        column = self.ColChoose
        fil = 'sum'                            ###sum
        fd = 'month'                            ###month
        if len(column) == 1 and len(row) == 1:
            if row[0] in self.Measure:
                sy = str(fil+'('+row[0]+'):Q')
                st = sy
            else:
                if self.data[row[0]].dtypes == 'datetime64[ns]':
                    #fd = 'month' 
                    sy = str(fd+'('+row[0]+'):T')
                else:
                    sy = str(row[0]+':N')
            if column[0] in self.Measure:
                sx = str(fil+'('+column[0]+'):Q')
                st = sx
            else:
                if self.data[column[0]].dtypes == 'datetime64[ns]':
                    #fd = 'month' 
                    sx = str(fd+'('+column[0]+'):T')
                else:
                    sx = str(column[0]+':N')

            c = alt.Chart(self.data).mark_bar().encode(
                x=sx,
                y=sy,
                tooltip = st
            ).resolve_scale(x = 'independent',y = 'independent')
            self.Chart = c
            #self.plotChart()
        else:
            if len(column) > 1 and len(column) <= 2:
                Di = column
                Me = row
                if self.data[Di[0]].dtypes == 'datetime64[ns]':
                    scol = str(fd+'('+Di[0]+'):T')
                    sx = str(Di[-1]+':N')
                elif self.data[Di[-1]].dtypes == 'datetime64[ns]':
                    scol = str(Di[0]+':N')
                    sx = str(fd+'('+Di[-1]+'):T')
                else:
                    scol = str(Di[0]+':N')
                    sx = str(Di[-1]+':N')

                c = alt.Chart(self.data).mark_bar().encode(
                    x=sx,
                    y=str(fil+'('+Me[0]+'):Q'),
                    color=scol,
                    tooltip = str(fil+'('+Me[0]+'):Q')
                ).facet(column=scol
                ).resolve_scale(x = 'independent')
                self.Chart = c
                #self.plotChart()

            elif len(row) > 1 and len(row) <= 2:
                Di = row
                Me = column
                if self.data[Di[0]].dtypes == 'datetime64[ns]':            #year,date error (large data)
                    srow = str(fd+'('+Di[0]+'):T')
                    sy = str(Di[-1]+':N')
                    #print(srow)
                    #print(sy)
                elif self.data[Di[-1]].dtypes == 'datetime64[ns]':
                    srow = str(Di[0]+':N')
                    sy = str(fd+'('+Di[-1]+'):T')
                else:
                    srow = str(Di[0]+':N')
                    sy = str(Di[-1]+':N')

                c = alt.Chart(self.data).mark_bar().encode(
                    x=str(fil+'('+Me[0]+'):Q'),
                    y=sy,
                    color=srow,
                    tooltip = str(fil+'('+Me[0]+'):Q')
                ).facet(row=srow
                ).resolve_scale(y = 'independent')
                self.Chart = c
                #self.plotChart()
            else:
                return 'Pls enter 1 or 2 Dimension'
            
    def plotLine(self):
        row = self.RowChoose
        column = self.ColChoose
        if not (len(column) == 1 and len(row) == 1):
            return
        fil = 'sum'                                        ###sum
        fd = 'month'                                        ###month
        if self.data[row[0]].dtypes == 'datetime64[ns]':
            Di = row[0]
            Me = column[0]
            c = alt.Chart(self.data).mark_line(point=True).encode(
                alt.X(str(fil+'('+Me+'):Q')),
                alt.Y(str(fd+'('+Di+'):T')),
                tooltip = str(fil+'('+Me+'):Q')
            )
            self.Chart = c
            #self.plotChart()

        elif self.data[column[0]].dtypes == 'datetime64[ns]':
            Me = row[0]
            Di = column[0]
            c = alt.Chart(self.data).mark_line(point=True).encode(
                alt.X(str(fd+'('+Di+'):T')),
                alt.Y(str(fil+'('+Me+'):Q')),
                tooltip = str(fil+'('+Me+'):Q')
            )
            self.Chart = c
            #self.plotChart()
        else:
            return

    def plotPie(self):
        row = self.RowChoose
        column = self.ColChoose
        if not (len(column) == 1 and len(row) == 1):
            return
        fil = 'sum'                                       ####sum
        fd = 'year'                                       ####year
        if row[0] in self.Measure:
            Mes = row[0]
            Di = column[0]
        elif column[0] in self.Measure:
            Mes = column[0]
            Di = row[0]

        if self.data[Di].dtypes == 'datetime64[ns]':
            s = str(fd+'('+Di+'):T')
        else:
            s = str(Di+':N')

        base = alt.Chart(self.data).encode(
            theta=alt.Theta(str(fil+'('+Mes+'):Q')), 
            color=alt.Color(s, type="nominal"), 
            tooltip = str(fil+'('+Mes+'):Q')
        )

        pie = base.mark_arc(outerRadius=120)
        self.Chart = pie
        #self.plotChart()