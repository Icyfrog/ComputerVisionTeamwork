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

def swap(width, height, src, mask):
    # print(src)
    output = copy.deepcopy(src)
    y, x, _ = mask.shape
    # print(x,y,width,height,output.shape, src.shape)
    if (y+height>=src.shape[0] or x+width>=src.shape[1]):
        return
    for i in range(x):
        for j in range(y):   
            output[height + j,width + i] = mask[j, i]
    return output

def finalImage(dirpath):
    icon2, icon3, icon1 = getIcon()
    
    resultImagePath = dirpath + '/result.jpg'
    resultImage = cv2.imread(resultImagePath)
    # print(resultImagePath)

    f = open(dirpath+"/record.txt", mode='a')

    files = os.listdir(dirpath)
    for file in files:
        fileset = file.split('+')
        # print(fileset, resultImage.shape)
        if fileset[-1] == 'pos.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon1)
            f.writelines("x: " + fileset[1] + ", y: " + fileset[2] + " 正面\n")
        elif fileset[-1] == 'neg.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon2)
            f.writelines("x: " + fileset[1] + ", y: " + fileset[2] + " 反面\n")
        elif fileset[-1] == 'square.jpg':
            resultImage = swap(int(fileset[1]), int(fileset[2]), resultImage, icon3)
            f.writelines("x: " + fileset[1] + ", y: " + fileset[2] + " 侧面\n")
        else:
            continue

    f.close()

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