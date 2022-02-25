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


# ex.setRowCol(["Segment"],[])
# ex.setRowCol([],["Segment"])

# ex.setRowCol([],["Sales"])
# ex.setRowCol(["Sales"],[])

# ex.setRowCol([],["Sales","Profit"])
# ex.setRowCol(["Sales","Profit"],[])

# ex.setRowCol(["Segment","Sales"],[])
# ex.setRowCol([],["Segment","Sales"])

# ex.setRowCol(["Segment"],["Sales","Profit"])
# ex.setRowCol(["Sales","Profit"],["Segment"])

# ex.setRowCol(["Ship Mode","Segment"],["Sales"])
# ex.setRowCol(["Sales"],["Ship Mode","Segment"])

# ex.setRowCol(["Ship Mode","Segment"],["Sales","Profit"])
# ex.setRowCol(["Sales","Profit"],["Ship Mode","Segment"])

# ex.setRowCol(["Segment","Sales","Profit"],["Region"])
# ex.setRowCol(["Region"],["Segment","Sales","Profit"])

# ex.setRowCol(["Region","Segment"],["Region","Sales","Profit"])
# ex.setRowCol(["Segment","Region"],["Ship Mode",["Profit","sum"],["Sales","sum"]])
# ex.setRowCol(["Segment","Region","Sales","Profit"],[])

# ex.setRowCol(["Segment","Profit","Sales"],[])
# ex.setRowCol([],["Segment","Profit","Sales"])
# ex.setRowCol(["Ship Mode",["Profit","sum"],["Sales","sum"]],["Segment","Region"])

# ex.setRowCol(["Segment",["Sales","sum"]],["Category","Region"])
# ex.setRowCol(["Category","Region"],["Segment",["Sales","sum"]])

# ex.setRowCol(['Region'],[['Order Date', 'year'], ['Discount', 'sum']])

# ex.filter = {'Region': ['South', 'West', 'Central'], 'Ship Date year': ['2019', '2020']}
# ex.setRowCol([],['Region', 'Ship Date year'])
# ex.setRowAndColumn()

ex.filter = {'Region': ['South', 'West'], 'Ship Date year': ['2019', '2020']}
ex.setRowCol([],['Region', 'Ship Date year'])
ex.setRowAndColumn()