from tkinter import filedialog
from tkinter import *
import os
import glob
import cv2
import numpy as np
import xlsxwriter
import xlrd

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    foldername = filedialog.askdirectory()
    folder_path.set(foldername)
    state_Label.set(foldername)
    print(foldername)

    global files;
    files = os.listdir(foldername)
    print(files)


def extract_button():
    # Extract Features and store in database
    #global labels,meanValue,stdValue,medianValue,midrangeValue
    labels = []

    n = len(files);
    for f in files:
        newString = ""
        string = f
        for char in string:
            if char >= 'a' and char <= 'z':
                newString = newString + char

            else:
                break
        labels.append(newString)

    print(labels)

    meanValue = []
    stdValue = []
    medianValue = []
    midrangeValue = []

    for img in glob.glob(folder_path.get()+"\*.png"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        meanValue.append(np.mean(image))
        stdValue.append(np.std(image))
        medianValue.append(np.median(image))
        minValue = np.amin(image)
        maxValue = np.amax(image)
        midrangeValue.append((maxValue-minValue)/2)

    print(meanValue)
    print(stdValue)
    print(medianValue)
    print(midrangeValue)

    #global workbook
    workbook = xlsxwriter.Workbook('Train.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    worksheet.write(0, 2, "Std")
    worksheet.write(0, 3, "Median")
    worksheet.write(0, 4, "Midrange")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
        std = stdValue[i]
        mdn = medianValue[i]
        mdr = midrangeValue[i]

        worksheet.write(worksheetRow, worksheetCol, l)
        worksheet.write(worksheetRow, worksheetCol + 1, mn)
        worksheet.write(worksheetRow, worksheetCol + 2, std)
        worksheet.write(worksheetRow, worksheetCol + 3, mdn)
        worksheet.write(worksheetRow, worksheetCol + 4, mdr)
        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("Training Complete")

def load_button():
        #load xlsx file
        #global xlsx_path
        xlsx_path = filedialog.askopenfilename()

        print(xlsx_path)

        workbook = xlrd.open_workbook(xlsx_path)

        worksheet = workbook.sheet_by_index(0)

        global trainLabel,trainMidrange,trainMedian, trainStd, trainMean

        trainLabel = []
        trainMean = []
        trainStd = []
        trainMedian = []
        trainMidrange = []

        sheetRow = worksheet.row_values(0)
        print(sheetRow)
        sheetCol = worksheet.col_values(0)
        print(sheetCol)
        colLength = len(sheetCol)
        print(colLength)

        for i in range(1, colLength):
            trainLabel.append(worksheet.cell_value(i, 0))
            trainMean.append(worksheet.cell_value(i, 1))
            trainStd.append(worksheet.cell_value(i, 2))
            trainMedian.append(worksheet.cell_value(i, 3))
            trainMidrange.append(worksheet.cell_value(i, 4))

        print(trainLabel)
        print(trainMean)
        print(trainStd)
        print(trainMedian)
        print(trainMidrange)

        state_Label.set("Loading Done")

def image_button():
    # load image file
    #global Image path
    global image_path
    image_path = filedialog.askopenfilename()

    print(image_path)
    state_Label.set("Test Image Selected")

def recognition_button():
    #read image
    recogImage = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    recogMean = np.mean(recogImage)
    recogStd = np.std(recogImage)
    recogMedian = np.median(recogImage)
    recogMidrange = (np.amax(recogImage)-np.amin(recogImage))/2

    print(recogMean)
    print(recogStd)
    print(recogMedian)
    print(recogMidrange)

    tmn = trainMean[0]
    tstd = trainStd[0]
    tmdn = trainMedian[0]
    tmdr = trainMidrange[0]

    result = (recogMean - tmn) ** 2 + (recogMedian - tmdn) ** 2 + (recogMidrange - tmdr) ** 2

    minResult = result
    resultLabel = trainLabel[0]

    for i in range(1, len(trainMean)):
        tl = trainLabel[i]
        tmn = trainMean[i]
        tstd = trainStd[i]
        tmdn = trainMedian[i]
        tmdr = trainMidrange[i]

        result = (recogMean-tmn)**2 + (recogMedian-tmdn)**2 + (recogMidrange-tmdr)**2
        if(result<minResult):
            minResult = result
            resultLabel = tl

    state_Label.set("Recognition Done")
    result_Label.set(resultLabel)
    print(resultLabel)
    print(minResult)


#----------------------------------------------------------------------------------------------------------------

root = Tk()
folder_path = StringVar()

state_Label = StringVar()
lbl1 = Label(master=root,textvariable=state_Label)
lbl1.grid(row=1, column=1)

#lbl1 = Label(master=root,textvariable=resultLabel)
#lbl1.grid(row=1, column=1)
result_Label = StringVar()
lbl2 = Label(master=root,textvariable=result_Label)
lbl2.grid(row=3, column=1)


button1 = Button(text="Browse", command=browse_button)
button1.grid(row=5, column=1)

button2 = Button(text="Extract", command=extract_button)
button2.grid(row=5, column=3)

button3 = Button(text="Load Data", command=load_button)
button3.grid(row=5, column=5)

button4 = Button(text="Load Query Image", command=image_button)
button4.grid(row=5, column=7)

button5 = Button(text="Recognition", command=recognition_button)
button5.grid(row=5, column=9)

mainloop()