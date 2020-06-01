import glob
import cv2
import numpy as np
import os
import xlsxwriter

testfiles = os.listdir("Train and test ETH 80 dataset/TestETH80data328")

testlabels = []

testn = len(testfiles);
for testf in testfiles:
    testnewString = ""
    teststring = testf
    for testchar in teststring:
        if testchar >= 'a' and testchar <= 'z':
            testnewString = testnewString+testchar

        else:
            break
    testlabels.append(testnewString)


print(testfiles)
print(testlabels)

testmeanValue = []
teststdValue = []

for testimg in glob.glob("Train and test ETH 80 dataset/TestETH80data328/*.png"):
    # Load an color image in grayscale
    testimage = cv2.imread(testimg, 0)
    testmeanValue.append(np.mean(testimage))
    teststdValue.append(np.std(testimage))

print(testmeanValue)
print(teststdValue)

testworkbook = xlsxwriter.Workbook('Test.xlsx')

testworksheet = testworkbook.add_worksheet()

testworksheetRow = 0
testworksheetCol = 0

for testl in testlabels:
    testworksheet.write(testworksheetRow,testworksheetCol,testl)
    testworksheetRow+=1


testworksheetRow = 0
testworksheetCol = 1

for testmn in testmeanValue:
    testworksheet.write(testworksheetRow,testworksheetCol,testmn)
    testworksheetRow+=1

testworksheetRow = 0
testworksheetCol = 2

for teststd in teststdValue:
    testworksheet.write(testworksheetRow,testworksheetCol,teststd)
    testworksheetRow+=1

testworkbook.close()

cv2.waitKey(0)
cv2.destroyAllWindows()