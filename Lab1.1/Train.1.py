import os
import glob
import cv2
import numpy as np
import xlsxwriter

files = os.listdir("Train and test ETH 80 dataset/TrainETH80data2952")

labels = []

n = len(files);
for f in files:
    newString = ""
    string = f
    for char in string:
        if char >= 'a' and char <= 'z':
            newString = newString+char

        else:
            break
    labels.append(newString)


print(files)
print(labels)

meanValue = []
stdValue = []

for img in glob.glob("Train and test ETH 80 dataset/TrainETH80data2952/*.png"):
    # Load an color image in grayscale
    image = cv2.imread(img, 0)
    meanValue.append(np.mean(image))
    stdValue.append(np.std(image))

print(meanValue)
print(stdValue)

workbook = xlsxwriter.Workbook('TrainNew.xlsx')

worksheet = workbook.add_worksheet()

worksheet.write(0,0,"Label")
worksheet.write(0,1,"Mean")
worksheet.write(0,2,"Std")

worksheetRow = 1
worksheetCol = 0

for i in range(len(labels)):

    l=labels[i]
    mn = meanValue[i]
    std = stdValue[i]

    worksheet.write(worksheetRow,worksheetCol,l)
    worksheet.write(worksheetRow, worksheetCol+1, mn)
    worksheet.write(worksheetRow, worksheetCol+2, std)
    i+=1
    worksheetRow+=1




workbook.close()


cv2.waitKey(0)
cv2.destroyAllWindows()