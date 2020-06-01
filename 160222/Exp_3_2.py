from tkinter import filedialog
from tkinter import *
import os
import glob
import cv2
import numpy as np
import xlsxwriter
import xlrd
from numpy import percentile



def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path,foldername
    foldername = filedialog.askdirectory()
    folder_path.set(foldername)
    state_Label.set("Folder Selected")
    print(foldername)


def extract_button():
    #All files will be selected from the folder
    files = os.listdir(foldername)
    print(files)

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
    modeValue =[]
    meanDevValue = []
    skewnessValue = []
    minValue = []
    maxValue = []
    q1Value = []
    q2Value = []
    q3Value = []
    varienceValue = []
    covarValue = []

    imageNumber = 0

    for img in glob.glob(folder_path.get() + "\*.png"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        mean = np.mean(image)
        meanValue.append(mean)
        #--------------------------------------------------------------------------
        std = np.std(image)
        stdValue.append(std)
        medianValue.append(np.median(image))
        minVal = np.amin(image)
        maxVal = np.amax(image)
        midrangeValue.append((maxVal - minVal) / 2)
        quartiles = percentile(image, [25, 50, 75])
        q1 = quartiles[0]
        q2 = quartiles[1]
        q3 = quartiles[2]
        minValue.append(minVal)
        q1Value.append(q1)
        q2Value.append(q2)
        q3Value.append(q3)
        maxValue.append(maxVal)

        varience = np.var(image)
        varienceValue.append(varience)


        height, wideth= np.shape(image)
        #print(height)
        #print(wideth)
        hashmode = []
        meanDev = 0

        for i in range(0,256):
            hashmode.append(0)

        for i in range(0, height):
            for j in range(0, wideth):
                pixValue = image[i][j]
                # print(pixValue)
                hashmode[pixValue] = hashmode[pixValue] + 1
                meanDev = meanDev + abs(image[i][j] - mean)

        getMaxPixFreq = max(hashmode)
        mode = hashmode.index(getMaxPixFreq)
        modeValue.append(mode)
        #print(mode)
        meanDev = meanDev/(height*wideth)
        skewness = (mean-mode)/std

        meanDevValue.append(meanDev)
        skewnessValue.append(skewness)

        covar = (std/mean)*100
        covarValue.append(covar)
        imageNumber = imageNumber + 1
        print(imageNumber)













        #histg = cv2.calcHist([image], [0], None, [256], [0, 256])

        #print(histg)







    print(meanValue)
    #-----------------------------------------------------------------
    print(stdValue)
    print(medianValue)
    print(midrangeValue)
    print(modeValue)
    print(meanDevValue)
    print(skewnessValue)
    print(minValue)
    print(q1Value)
    print(q2Value)
    print(q3Value)
    print(maxValue)
    print(varienceValue)
    print(covarValue)

    # global workbook
    workbook = xlsxwriter.Workbook('Train.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    #------------------------------------
    worksheet.write(0, 2, "Median")
    worksheet.write(0, 3, "Midrange")
    worksheet.write(0, 4, "Std")
    worksheet.write(0, 5, "Mode")
    worksheet.write(0, 6, "Min")
    worksheet.write(0, 7, "Q1")
    worksheet.write(0, 8, "Q2")
    worksheet.write(0, 9, "Q3")
    worksheet.write(0, 10, "Max")
    worksheet.write(0, 11, "Varience")
    worksheet.write(0, 12, "Mean Dev")
    worksheet.write(0, 13, "Skewness")
    worksheet.write(0, 14, "COV")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
        #--------------------------------------------------------
        std = stdValue[i]
        mdn = medianValue[i]
        mdr = midrangeValue[i]
        mdv = modeValue[i]
        minv = minValue[i]
        q1v = q1Value[i]
        q2v = q2Value[i]
        q3v = q3Value[i]
        maxv = maxValue[i]
        varv = varienceValue[i]
        mndev = meanDevValue[i]
        skv = skewnessValue[i]
        cov = covarValue[i]



        worksheet.write(worksheetRow, worksheetCol, l)
        worksheet.write(worksheetRow, worksheetCol + 1, mn)
        #----------------------------------------------------------------------------------
        #worksheet.write(worksheetRow, worksheetCol + 2, std)
        worksheet.write(worksheetRow, worksheetCol + 2, mdn)
        worksheet.write(worksheetRow, worksheetCol + 3, mdr)
        worksheet.write(worksheetRow, worksheetCol + 4, std)
        worksheet.write(worksheetRow, worksheetCol + 5, mdv)
        worksheet.write(worksheetRow, worksheetCol + 6, minv)
        worksheet.write(worksheetRow, worksheetCol + 7, q1v)
        worksheet.write(worksheetRow, worksheetCol + 8, q2v)
        worksheet.write(worksheetRow, worksheetCol + 9, q3v)
        worksheet.write(worksheetRow, worksheetCol + 10, maxv)
        worksheet.write(worksheetRow, worksheetCol + 11, varv)
        worksheet.write(worksheetRow, worksheetCol + 12, mndev)
        worksheet.write(worksheetRow, worksheetCol + 13, skv)
        worksheet.write(worksheetRow, worksheetCol + 14, cov)


        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("Extraction Complete")

def load_button():
    # load xlsx file
    # global xlsx_path

    global xlsx_path
    xlsx_path = filedialog.askopenfilename()

    print(xlsx_path)
    state_Label.set("Load Complete")


def image_button():
    # load image file
    #global Image path
    global image_path
    image_path = filedialog.askopenfilename()

    print(image_path)
    state_Label.set("Test Image Selected")


def recognition_button():
    # load xlsx file
    workbook = xlrd.open_workbook(xlsx_path)

    worksheet = workbook.sheet_by_index(0)

    #global trainLabel, trainMidrange, trainMedian, trainStd, trainMean

    trainLabel = []
    trainMean = []
    #---------------------------------------------
    trainStd = []
    trainMedian = []
    trainMidrange = []
    trainMode = []
    trainMin = []
    trainQ1 = []
    trainQ2 = []
    trainQ3 = []
    trainMax = []
    trainVarience = []
    trainMeanDev = []
    trainSkewness = []
    trainCOV = []

    sheetRow = worksheet.row_values(0)
    print(sheetRow)
    sheetCol = worksheet.col_values(0)
    print(sheetCol)
    colLength = len(sheetCol)
    print(colLength)

    for i in range(1, colLength):
        trainLabel.append(worksheet.cell_value(i, 0))
        trainMean.append(worksheet.cell_value(i, 1))
        #------------------------------------------------------------------
        #trainStd.append(worksheet.cell_value(i, 2))
        trainMedian.append(worksheet.cell_value(i, 2))
        trainMidrange.append(worksheet.cell_value(i, 3))
        trainStd.append(worksheet.cell_value(i, 4))
        trainMode.append(worksheet.cell_value(i, 5))
        trainMin.append(worksheet.cell_value(i, 6))
        trainQ1.append(worksheet.cell_value(i, 7))
        trainQ2.append(worksheet.cell_value(i, 8))
        trainQ3.append(worksheet.cell_value(i, 9))
        trainMax.append(worksheet.cell_value(i, 10))
        trainVarience.append(worksheet.cell_value(i, 11))
        trainMeanDev.append(worksheet.cell_value(i, 12))
        trainSkewness.append(worksheet.cell_value(i, 13))
        trainCOV.append(worksheet.cell_value(i, 14))

    print(trainLabel)
    print(trainMean)
    #-------------------------------------------------------
    print(trainStd)
    print(trainMedian)
    print(trainMidrange)
    print(trainMode)
    print(trainMin)
    print(trainQ1)
    print(trainQ2)
    print(trainQ3)
    print(trainMax)
    print(trainVarience)
    print(trainMeanDev)
    print(trainSkewness)
    print(trainCOV)

    state_Label.set("Loading Done")

    recogImage = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    recogMean = np.mean(recogImage)
    #---------------------------------------------------
    recogStd = np.std(recogImage)
    recogMedian = np.median(recogImage)
    recogMidrange = (np.amax(recogImage) - np.amin(recogImage)) / 2
    recogMin = np.amin(recogImage)
    recogquartiles = percentile(recogImage, [25, 50, 75])
    recogQ1 = recogquartiles[0]
    recogQ2 = recogquartiles[1]
    recogQ3 = recogquartiles[2]
    recogMax = np.amax(recogImage)
    recogVarience = np.var(recogImage)

    height, wideth= np.shape(recogImage)

    reHash = []
    recogMeanDev = 0

    for i in range(0,256):
        reHash.append(0)

    for i in range(0, height):
        for j in range(0, wideth):
            pixValue = recogImage[i][j]
            # print(pixValue)
            reHash[pixValue] = reHash[pixValue] + 1
            recogMeanDev = recogMeanDev + abs(recogImage[i][j] - recogMean)

    getMaxPixFreq = max(reHash)
    recogMode = reHash.index(getMaxPixFreq)
    # print(mode)
    recogMeanDev = recogMeanDev / (height * wideth)
    recogSkewness = (recogMean - recogMode) / recogStd
    recogCOV = (recogStd/recogMean)*100



    print(recogMean)
    #--------------------------------------------
    print(recogStd)
    print(recogMedian)
    print(recogMidrange)
    print(recogMode)
    print(recogMin)
    print(recogQ1)
    print(recogQ2)
    print(recogQ3)
    print(recogMax)
    print(recogVarience)
    print(recogMeanDev)
    print(recogSkewness)
    print(recogCOV)

    tmn = trainMean[0]
    tstd = trainStd[0]
    tmdn = trainMedian[0]
    tmdr = trainMidrange[0]
    tmdv = trainMode[0]
    tminv = trainMin[0]
    tq1v = trainQ1[0]
    tq2v = trainQ2[0]
    tq3v = trainQ3[0]
    tmaxv = trainMax[0]
    tvarv = trainVarience[0]
    tmndev = trainMeanDev[0]
    tskv = trainSkewness[0]
    tcov = trainCOV[0]


    #result = (recogMean - tmn) ** 2 + (recogMedian - tmdn) ** 2 + (recogMidrange - tmdr) ** 2 + (recogStd - tstd)**2
    #result = np.sqrt(result)

    avgT = (tminv + tq1v + tq2v + tq3v + tmaxv + tvarv + tmndev + tskv + tcov)/9
    varT = ((tminv**2 + tq1v**2 + tq2v**2 + tq3v**2 + tmaxv**2 + tvarv**2 + tmndev**2 + tskv**2 + tcov**2)/9)-avgT**2
    stdT = np.sqrt(varT)

    avgR = (recogMin + recogQ1 + recogQ2 + recogQ3 + recogMax + recogVarience + recogMeanDev + recogSkewness + recogCOV)/9
    varR = ((recogMin**2 + recogQ1**2 + recogQ2**2 + recogQ3**2 + recogMax**2 + recogVarience**2 + recogMeanDev**2 + recogSkewness**2 + recogCOV**2)/9)
    stdR = np.sqrt(varR)

    resultUpper = (tminv*recogMin + tq1v*recogQ1 + tq2v*recogQ2 + tq3v*recogQ3 + tmaxv*recogMax + tvarv*recogVarience + tmndev*recogMeanDev + tskv*recogSkewness + tcov*recogCOV)-9*avgR*avgT
    resultLower = 9*stdT*stdR
    result = resultUpper/resultLower
    maxResult = result
    resultLabel = trainLabel[0]
    print(result)

    for i in range(1, len(trainMean)):
        tl = trainLabel[i]
        tmn = trainMean[i]
        #-----------------------------------------
        tstd = trainStd[i]
        tmdn = trainMedian[i]
        tmdr = trainMidrange[i]
        tmdv = trainMode[i]
        tminv = trainMin[i]
        tq1v = trainQ1[i]
        tq2v = trainQ2[i]
        tq3v = trainQ3[i]
        tmaxv = trainMax[i]
        tvarv = trainVarience[i]
        tmndev = trainMeanDev[i]
        tskv = trainSkewness[i]
        tcov = trainCOV[i]

        avgT = (tminv + tq1v + tq2v + tq3v + tmaxv + tvarv + tmndev + tskv + tcov) / 9
        varT = ((tminv ** 2 + tq1v ** 2 + tq2v ** 2 + tq3v ** 2 + tmaxv ** 2 + tvarv ** 2 + tmndev ** 2 + tskv ** 2 + tcov ** 2) / 9) - avgT ** 2
        stdT = np.sqrt(varT)

        resultUpper = (tminv * recogMin + tq1v * recogQ1 + tq2v * recogQ2 + tq3v * recogQ3 + tmaxv * recogMax + tvarv * recogVarience + tmndev * recogMeanDev + tskv * recogSkewness + tcov * recogCOV) - 9 * avgR * avgT
        resultLower = 9 * stdT * stdR
        result = resultUpper / resultLower
        print(result)

        #result = (recogMean - tmn) ** 2 + (recogMedian - tmdn) ** 2 + (recogMidrange - tmdr) ** 2 + (recogStd - tstd)**2
        #result = np.sqrt(result)

        if (result >maxResult):
            maxResult = result
            resultLabel = tl

    state_Label.set("Recognition Done")
    result_Label.set(resultLabel)
    print(resultLabel)
    print(maxResult)


root = Tk()



topframe = Frame(root)
topframe.pack()

bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

folder_path = StringVar()
state_Label = StringVar()
#xlsx_path = str()


lbl1 = Label(master=root,textvariable=state_Label)
lbl1.pack()
#lbl1.grid(row=1, column=1)

#lbl1 = Label(master=root,textvariable=resultLabel)
#lbl1.grid(row=1, column=1)
result_Label = StringVar()
lbl2 = Label(master=topframe,textvariable=result_Label)
lbl2.pack()
#lbl2.grid(row=3, column=1)


button1 = Button(bottomframe, text="Browse Folder", command=browse_button)
#button1.grid(row=5, column=1)
button1.pack(side = LEFT)

button2 = Button(bottomframe, text="Extract", command=extract_button)
#button2.grid(row=5, column=3)
button2.pack(side = LEFT)

button3 = Button(bottomframe, text="Load Data File", command=load_button)
#button3.grid(row=5, column=5)
button3.pack(side = LEFT)

button4 = Button(bottomframe, text="Load Query Image", command=image_button)
#button4.grid(row=5, column=7)
button4.pack(side = LEFT)

button5 = Button(bottomframe, text="Recognition", command=recognition_button)
#button5.grid(row=5, column=9)
button5.pack(side = LEFT)

mainloop()