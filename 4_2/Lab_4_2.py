from tkinter import filedialog
from tkinter import *
import os
import glob
import cv2
import numpy as np
import xlsxwriter
import xlrd
from numpy import percentile
from skimage import feature
import pandas as pd
from sklearn.tree import DecisionTreeClassifier




def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path,foldername
    foldername = filedialog.askdirectory()
    folder_path.set(foldername)
    state_Label.set("Folder Selected")
    print(foldername)

def extract_CT_button():
    global flag
    flag = 1
    #All files will be selected from the folder
    files = os.listdir(foldername)
    print(files)

    labels = []

    n = len(files);
    for f in files:
        newString = f.split('.',2)[0]
        labels.append(newString)

    print(labels)

    meanValue = []
    medianValue = []
    modeValue = []
    midrangeValue = []

    imageNumber = 0

    for img in glob.glob(folder_path.get() + "\*.png"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        mean = np.mean(image)
        meanValue.append(mean)
        #std = np.std(image)
        medianValue.append(np.median(image))
        minVal = np.amin(image)
        maxVal = np.amax(image)
        midrangeValue.append((maxVal - minVal) / 2)

        height, wideth= np.shape(image)
        hashmode = []

        for i in range(0,256):
            hashmode.append(0)

        for i in range(0, height):
            for j in range(0, wideth):
                pixValue = image[i][j]
                hashmode[pixValue] = hashmode[pixValue] + 1

        getMaxPixFreq = max(hashmode)
        mode = hashmode.index(getMaxPixFreq)
        modeValue.append(mode)

        imageNumber = imageNumber + 1
        print(imageNumber)

    print(meanValue)
    print(medianValue)
    print(modeValue)

    workbook = xlsxwriter.Workbook('Train_CT.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    worksheet.write(0, 2, "Median")
    worksheet.write(0, 3, "Mode")
    worksheet.write(0, 4, "Midrange")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
        mdn = medianValue[i]
        mdr = midrangeValue[i]
        mdv = modeValue[i]



        worksheet.write(worksheetRow, worksheetCol, l)
        worksheet.write(worksheetRow, worksheetCol + 1, mn)
        worksheet.write(worksheetRow, worksheetCol + 2, mdn)
        worksheet.write(worksheetRow, worksheetCol + 3, mdv)
        worksheet.write(worksheetRow, worksheetCol + 4, mdr)

        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("CT Extraction Complete")

def extract_DD_button():
    global flag
    flag = 2
    #All files will be selected from the folder
    files = os.listdir(foldername)
    print(files)

    labels = []

    n = len(files);
    for f in files:
        newString = f.split(".",2)[0]
        labels.append(newString)

    print(labels)

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
        std = np.std(image)
        minVal = np.amin(image)
        maxVal = np.amax(image)
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
        meanDev = meanDev/(height*wideth)
        skewness = (mean-mode)/std

        meanDevValue.append(meanDev)
        skewnessValue.append(skewness)

        covar = (std/mean)*100
        covarValue.append(covar)
        imageNumber = imageNumber + 1
        print(imageNumber)

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
    workbook = xlsxwriter.Workbook('Train_DD.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Min")
    worksheet.write(0, 2, "Q1")
    worksheet.write(0, 3, "Q2")
    worksheet.write(0, 4, "Q3")
    worksheet.write(0, 5, "Max")
    worksheet.write(0, 6, "Varience")
    worksheet.write(0, 7, "Mean Dev")
    worksheet.write(0, 8, "Skewness")
    worksheet.write(0, 9, "COV")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
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
        worksheet.write(worksheetRow, worksheetCol + 1, minv)
        worksheet.write(worksheetRow, worksheetCol + 2, q1v)
        worksheet.write(worksheetRow, worksheetCol + 3, q2v)
        worksheet.write(worksheetRow, worksheetCol + 4, q3v)
        worksheet.write(worksheetRow, worksheetCol + 5, maxv)
        worksheet.write(worksheetRow, worksheetCol + 6, varv)
        worksheet.write(worksheetRow, worksheetCol + 7, mndev)
        worksheet.write(worksheetRow, worksheetCol + 8, skv)
        worksheet.write(worksheetRow, worksheetCol + 9, cov)


        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("DD Extraction Complete")

def extract_CT_DD_button():
    #All files will be selected from the folder

    global flag
    flag = 3
    files = os.listdir(foldername)
    print(files)

    labels = []

    n = len(files);
    for f in files:
        newString = f.split(".",2)[0]
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

    print(meanValue)
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
    workbook = xlsxwriter.Workbook('Train_CT_DD.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    worksheet.write(0, 2, "Median")
    worksheet.write(0, 3, "Midrange")
    worksheet.write(0, 4, "Mode")
    worksheet.write(0, 5, "Min")
    worksheet.write(0, 6, "Q1")
    worksheet.write(0, 7, "Q2")
    worksheet.write(0, 8, "Q3")
    worksheet.write(0, 9, "Max")
    worksheet.write(0, 10, "Varience")
    worksheet.write(0, 11, "Mean Dev")
    worksheet.write(0, 12, "Skewness")
    worksheet.write(0, 13, "COV")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
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
        worksheet.write(worksheetRow, worksheetCol + 2, mdn)
        worksheet.write(worksheetRow, worksheetCol + 3, mdr)
        worksheet.write(worksheetRow, worksheetCol + 4, mdv)
        worksheet.write(worksheetRow, worksheetCol + 5, minv)
        worksheet.write(worksheetRow, worksheetCol + 6, q1v)
        worksheet.write(worksheetRow, worksheetCol + 7, q2v)
        worksheet.write(worksheetRow, worksheetCol + 8, q3v)
        worksheet.write(worksheetRow, worksheetCol + 9, maxv)
        worksheet.write(worksheetRow, worksheetCol + 10, varv)
        worksheet.write(worksheetRow, worksheetCol + 11, mndev)
        worksheet.write(worksheetRow, worksheetCol + 12, skv)
        worksheet.write(worksheetRow, worksheetCol + 13, cov)


        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("CT and DD Extraction Complete")

def extract_LBP_button():
    global flag
    flag = 1
    # All files will be selected from the folder
    files = os.listdir(foldername)
    print(files)

    labels = []

    n = len(files);
    for f in files:
        newString = f.split('.', 2)[0]
        labels.append(newString)

    print(labels)
    v0 = []
    v1 = []
    v2 = []
    v3 = []
    v4 = []
    v5 = []
    v6 = []
    v7 = []
    v8 = []
    v9 = []


    for img in glob.glob(folder_path.get() + "\*.png"):
        image = cv2.imread(img, 0)
        features = feature.local_binary_pattern(image, 8, 1, method="default")
        (hist, _) = np.histogram(features.ravel(), bins=np.arange(0,8+3), range=(0, 8+2))

        hist = hist.astype("float")
        hist = hist/(hist.sum()+1e-7)
        print(hist)
        #LBPfeatures.append(features)
        v0.append(hist[0])
        v1.append(hist[1])
        v2.append(hist[2])
        v3.append(hist[3])
        v4.append(hist[4])
        v5.append(hist[5])
        v6.append(hist[6])
        v7.append(hist[7])
        v8.append(hist[8])
        v9.append(hist[9])

    print(v0)
    print(v1)
    print(v2)
    print(v3)
    print(v4)
    print(v5)
    print(v6)
    print(v7)
    print(v8)
    print(v9)

    # global workbook
    workbook = xlsxwriter.Workbook('Train_LPB.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "v0")
    worksheet.write(0, 2, "v1")
    worksheet.write(0, 3, "v2")
    worksheet.write(0, 4, "v3")
    worksheet.write(0, 5, "v4")
    worksheet.write(0, 6, "v5")
    worksheet.write(0, 7, "v6")
    worksheet.write(0, 8, "v7")
    worksheet.write(0, 9, "v8")
    worksheet.write(0, 10, "v9")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        worksheet.write(worksheetRow, worksheetCol, labels[i])
        worksheet.write(worksheetRow, worksheetCol+1, v0[i])
        worksheet.write(worksheetRow, worksheetCol + 2, v1[i])
        worksheet.write(worksheetRow, worksheetCol + 3, v2[i])
        worksheet.write(worksheetRow, worksheetCol + 4, v3[i])
        worksheet.write(worksheetRow, worksheetCol + 5, v4[i])
        worksheet.write(worksheetRow, worksheetCol + 6, v5[i])
        worksheet.write(worksheetRow, worksheetCol + 7, v6[i])
        worksheet.write(worksheetRow, worksheetCol + 8, v7[i])
        worksheet.write(worksheetRow, worksheetCol + 9, v8[i])
        worksheet.write(worksheetRow, worksheetCol + 10, v9[i])
        worksheetRow += 1
    workbook.close()
    state_Label.set("LDP Extraction Complete")


def load_button():
    # load xlsx file
    # global xlsx_path

    global xlsx_path
    xlsx_path = filedialog.askopenfilename()

    print(xlsx_path)
    state_Label.set("Load Complete")

def image_button():
    # Allow user to select a directory and store it in global var
    # called imfolder_path

    global imfolder_path, imfoldername
    imfoldername = filedialog.askdirectory()
    imfolder_path.set(imfoldername)
    state_Label.set("Test Folder Selected")
    print(imfoldername)

def extract_CT_QM_button():
    # All files will be selected from the folder
    files = os.listdir(imfoldername)
    print(files)

    labels = []

    n = len(files)
    print(n)
    for f in files:
        newString = f.split('.', 2)[0]
        labels.append(newString)

    print(labels)

    meanValue = []
    medianValue = []
    modeValue = []
    midrangeValue = []

    imageNumber = 0

    for img in glob.glob(imfolder_path.get() + "\*.JPG"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        print(image)
        mean = np.mean(image)
        meanValue.append(mean)
        medianValue.append(np.median(image))
        minVal = np.amin(image)
        maxVal = np.amax(image)
        midrangeValue.append((maxVal - minVal) / 2)
        height, wideth = np.shape(image)
        hashmode = []
        meanDev = 0

        for i in range(0, 256):
            hashmode.append(0)

        for i in range(0, height):
            for j in range(0, wideth):
                pixValue = image[i][j]
                hashmode[pixValue] = hashmode[pixValue] + 1

        getMaxPixFreq = max(hashmode)
        mode = hashmode.index(getMaxPixFreq)
        modeValue.append(mode)
        imageNumber = imageNumber + 1
        print(imageNumber)


    print(meanValue)
    print(medianValue)
    print(modeValue)
    print(midrangeValue)

    # global workbook
    workbook = xlsxwriter.Workbook('Test_CT.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    worksheet.write(0, 2, "Median")
    worksheet.write(0, 3, "Mode")
    worksheet.write(0, 4, "Midrange")

    worksheetRow = 1
    worksheetCol = 0

    print(len(labels))

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
        mdn = medianValue[i]
        mdv = modeValue[i]
        mdr = midrangeValue[i]

        worksheet.write(worksheetRow, worksheetCol, l)
        worksheet.write(worksheetRow, worksheetCol + 1, mn)
        worksheet.write(worksheetRow, worksheetCol + 2, mdn)
        worksheet.write(worksheetRow, worksheetCol + 3, mdv)
        worksheet.write(worksheetRow, worksheetCol + 4, mdr)

        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("Test CT Extraction Complete")

def extract_DD_QM_button():
    # All files will be selected from the folder
    files = os.listdir(imfoldername)
    print(files)

    labels = []

    n = len(files)
    print(n)
    for f in files:
        newString = f.split('.', 2)[0]
        labels.append(newString)

    print(labels)

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

    for img in glob.glob(imfolder_path.get() + "\*.JPG"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        mean = np.mean(image)
        std = np.std(image)
        minVal = np.amin(image)
        maxVal = np.amax(image)
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

        height, wideth = np.shape(image)
        hashmode = []
        meanDev = 0

        for i in range(0, 256):
            hashmode.append(0)

        for i in range(0, height):
            for j in range(0, wideth):
                pixValue = image[i][j]
                hashmode[pixValue] = hashmode[pixValue] + 1
                meanDev = meanDev + abs(image[i][j] - mean)

        getMaxPixFreq = max(hashmode)
        mode = hashmode.index(getMaxPixFreq)
        meanDev = meanDev / (height * wideth)
        skewness = (mean - mode) / std

        meanDevValue.append(meanDev)
        skewnessValue.append(skewness)

        covar = (std / mean) * 100
        covarValue.append(covar)
        imageNumber = imageNumber + 1
        print(imageNumber)

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
    workbook = xlsxwriter.Workbook('Test_DD.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Min")
    worksheet.write(0, 2, "Q1")
    worksheet.write(0, 3, "Q2")
    worksheet.write(0, 4, "Q3")
    worksheet.write(0, 5, "Max")
    worksheet.write(0, 6, "Varience")
    worksheet.write(0, 7, "Mean Dev")
    worksheet.write(0, 8, "Skewness")
    worksheet.write(0, 9, "COV")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
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
        worksheet.write(worksheetRow, worksheetCol + 1, minv)
        worksheet.write(worksheetRow, worksheetCol + 2, q1v)
        worksheet.write(worksheetRow, worksheetCol + 3, q2v)
        worksheet.write(worksheetRow, worksheetCol + 4, q3v)
        worksheet.write(worksheetRow, worksheetCol + 5, maxv)
        worksheet.write(worksheetRow, worksheetCol + 6, varv)
        worksheet.write(worksheetRow, worksheetCol + 7, mndev)
        worksheet.write(worksheetRow, worksheetCol + 8, skv)
        worksheet.write(worksheetRow, worksheetCol + 9, cov)

        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("Extraction Complete")

def extract_CT_DD_QM_button():
    # All files will be selected from the folder
    files = os.listdir(imfoldername)
    print(files)

    labels = []

    n = len(files)
    print(n)
    for f in files:
        newString = f.split('.', 2)[0]
        labels.append(newString)

    print(labels)


    meanValue = []
    #stdValue = []
    medianValue = []
    midrangeValue = []
    modeValue = []
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

    for img in glob.glob(imfolder_path.get() + "\*.JPG"):
        # Load an color image in grayscale
        image = cv2.imread(img, 0)
        mean = np.mean(image)
        meanValue.append(mean)
        std = np.std(image)
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

        height, wideth = np.shape(image)
        hashmode = []
        meanDev = 0

        for i in range(0, 256):
            hashmode.append(0)

        for i in range(0, height):
            for j in range(0, wideth):
                pixValue = image[i][j]
                hashmode[pixValue] = hashmode[pixValue] + 1
                meanDev = meanDev + abs(image[i][j] - mean)

        getMaxPixFreq = max(hashmode)
        mode = hashmode.index(getMaxPixFreq)
        modeValue.append(mode)
        meanDev = meanDev / (height * wideth)
        skewness = (mean - mode) / std

        meanDevValue.append(meanDev)
        skewnessValue.append(skewness)

        covar = (std / mean) * 100
        covarValue.append(covar)
        imageNumber = imageNumber + 1
        print(imageNumber)

    # global workbook
    workbook = xlsxwriter.Workbook('Test_CT_DD.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "Mean")
    worksheet.write(0, 2, "Median")
    worksheet.write(0, 3, "Midrange")
    worksheet.write(0, 4, "Mode")
    worksheet.write(0, 5, "Min")
    worksheet.write(0, 6, "Q1")
    worksheet.write(0, 7, "Q2")
    worksheet.write(0, 8, "Q3")
    worksheet.write(0, 9, "Max")
    worksheet.write(0, 10, "Varience")
    worksheet.write(0, 11, "Mean Dev")
    worksheet.write(0, 12, "Skewness")
    worksheet.write(0, 13, "COV")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        l = labels[i]
        mn = meanValue[i]
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
        worksheet.write(worksheetRow, worksheetCol + 2, mdn)
        worksheet.write(worksheetRow, worksheetCol + 3, mdr)
        worksheet.write(worksheetRow, worksheetCol + 4, mdv)
        worksheet.write(worksheetRow, worksheetCol + 5, minv)
        worksheet.write(worksheetRow, worksheetCol + 6, q1v)
        worksheet.write(worksheetRow, worksheetCol + 7, q2v)
        worksheet.write(worksheetRow, worksheetCol + 8, q3v)
        worksheet.write(worksheetRow, worksheetCol + 9, maxv)
        worksheet.write(worksheetRow, worksheetCol + 10, varv)
        worksheet.write(worksheetRow, worksheetCol + 11, mndev)
        worksheet.write(worksheetRow, worksheetCol + 12, skv)
        worksheet.write(worksheetRow, worksheetCol + 13, cov)

        i += 1
        worksheetRow += 1

    workbook.close()
    state_Label.set("Extraction Complete")


def extract_LBP_QM_button():
    global flag
    flag = 1
    # All files will be selected from the folder
    files = os.listdir(imfoldername)
    print(files)

    labels = []

    n = len(files);
    for f in files:
        newString = f.split('.', 2)[0]
        labels.append(newString)

    print(labels)
    v0 = []
    v1 = []
    v2 = []
    v3 = []
    v4 = []
    v5 = []
    v6 = []
    v7 = []
    v8 = []
    v9 = []

    for img in glob.glob(imfolder_path.get() + "\*.JPG"):
        image = cv2.imread(img, 0)
        features = feature.local_binary_pattern(image, 8, 1, method="default")
        (hist, _) = np.histogram(features.ravel(), bins=np.arange(0, 8 + 3), range=(0, 8 + 2))

        hist = hist.astype("float")
        hist = hist / (hist.sum() + 1e-7)
        print(hist)
        # LBPfeatures.append(features)
        v0.append(hist[0])
        v1.append(hist[1])
        v2.append(hist[2])
        v3.append(hist[3])
        v4.append(hist[4])
        v5.append(hist[5])
        v6.append(hist[6])
        v7.append(hist[7])
        v8.append(hist[8])
        v9.append(hist[9])

    print(v0)
    print(v1)
    print(v2)
    print(v3)
    print(v4)
    print(v5)
    print(v6)
    print(v7)
    print(v8)
    print(v9)

    # global workbook
    workbook = xlsxwriter.Workbook('Test_LPB.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Label")
    worksheet.write(0, 1, "v0")
    worksheet.write(0, 2, "v1")
    worksheet.write(0, 3, "v2")
    worksheet.write(0, 4, "v3")
    worksheet.write(0, 5, "v4")
    worksheet.write(0, 6, "v5")
    worksheet.write(0, 7, "v6")
    worksheet.write(0, 8, "v7")
    worksheet.write(0, 9, "v8")
    worksheet.write(0, 10, "v9")

    worksheetRow = 1
    worksheetCol = 0

    for i in range(len(labels)):
        worksheet.write(worksheetRow, worksheetCol, labels[i])
        worksheet.write(worksheetRow, worksheetCol + 1, v0[i])
        worksheet.write(worksheetRow, worksheetCol + 2, v1[i])
        worksheet.write(worksheetRow, worksheetCol + 3, v2[i])
        worksheet.write(worksheetRow, worksheetCol + 4, v3[i])
        worksheet.write(worksheetRow, worksheetCol + 5, v4[i])
        worksheet.write(worksheetRow, worksheetCol + 6, v5[i])
        worksheet.write(worksheetRow, worksheetCol + 7, v6[i])
        worksheet.write(worksheetRow, worksheetCol + 8, v7[i])
        worksheet.write(worksheetRow, worksheetCol + 9, v8[i])
        worksheet.write(worksheetRow, worksheetCol + 10, v9[i])
        worksheetRow += 1
    workbook.close()
    state_Label.set("LDP Extraction Complete")


def load_Test_button():
    global xlsx_path2
    xlsx_path2 = filedialog.askopenfilename()

    print(xlsx_path2)
    state_Label.set("Load Complete")


def recognition_ED_button():
    # load xlsx file
    workbook = xlrd.open_workbook(xlsx_path)

    worksheet = workbook.sheet_by_index(0)
    sheetRow = worksheet.row_values(0)
    sheetCol = worksheet.col_values(0)
    print(sheetRow)
    print(sheetCol)
    rtr = len(sheetCol)-1
    ctr = len(sheetRow)

    workbook2 = xlrd.open_workbook(xlsx_path2)

    worksheet2 = workbook2.sheet_by_index(0)
    sheetRow2 = worksheet2.row_values(0)
    sheetCol2 = worksheet2.col_values(0)
    rts = len(sheetCol2)-1
    cts = len(sheetRow2)

    trainData = []

    for i in range(0, rtr):
        trainData.append([int(0) for j in range(0,ctr)])

    testData = []
    for i in range(0, rts):
        testData.append([int(0) for j in range(0,cts)])

    for i in range(0,rtr):
        for j in range(0,ctr):
            trainData[i][j] = worksheet.cell_value(i+1, j)

    print(trainData)

    for i in range(0,rts):
        for j in range(0,cts):
            testData[i][j] = worksheet2.cell_value(i+1, j)

    print(testData)

    workbooknew = xlsxwriter.Workbook('RecognitionEucledian.xlsx')
    print("OK")
    worksheetnew = workbooknew.add_worksheet()
    worksheetnew.write(0, 0, "TestObject")
    worksheetnew.write(0, 1, "Recognition")


    for i in range(0,rts):
        print(i)
        for k in range(0,rtr):
            ed = 0
            if(k==0):
                for j in range(1,cts):
                    ed = ed+ (trainData[k][j]-testData[1][j])**2
                ed = np.sqrt(ed)
                print(ed)
                mindis = ed
                recog = trainData[k][0]

            else:
                for j in range(1, cts):
                    #print("print hoy na ken?")
                    ed = ed + (trainData[k][j] - testData[i][j]) ** 2
                ed = np.sqrt(ed)
                print(ed)
                if(ed<mindis):
                    recog = trainData[k][0]


        worksheetnew.write(i + 1, 0, testData[i][0])
        worksheetnew.write(i + 1, 1, recog)
    workbooknew.close()
    state_Label.set("Recognition Done")

def recognition_CR_button():
    # load xlsx file
    workbook = xlrd.open_workbook(xlsx_path)

    worksheet = workbook.sheet_by_index(0)
    sheetRow = worksheet.row_values(0)
    sheetCol = worksheet.col_values(0)
    print(sheetRow)
    print(sheetCol)
    rtr = len(sheetCol) - 1
    ctr = len(sheetRow)

    workbook2 = xlrd.open_workbook(xlsx_path2)

    worksheet2 = workbook2.sheet_by_index(0)
    sheetRow2 = worksheet2.row_values(0)
    sheetCol2 = worksheet2.col_values(0)
    rts = len(sheetCol2) - 1
    cts = len(sheetRow2)

    trainData = []

    for i in range(0, rtr):
        trainData.append([int(0) for j in range(0, ctr)])

    testData = []
    for i in range(0, rts):
        testData.append([int(0) for j in range(0, cts)])

    for i in range(0, rtr):
        for j in range(0, ctr):
            trainData[i][j] = worksheet.cell_value(i + 1, j)

    print(trainData)

    for i in range(0, rts):
        for j in range(0, cts):
            testData[i][j] = worksheet2.cell_value(i + 1, j)

    print(testData)

    workbooknew = xlsxwriter.Workbook('RecognitionCorelation.xlsx')
    print("OK")
    worksheetnew = workbooknew.add_worksheet()
    worksheetnew.write(0, 0, "TestObject")
    worksheetnew.write(0, 1, "Recognition")

    for i in range(0, rts):
        print(i)
        avgTs = 0
        varTs = 0
        for j in range(1,cts):
            avgTs = avgTs+testData[i][j]
            varTs = varTs+testData[i][j]**2

        avgTs = avgTs/rts
        varTs = (varTs/rts)-avgTs**2
        stdTs = np.sqrt(varTs)

        for k in range(0, rtr):
            avgTr = 0
            varTr = 0
            rup = 0
            if (k == 0):
                for j in range(1, cts):
                    avgTr = avgTr + trainData[k][j]
                    varTr = varTr + trainData[k][j] ** 2
                    rup = rup + testData[i][j]*trainData[k][j]

                avgTr = avgTr / rtr
                varTr = (varTr / rtr) - avgTr ** 2
                stdTr = np.sqrt(varTr)
                rup = rup - cts*avgTs*avgTr
                result = rup/(cts*stdTr*stdTs)
                max = result
                recog = trainData[k][0]
                print(result)

            else:
                for j in range(1, cts):
                    avgTr = avgTr + trainData[k][j]
                    varTr = varTr + trainData[k][j] ** 2
                    rup = rup + testData[i][j] * trainData[k][j]

                avgTr = avgTr / rtr
                varTr = (varTr / rtr) - avgTr ** 2
                stdTr = np.sqrt(varTr)
                rup = rup - cts * avgTs * avgTr
                result = rup / (cts * stdTr * stdTs)
                print(result)

            if (result> max):
                    recog = trainData[k][0]


        print("-----------------")



        worksheetnew.write(i + 1, 0, testData[i][0])
        worksheetnew.write(i + 1, 1, recog)
    workbooknew.close()
    state_Label.set("Recognition Done")

def recognition_DT_button():
    # load xlsx file
    workbook = xlrd.open_workbook(xlsx_path)

    worksheet = workbook.sheet_by_index(0)
    sheetRow = worksheet.row_values(0)
    sheetCol = worksheet.col_values(0)
    print(sheetRow)
    print(sheetCol)
    rtr = len(sheetCol) - 1
    ctr = len(sheetRow)

    workbook2 = xlrd.open_workbook(xlsx_path2)

    worksheet2 = workbook2.sheet_by_index(0)
    sheetRow2 = worksheet2.row_values(0)
    sheetCol2 = worksheet2.col_values(0)
    rts = len(sheetCol2) - 1
    cts = len(sheetRow2)

    feature_cols = []

    for i in range(1, ctr):
        feature_cols.append(sheetRow[i])

    print(feature_cols)
    target = sheetRow[0]

    trainData = []

    for i in range(0, rtr):
        trainData.append([int(0) for j in range(0, ctr)])

    testData = []
    for i in range(0, rts):
        testData.append([int(0) for j in range(0, cts)])

    for i in range(0, rtr):
        for j in range(0, ctr):
            trainData[i][j] = worksheet.cell_value(i + 1, j)

    print(trainData)

    for i in range(0, rts):
        for j in range(0, cts):
            testData[i][j] = worksheet2.cell_value(i + 1, j)

    print(testData)


    trainLbl = []
    for i in range(0,rtr):
        trainLbl.append(trainData[i][0])
    print(trainLbl)

    testLbl = []
    for i in range(0,rts):
        testLbl.append(testData[i][0])

    print(testLbl)

    trainSet = []
    for i in range(0, rtr):
        trainSet.append([int(0) for j in range(0, ctr-1)])

    testSet = []
    for i in range(0, rts):
        testSet.append([int(0) for j in range(0, ctr - 1)])

    for i in range(0,rtr):
        for j in range(0,ctr-1):
            trainSet[i][j] = trainData[i][j+1]
    print(trainSet)

    for i in range(0,rts):
        for j in range(0,ctr-1):
            testSet[i][j] = testData[i][j+1]

    print(testSet)
    print(trainLbl)
    print(testLbl)

    x = trainSet
    y = trainLbl
    z = testSet

    clf = DecisionTreeClassifier()
    clf = clf.fit(x, y)
    y_pred = clf.predict(z)
    print(y_pred)

    workbooknew = xlsxwriter.Workbook('RecognitionDT.xlsx')
    print("OK")
    worksheetnew = workbooknew.add_worksheet()
    worksheetnew.write(0, 0, "TestObject")
    worksheetnew.write(0, 1, "Recognition")
    for i in range(0,rts):
        worksheetnew.write(i + 1, 0, testLbl[i])
        worksheetnew.write(i + 1, 1, y_pred[i])

    workbooknew.close()
    state_Label.set("Recognition Done")







root = Tk()

topframe = Frame(root)
topframe.pack()

bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

folder_path = StringVar()
state_Label = StringVar()
imfolder_path = StringVar()
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

button2 = Button(bottomframe, text="Extract CT", command=extract_CT_button)
#button2.grid(row=5, column=3)
button2.pack(side = LEFT)

button3 = Button(bottomframe, text="Extract DD", command=extract_DD_button)
#button2.grid(row=5, column=3)
button3.pack(side = LEFT)

button4 = Button(bottomframe, text="Extract CT+DD", command=extract_CT_DD_button)
#button2.grid(row=5, column=3)
button4.pack(side = LEFT)

button5 = Button(bottomframe, text="Extract LBP", command=extract_LBP_button)
#button2.grid(row=5, column=3)
button5.pack(side = LEFT)

button6 = Button(bottomframe, text="Load Train", command=load_button)
#button3.grid(row=5, column=5)
button6.pack(side = LEFT)

button7 = Button(bottomframe, text="Load Query Folder", command=image_button)
#button4.grid(row=5, column=7)
button7.pack(side = LEFT)

button8 = Button(bottomframe, text="CT of QIM", command=extract_CT_QM_button)
#button5.grid(row=5, column=9)
button8.pack(side = LEFT)

button9 = Button(bottomframe, text="DD of QIM", command=extract_DD_QM_button)
#button5.grid(row=5, column=9)
button9.pack(side = LEFT)

button10 = Button(bottomframe, text="CT & DD of QIM", command=extract_CT_DD_QM_button)
#button5.grid(row=5, column=9)
button10.pack(side = LEFT)

button11 = Button(bottomframe, text="LBP of QIM", command=extract_LBP_QM_button)
#button5.grid(row=5, column=9)
button11.pack(side = LEFT)

button12 = Button(bottomframe, text="Load Test", command=load_Test_button)
#button3.grid(row=5, column=5)
button12.pack(side = LEFT)

button13 = Button(bottomframe, text="Recognition using ED", command=recognition_ED_button)
#button5.grid(row=5, column=9)
button13.pack(side = LEFT)

button14 = Button(bottomframe, text="Recognition using Cor", command=recognition_CR_button)
#button5.grid(row=5, column=9)
button14.pack(side = LEFT)

button15 = Button(bottomframe, text="Recognition using DT", command=recognition_DT_button)
#button5.grid(row=5, column=9)
button15.pack(side = LEFT)


mainloop()