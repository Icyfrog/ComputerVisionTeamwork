# -*- coding: utf-8 -*-

import cv2
import os
import copy
import numpy as np

import cut
import circle

def getIcon():
    iconpath = './icon'
    files = os.listdir(iconpath)

    images=[]
    for file in files:
        images.append(cv2.imread(iconpath + '/' + file))
    return images

def swap(height, width, src, mask):
    output = copy.deepcopy(src)
    x, y, _ = mask.shape
    for i in range(x):
        for j in range(y):
            output[width + i, height + j] = mask[i, j]
    return output

def finalImage(dirpath):
    icon2, icon3, icon1 = getIcon()
    
    resultImagePath = dirpath + '/result.jpg'
    resultImage = cv2.imread(resultImagePath)

    files = os.listdir(dirpath)    
    for file in files:
        if file == "result.jpg" or file == "output.jpg":
            continue
        fileset = file.split('+')
        if fileset[3] == 'pos.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon1)
        elif fileset[3] == 'neg.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon2)
        elif fileset[3] == 'square.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon3)

    cv2.imwrite(dirpath + '/output.jpg', resultImage)

def oneFile(filepath):
    if filepath[-3:] == 'jpg' or filepath[-3:] == 'png':
        newfilepath = filepath + 'dir'

        cut.cutImg(filepath)
        circle.checkFile(newfilepath)
        finalImage(newfilepath)

def oneDir(dirpath):
    files = os.listdir(dirpath)
    for file in files:
        if file[-3:] == 'jpg' or file[-3:] == 'png':
            filepath = dirpath + '/' + file
            newfilepath = filepath + 'dir'

            cut.cutImg(filepath)
            circle.checkFile(newfilepath)
            finalImage(newfilepath)