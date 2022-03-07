import csv
from fileinput import filename
from re import M
from typing_extensions import Self
from unittest import result
from csvManager import csvManager
import os
import sys
import unittest
import pandas as pd

Dimension =  [
        "Row ID",
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Customer ID",
        "Customer Name",
        "Segment",
        "Country/Region",
        "City",
        "State",
        "Postal Code",
        "Region",
        "Product ID",
        "Category",
        "Sub-Category",
        "Product Name"
    ]
Measurment = [
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    ]
All = [
        "Row ID",
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Customer ID",
        "Customer Name",
        "Segment",
        "Country/Region",
        "City",
        "State",
        "Postal Code",
        "Region",
        "Product ID",
        "Category",
        "Sub-Category",
        "Product Name",
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    ]
dv = pd.read_csv("C:\\Users\\Pooncharat Wongkom\\Desktop\\Test3\\TableauDataAnalysis\\SS_5lines.csv",encoding='windows-1252')
df = ["SS_5lines.csv","SS_20lines.csv"]
class TestUnitMain(unittest.TestCase) :
    
    def setUp(self):
        self.selectFile = "SS_5lines.csv"
        self.path = "C:\\Users\\Pooncharat Wongkom\\Desktop\\Test3\\TableauDataAnalysis"
        #self.df = pd.read_csv("SS_5lines.csv", encoding='windows-1252')

    def testgetOnlyDi(self) : #Get only Dimension
        getData = csvManager().getOnlyDi()
        result = len(getData)
        #print(getData)
        self.assertEqual(result, 14)

    def testIsMeasure(self) : #Check that has measure or not, if it has return true
        getData = csvManager().isMeasure(Dimension)
        #print(getData)
        self.assertTrue(getData)

    def testReadDate(self) : #Find date 
        getData = csvManager().readDate()
        result = len(getData)
        #print(getData)
        self.assertEqual(result, 2)

    def testGetHead(self) :
        getData = csvManager().getHead()
        result = len(getData)
        #print(getData)
        self.assertEqual(result, 21)
        
    def testgetsizeDimension(self) : #Check how mny value in Dimension has
        getData = csvManager().getsizeDimension("Row ID")
        result = getData
        #print(result)
        self.assertEqual(result, 5)

    def testGetMeasure(self) : 
        getData = csvManager().getMeasure()
        result = len(getData)
        #print(getData)
        self.assertEqual(result, 4)

    def testIsDimension(self) : #Check that been Dimension or Measurment
        getData = csvManager().isDimension("Row ID")
        #print(getData)
        self.assertTrue(result)

    '''def testSetRowCol(self) :
        getData = csvManager().setRowCol("Category","Profit")
        #print(getData)
        self.assertIsNone(getData)'''

    def testGetRow(self) :
        getData = csvManager().getRow()
        result = len(getData)
        #print(getData)
        self.assertEqual(result,0)

    def testGetCol(self) :
        getData = csvManager().getCol()
        result = len(getData)
        #print(getData)
        self.assertEqual(result,0)

    def testUnionFile(self) :
        getData = csvManager().unionFile(df)
        result = len(getData)
        #print(getData)
        self.assertEqual(result,5)

    def testFilterMes(self) :
        getData = csvManager().filterMes(Measurment)
        result = len(getData)
        #print(getData)
        self.assertEqual(result,4)

    def testGetDate(self) :
        getData = csvManager().getDate()
        result = len(getData)
        self.assertEqual(result, 2)
    
    

if __name__ == "__main__":
    #TestUnitMain.TestGetMeasure(Dimension)
    
    unittest.main()
#print(TestUnitMain().TestGetMeasure())