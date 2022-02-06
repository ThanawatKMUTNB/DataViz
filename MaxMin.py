from email import header
from operator import mod
import os
import pathlib
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QLineSeries
import numpy as np
import pandas as pd
import csvManager
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart
from PyQt5.QtGui import QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

from itertools import chain
from re import S
import numpy as np
import pandas as pd
import xlrd
import openpyxl


def findMax():
    df = pd.read_excel('Superstore.xlsx', engine = "openpyxl")
    max_value = df["Sales"].max()
    #df = pd.read_excel(, index_col=0)
    return max_value
print(findMax())
def findMin():
    df = pd.read_excel('Superstore.xlsx', engine = "openpyxl")
    min_value = df["Sales"].min()
    #df = pd.read_excel(, index_col=0)
    return min_value
print(findMin())
def findMean():
    df = pd.read_excel('Superstore.xlsx', engine = "openpyxl")
    mean_value = df["Sales"].mean()
    #df = pd.read_excel(, index_col=0)
    return mean_value
print(findMean())
def findSum():
    df = pd.read_excel('Superstore.xlsx', engine = "openpyxl")
    sum_value = df["Sales"].sum()
    #df = pd.read_excel(, index_col=0)
    return sum_value
print(findSum())