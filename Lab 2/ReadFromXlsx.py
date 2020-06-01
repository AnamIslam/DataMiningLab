import os
import glob
import cv2
import numpy as np
import xlsxwriter
import xlrd

workbook = xlrd.open_workbook("Train.xlsx")

# print number of sheets
nsheets = workbook.nsheets
print(nsheets)

# print sheet names
namesSheets = workbook.sheet_names()
print(namesSheets)

worksheet = workbook.sheet_by_index(0)
print(worksheet)
fullData= []
trainLabel = []
trainMean = []
trainStd = []
trainMedian = []
trainMidrange = []


sheetRow = worksheet.row_values(0)
print(sheetRow)
sheetCol =  worksheet.col_values(0)
print(sheetCol)
colLength = len(sheetCol)
print(colLength)

#for index in range(1, worksheet.nrows):
    #thisrow = worksheet.row_values(index)
    #fullData.append(thisrow)

#print(fullData)


for i in range(1,colLength):
    trainLabel.append(worksheet.cell_value(i, 0))
    trainMean.append(worksheet.cell_value(i,1))
    trainStd.append(worksheet.cell_value(i, 2))
    trainMedian.append(worksheet.cell_value(i, 3))
    trainMidrange.append(worksheet.cell_value(i, 4))

print(trainLabel)
print(trainMean)
print(trainStd)
print(trainMedian)
print(trainMidrange)
