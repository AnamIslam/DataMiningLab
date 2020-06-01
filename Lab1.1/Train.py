import glob
import cv2
import numpy as np
import os
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

workbook = xlsxwriter.Workbook('Train.xlsx')

worksheet = workbook.add_worksheet()

worksheetRow = 0
worksheetCol = 0

for l in labels:
    worksheet.write(worksheetRow,worksheetCol,l)
    worksheetRow+=1


worksheetRow = 0
worksheetCol = 1

for mn in meanValue:
    worksheet.write(worksheetRow,worksheetCol,mn)
    worksheetRow+=1

worksheetRow = 0
worksheetCol = 2

for std in stdValue:
    worksheet.write(worksheetRow,worksheetCol,std)
    worksheetRow+=1

workbook.close()


cv2.waitKey(0)
cv2.destroyAllWindows()