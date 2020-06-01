import os
import glob
import cv2
import numpy as np
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

testworkbook = xlsxwriter.Workbook('TestNew.xlsx')

testworksheet = testworkbook.add_worksheet()

testworksheet.write(0,0,"Label")
testworksheet.write(0,1,"Mean")
testworksheet.write(0,2,"Std")


testworksheetRow = 1
testworksheetCol = 0


for testi in range(len(testlabels)):
    testl = testlabels[testi]
    testmn = testmeanValue[testi]
    teststd = teststdValue[testi]

    testworksheet.write(testworksheetRow, testworksheetCol, testl)
    testworksheet.write(testworksheetRow, testworksheetCol + 1, testmn)
    testworksheet.write(testworksheetRow, testworksheetCol + 2, teststd)
    testi += 1
    testworksheetRow += 1


testworkbook.close()

cv2.waitKey(0)
cv2.destroyAllWindows()
