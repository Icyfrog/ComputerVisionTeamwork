# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np

def condDilate(img, mask, kernel, anchor=(-1,-1)):
    last = img
    curr = img
    count = 0
    while True:
        count += 1
        curr = cv2.dilate(last, kernel, anchor=anchor)
        curr = np.min((curr,mask),axis=0)
        diff = cv2.subtract(curr, last)
        if not np.any(diff):
            break
        if count>10000:
            print('out')
            break
        last = curr
    return curr

def check_in(piece, total):
    x_p = piece[0]
    y_p = piece[1]
    w_p = piece[2]
    h_p = piece[3]
    for temp_piece in total:
        if((x_p > temp_piece[0] and \
            x_p < (temp_piece[0]+temp_piece[2])) and \
            (y_p > temp_piece[1] and y_p < (temp_piece[1]+temp_piece[3]))):
            return True
    return False

def createdir(dirname):
    isExists=os.path.exists(dirname)
    if not isExists:
        os.makedirs(dirname)
    return

def cutImg(filename):
    img = cv2.imread(filename)
    filename = filename+"dir"
    createdir(filename)
    result = img

    # 平滑，去除背景噪声
    img = cv2.GaussianBlur(img, (9,9), 2.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 自适应阈值二值化，找出瓶盖轮廓
    thresh = cv2.adaptiveThreshold(gray,255, \
        cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,9,2)
    # cv2.imwrite(filename+"/"+"thresh.jpg", thresh)

    # 先腐蚀，再条件膨胀，去除细小噪点
    # 再多次膨胀，使瓶盖轮廓成为一个连通区域
    kernelsize = (3,3)
    iterations = 16
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelsize)
    eroded = cv2.erode(thresh, kernel, iterations=2)
    # cv2.imwrite(filename+"/"+"eroded.jpg", eroded)
    thresh = condDilate(eroded,thresh,kernel)
    # cv2.imwrite(filename+"/"+"condDilate.jpg", thresh)
    dilate = cv2.dilate(thresh, kernel, iterations=iterations)
    # cv2.imwrite(filename+"/"+"dilate.jpg", dilate)

    # 查找边缘
    contours, hierarchy = cv2.findContours(dilate, \
        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    color = (0, 255, 0)
    # color1 = (0, 0, 255)
    # cv2.drawContours(img,contours,-1,color1)

    # 框出大片的连通区域
    i = 0
    temp_result = []
    temp_result_binary = []
    temp_pos = []
    temp_test_round = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if x == 0:
            continue
        temp = result[y:(y + h), x:(x + w)]
        temp_binary = thresh[y:(y + h), x:(x + w)]
        temp_round = dilate[y:(y + h), x:(x + w)]
        if not(w < 50 and h < 50): # 忽略过小的元素
            if(not(check_in([x, y, w, h], temp_pos))): # 不被更大的矩形包围
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 1) # 绘制矩形框
                temp_pos.append([x, y, w, h])
                temp_result.append(temp)
                temp_result_binary.append(temp_binary)
                temp_test_round.append(temp_round)
                i = i + 1

    # 确定正侧面，并保存结果图像
    for index in range(0,i):
        p = temp_result[index]
        b = temp_result_binary[index]
        r = temp_test_round[index]
        tmpx = temp_pos[index][0]
        tmpy = temp_pos[index][1]
        tmpw = temp_pos[index][2]
        tmph = temp_pos[index][3]
        tail = 'round'
        gapew = int(tmpw*0.03)
        gapeh = int(tmph*0.03)
        # print(tmpw,tmph)

        if tmpw<=gapew or tmph<=gapeh or gapeh<0 or gapew<0:
            continue
        # 边框四点不都是白色，为方形
        if not(r[gapeh,int(tmpw/2)]==255 and \
            r[tmph-gapeh-1,int(tmpw/2)]==255 and \
            r[int(tmph/2),gapew]==255 and \
            r[int(tmph/2),tmpw-gapew-1]==255):
            tail = 'square'
        # 宽高比远离1，为方形
        if tmpw/tmph>1.2 or tmpw/tmph<0.8:
            tail = 'square'
        # cv2.imwrite(filename+"/"+str(tmpx)+"+"+str(tmpy)+"+"+tail+".jpg",p)
        cv2.imwrite(filename+"/"+"binary+"+str(tmpx)+"+"+str(tmpy)+"+"+tail+".jpg",b)

    cv2.imwrite(filename+"/"+"result.jpg", img)
    return
