import pandas as pd
from csvManager import csvManager

ex = csvManager()
ex.Measure = {'Sales':"sum",'Quantity':"sum",'Discount':"sum",'Profit':"sum"}        
ex.df = pd.read_csv("Superstore.csv", encoding='windows-1252')
ex.getHead()
# ex.readMeasure()
# ex.setRowAndColumn(["Segment"],[])
# ex.setRowAndColumn([],["Segment"])

# ex.setRowAndColumn([],["Sales"])
# ex.setRowAndColumn(["Sales"],[])

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
# ex.filter = {'Discount': [0.0, 0.8], 'Profit': [50, 219.0], 'Region': ['East','South']}
# ex.setRowAndColumn(["Ship Mode",["Profit","sum"],["Sales","sum"]],["Segment","Region"])

# ex.setRowAndColumn(["Segment",["Sales","sum"]],["Category","Region"])
# ex.setRowAndColumn(["Category","Region"],["Segment",["Sales","sum"]])