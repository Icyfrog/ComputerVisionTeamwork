import copy
import cv2
import os
import numpy as np

# image：输入图像 ,必须是8位的单通道灰度图像
# method：定义检测图像中圆的方法。目前唯一实现的方法是cv2.HOUGH_GRADIENT。
# dp：累加器分辨率与图像分辨率的反比。dp获取越大，累加器数组越小。
# minDist：检测到的圆的中心，（x,y）坐标之间的最小距离。如果minDist太小，则可能导致检测到多个相邻的圆。如果minDist太大，则可能导致很多圆检测不到。
# circles：输出结果，发现的圆信息
# param1：用于处理边缘检测的梯度值方法。
# param2：cv2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
# minRadius：最小半径
# maxRadius：最大半径
criticalRate = 0.6
diffDistanceRate = 0.28
distanceRate = 0.2


criticalRate = 0.2
minDistRate = 1.0
maxRadiusRate = 0.7
cutRate = 0.2

def findOneCircle(oriImg):
    img = copy.deepcopy(oriImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,
                           int(minDistRate/2* (oriImg.shape[0]+oriImg.shape[1])), param1=200, param2=25,
                           minRadius=10, maxRadius = int(maxRadiusRate/2* (oriImg.shape[0]+oriImg.shape[1])))

    if ( type(circles)==type(np.ones((1,1))) ):
        for circle in circles[0]:
            # 圆的基本信息
            # 坐标行列
            x = int(circle[0])
            y = int(circle[1])
            # 半径
            r = int(circle[2])
            # 在原图用指定颜色标记出圆的位置
            img = cv2.circle(img, (x, y), r, (0, 0, 255), 3)
            img = cv2.circle(img, (x, y), 2, (255, 255, 0), -1)
        return img,circle
    return img, circles

def cut(oriImg, circle):
    img = copy.deepcopy(oriImg)
    r = int(circle[2])

    # width,height = int(circle[0]),int(circle[1])
    centerY, centerX = int(circle[0]), int(circle[1])

    for x in range(len(img)):
        for y in range(len(img[0])):
            temp = (centerX-x)**2 + (centerY-y)**2

            cutWidth = int(cutRate/2* (oriImg.shape[0]+oriImg.shape[1]))
            if(temp > (r-cutWidth )* (r-cutWidth)  ):
                img[x][y]=[0,0,0]
    return img

def checkCircle(circle):

    if(type(circle)==type(np.ones((1,1)))):
        return True
    return False

def distance(center1,center2):
    return (center1[0]-center2[0])**2 + (center1[1]-center2[1])**2


def check(img,circle):
    centerX,centerY,R = int(circle[0]),int(circle[1]),int(circle[2])
    count = 0
    for i in range(10):
        x=int(centerX - R + R/5*i)
        # print(img[centerX - R + int(R//10)*i][centerY])
        if(img[x][centerY][2] == 255):
            count = count + 1
    for i in range(10):
        y=int(centerY - R + R/5*i)
        # print(img[centerX - R + int(R//10)*i][centerY])
        if(img[centerX][y][2] == 255):
            count = count + 1
    print("count",count)
    if(count>=7):
        return True
    return False

def checkFace(filename):
    img = cv2.imread(filename)

    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 膨胀，填充瓶盖轮廓内部空间成为一个连通区域

    kernelsize = (3,3)
    iterations = 3
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelsize)
    dilated = cv2.dilate(img1, kernel,1)
    img1 = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    res1,circle1 = findOneCircle(img1)

    r1 = int(circle1[2])
    center1 = (int(circle1[0]),int(circle1[1]))

    global BASIC_R
    BASIC_R = circle1[2]

    res2,circle2 = res1,circle1

    r2 = int(circle2[2])
    center2 = (int(circle2[0]),int(circle2[1]))

    if(check(res2,circle2)):
        print (False)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return False      

    r2 = int(circle2[2])
    center2 = (int(circle2[0]),int(circle2[1]))

    return True

# 找到所有符合条件的二进制图片，在这里就是正面和反面的图片
def eachfile(filepath):
    imagefile = []
    pathdir = os.listdir(filepath)

    for s in pathdir:
        newpath = os.path.join(filepath, s)
        if os.path.isfile(newpath):
            file = os.path.splitext(newpath.split('/')[-1])[0]
            if file[0] == 'b' and file[-1] == 'd':
                imagefile.append(newpath)
    return imagefile

def checkFile(fp):
    filepaths = eachfile(fp)
    for filepath in filepaths:
        print(filepath)
        result = checkFace(filepath)
        print(result)
        newpath = ''
        if result:
            newpath = filepath[:-9] + 'neg' + filepath[-4:]
        else:
            newpath = filepath[:-9] + 'pos' + filepath[-4:]
        os.rename(filepath, newpath)
        
