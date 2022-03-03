import pandas as pd
from csvManager import csvManager

ex = csvManager()
ex.Measure = {'Sales':"sum",'Quantity':"sum",'Discount':"sum",'Profit':"average"}        
ex.df = pd.read_csv("Superstore.csv", encoding='windows-1252')

# ex.df = pd.read_csv("all-states-history.csv", encoding='windows-1252')

ex.getHead()
ex.typeDate = ex.readDate()
p = ex.getDataWithPandasByHead("Region")

# print(p.drop_duplicates().to_list())
# def getDi(n):
#     if n[-1] == ")":
#         j = n.index("(")
#         n = n[j+1:len(n)-1]
#     print(n)
#     return n

# getDi('YEAR(Order Date)')
# ex.readMeasure()


# ex.setRowAndColumn(["Segment"],[])
# ex.setRowAndColumn([],["Segment"])

# ex.setRowAndColumn([],[["Sales", 'sum']])
# ex.setRowAndColumn([["Sales", 'sum']],[])

# ex.setRowAndColumn([],["Sales","Profit"])
# ex.setRowAndColumn(["Sales","Profit"],[])

# ex.setRowAndColumn(["Segment","Sales"],[])
# ex.setRowAndColumn([],["Segment","Sales"])

# ex.setRowAndColumn(["Segment"],["Sales","Profit"])
# ex.setRowAndColumn(["Sales","Profit"],["Segment"])

# ex.setRowAndColumn(["Ship Mode","Segment"],["Sales"])
# ex.setRowAndColumn(["Sales"],["Ship Mode","Segment"])

# ex.setRowAndColumn(["Ship Mode","Segment"],["Sales","Profit"])
# ex.setRowAndColumn(["Sales","Profit"],["Ship Mode","Segment"])

# ex.setRowAndColumn(["Segment","Sales","Profit"],["Region"])
# ex.setRowAndColumn(["Region"],["Segment","Sales","Profit"])

# ex.setRowAndColumn(["Region","Segment"],["Region","Sales","Profit"])
# ex.setRowAndColumn(["Segment","Region"],["Ship Mode",["Profit","sum"],["Sales","sum"]])
# ex.setRowAndColumn(["Segment","Region","Sales","Profit"],[])

# ex.setRowAndColumn(["Segment","Profit","Sales"],[])
# ex.setRowAndColumn([],["Segment","Profit","Sales"])
# ex.setRowAndColumn(["Ship Mode",["Profit","sum"],["Sales","sum"]],["Segment","Region"])

# ex.setRowAndColumn(["Segment",["Sales","sum"]],["Category","Region"])
# ex.setRowAndColumn(["Category","Region"],["Segment",["Sales","sum"]])

# ex.setRowAndColumn(['Region'],[['Order Date', 'year'],"Segment", ['Discount', 'sum']])
# ex.setRowAndColumn(['Region',"Segment", ['Discount', 'sum']],[['Order Date', 'year']])

#
# ex.filter = {'Region': ['South', 'West', 'Central'], 'Ship Date year': ['2019', '2020']}
# ex.setRowAndColumn([],['Region', ['Ship Date','year']])

# ex.filter = {'Region': ['South', 'West'], 'Ship Date year': ['2019', '2020']}
# ex.setRowAndColumn([],['Region', 'Ship Date year'])

###
# ex.filter = {'Discount': [300, 558], 'Region': ['West', 'South', 'East', 'Central']}
# ex.filter = {'Ship Date year': [2019, 2018, 2017, 2020]}
# ex.setRowAndColumn([['Sales', 'sum']],[['Ship Date','year']])

# ex.setRowAndColumn([],[["Sales",'average'],["Profit",'sum']])
# ex.setRowAndColumn([["Sales",'average'],["Profit",'sum'],["Profit",'sum']],[])

# ex.setRowAndColumn(['Region',["Profit",'average'],["Profit",'average']],[])
# ex.setRowAndColumn([],['Region',["Profit",'average'],["Profit",'average']])

# ex.setRowAndColumn(['Region',["Profit",'sum'],["Sales",'average']],[])
ex.setRowAndColumn(['Region',["Profit",'count']],[])

# ex.setRowAndColumn([],['Region',['Ship Date', 'year']])
