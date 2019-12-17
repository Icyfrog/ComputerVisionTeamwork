# -*- coding: utf-8 -*-
# This file is for designing UI.
# Try to imitate the Pycharm mode.
# Reference : https://www.cnblogs.com/shwee/p/9427975.html
#             Tkinter UI structure
#           : https://www.tianqiweiqi.com/python-tkinter-filedialog.html
#             Tkinter file dialog
#             https://www.jianshu.com/p/05ef50ac89ac
#           :


import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
import function

# init the global variable
imageLable = None
imagePath = ''
seSize = (2, 2)
structureElement = []


# fit_size: change the size of the picture to fit the window
def fit_size(imageSize):
    windowSize = (1000, 618)
    ratio = float(imageSize[0]) / float(imageSize[1])
    height = float(windowSize[0]) / ratio
    length = float(windowSize[1]) * ratio

    if height > windowSize[1]:
        return int(length), windowSize[1]
    else:
        return windowSize[0], int(height)


# open_image: open photo from file dialog and show on the screen
def open_image():
    filePath = tkinter.filedialog.askopenfilename()
    global imagePath, imageLable
    imagePath = filePath
    image = cv2.imread(filePath)
    imageCV2 = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    imageShow = ImageTk.PhotoImage(imageCV2.resize(fit_size(imageCV2.size)))

    if imageLable is None:
        imageLable = tk.Label(image=imageShow)
        imageLable.image = imageShow
        imageLable.pack()
    else:
        imageLable.configure(image=imageShow)
        imageLable.image = imageShow
    return


def genSE():
    global structureElement, seSize
    kernel = None
    if len(structureElement) == 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, seSize)
    else:
        kernel = structureElement
    return kernel


def standard_edge_detection():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    kernel = genSE()
    erosion = function.bin_erosion(binary, kernel)
    dilation = function.bin_dilation(binary, kernel)
    result = cv2.subtract(dilation, erosion)
    resultImgName = 'EdgeDetSt' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)
    img2 = cv2.imread(resultImgName)
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()
    return


def external_edge_detection():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    kernel = genSE()
    dilation = function.bin_dilation(binary, kernel)
    result = np.subtract(dilation, binary)
    resultImgName = 'EdgeDetEx' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)

    img2 = cv2.imread(resultImgName)
    # print("hey!")
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()
    return


def internal_edge_detection():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    kernel = genSE()
    erosion = function.bin_erosion(binary, kernel)
    result = np.subtract(binary, erosion)
    resultImgName = 'EdgeDetIn' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)
    img2 = cv2.imread(resultImgName)
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()
    return


def standard_gradient():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = genSE()
    # line 124-128 can be replaced by line 129,130
    reSize = (len(img[0]), len(img))
    tmpDilation = function.gray_dilation(img, kernel)
    tmpErosion = function.gray_erosion(img, kernel)
    dilation = cv2.resize(np.uint8(tmpDilation), reSize)
    erosion = cv2.resize(np.uint8(tmpErosion), reSize)
    # dilation = cv2.dilate(img, kernel)
    # erosion = cv2.erode(img, kernel)
    result = 0.5 * cv2.subtract(dilation, erosion)
    resultImgName = 'StandardGradient_' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)
    img2 = cv2.imread(resultImgName)
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()


def external_gradient():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = genSE()
    # line 144-146 can be replaced by line 147
    reSize = (len(img[0]), len(img))
    tmpDilation = function.gray_dilation(img, kernel)
    dilation = cv2.resize(tmpDilation, reSize)
    # dilation = cv2.dilate(img, kernel)
    result = 0.5 * cv2.subtract(dilation, img)
    resultImgName = 'ExternalGradient_' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)
    img2 = cv2.imread(resultImgName)
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()


def internal_gradient():
    filePath = imagePath
    img = cv2.imread(filePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = genSE()
    # line 163-165 can be replaced by line 167
    '''
    reSize = (len(img[0]), len(img))
    tmpErosion = function.gray_erosion(img, kernel)
    erosion = cv2.resize(np.uint8(tmpErosion), reSize)
    '''
    erosion = cv2.erode(img, kernel)
    result = 0.5 * cv2.subtract(img, erosion)
    resultImgName = 'InternalGradient_' + filePath.replace('/', '_')
    cv2.imwrite(resultImgName, result)
    img2 = cv2.imread(resultImgName)
    plt.imshow(img2, cmap='gray'), plt.axis('off')
    plt.show()


'''
The following function cv2.dilate and cv2.erode 
are from the api of openCV, beacause my own realization costs
too much time...
'''

def cond_dilate_step(img, mask, kernel):
    last = img
    curr = img
    count = 0
    while True:
        count += 1
        curr = cv2.dilate(last, kernel)
        curr = np.min((curr, mask), axis=0)
        diff = cv2.subtract(curr, last)
        if not np.any(diff):
            break
        if count > 100:
            print('out')
            break
        last = curr
    return curr


def geodesic_dilate(img, mask, kernel, ):
    res = cv2.dilate(img, kernel)
    res = np.min((res, mask), axis=0)
    res = np.max((res, img), axis=0)
    return res


def geodesic_erode(img, mask, kernel):
    res = cv2.erode(img, kernel)
    res = np.max((res, mask), axis=0)
    res = np.min((res, img), axis=0)
    return res


def re_dilate(img, mask, kernel):
    last = img
    curr = img
    count = 0
    while True:
        count += 1
        curr = geodesic_dilate(last, mask, kernel)
        diff = cv2.subtract(curr, last)
        if not np.any(diff):
            break
        if count > 100:
            print('out')
            break
        last = curr
    return curr


def re_erode(img, mask, kernel):
    last = img
    curr = img
    count = 0
    while True:
        count += 1
        curr = geodesic_erode(last, mask, kernel)
        diff = cv2.subtract(curr, last)
        if not np.any(diff):
            break
        if count > 100:
            print('out')
            break
        last = curr
    return curr


def open_re(img, kernel):
    res = cv2.erode(img, kernel)
    res = re_dilate(res, img, kernel)
    return res


def close_re(img, kernel):
    res = cv2.dilate(img, kernel)
    res = re_erode(res, img, kernel)
    return res


def cond_dilate():
    global imagePath, structureElement, seSize
    filePath = imagePath
    if len(filePath) > 0:
        img = cv2.imread(filePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        kernel = genSE()
        marker = cv2.erode(binary, kernel, iterations=10)
        result = cond_dilate_step(marker, binary, kernel)

        resultImgName = 'condDilate' + filePath.replace('/', '_')
        cv2.imwrite(resultImgName, result)
        img2 = cv2.imread(resultImgName)
        plt.imshow(img2, cmap='gray'), plt.axis('off')
        plt.show()
        return
    else:
        return


def op_open_re():
    global imagePath, structureElement, seSize
    filePath = imagePath
    if len(filePath) > 0:
        img = cv2.imread(filePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = genSE()
        result = open_re(img, kernel)

        resultImgName = 'opOpenRe' + filePath.replace('/', '_')
        cv2.imwrite(resultImgName, result)
        img2 = cv2.imread(resultImgName)
        plt.imshow(img2, cmap='gray'), plt.axis('off')
        plt.show()
        return
    else:
        return


def op_close_re():
    global imagePath, structureElement, seSize
    filePath = imagePath
    if len(filePath) > 0:
        img = cv2.imread(filePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = genSE()
        result = close_re(img, kernel)

        resultImgName = 'opCloseRe' + filePath.replace('/', '_')
        cv2.imwrite(resultImgName, result)
        img2 = cv2.imread(resultImgName)
        plt.imshow(img2, cmap='gray'), plt.axis('off')
        plt.show()
        return
    else:
        return


def test_digit(content):
    if content.isdigit() or content == "":
        return True
    else:
        return False


def set_SE_size():
    global window, seSize

    settingWindow = tk.Toplevel(window)
    settingWindow.geometry('300x200')
    settingWindow.title('SE Size')

    test_cmd = settingWindow.register(test_digit)

    heightString = tk.StringVar(master=settingWindow, value=seSize[0])
    tk.Label(settingWindow, text='SE height: ').grid(row=1, column=0)
    entryHeight = tk.Entry(
        settingWindow,
        textvariable=heightString,
        validate='key',
        validatecommand=(test_cmd, '%P')
    )
    entryHeight.grid(row=1, column=1)

    weightString = tk.StringVar(master=settingWindow, value=seSize[1])
    tk.Label(settingWindow, text='SE Weight: ').grid(row=2, column=0)
    entryWeight = tk.Entry(
        settingWindow,
        textvariable=weightString,
        validate='key',
        validatecommand=(test_cmd, '%P')
    )
    entryWeight.grid(row=2, column=1)

    def save():
        global seSize
        newSize = (int(heightString.get()), int(weightString.get()))
        seSize = newSize
        settingWindow.destroy()
        return

    button = tk.Button(settingWindow, text='Save', command=save)
    button.grid(row=3, column=0, columnspan=2)
    return


def set_SE():
    global window, seSize, structureElement

    settingWindow = tk.Toplevel(window)
    settingWindow.title('SE Size')

    test_cmd = settingWindow.register(test_digit)
    rowNum = int(seSize[0])
    colNum = int(seSize[1])

    tmp = []
    for i in range(0, rowNum):
        row = []
        for j in range(0, colNum):
            String = None
            if len(structureElement) == 0:
                String = tk.StringVar(master=settingWindow, value='')
            else:
                String = tk.StringVar(master=settingWindow, value=structureElement[i][j])
            entry = tk.Entry(
                settingWindow,
                textvariable=String,
                validate='key',
                validatecommand=(test_cmd, '%P')
            )
            entry.grid(row=i, column=j)
            item = (String, entry)
            row.append(item)
        tmp.append(row)

    se = np.zeros(seSize, np.uint8)

    def save():
        global structureElement, seSize
        for i in range(0, rowNum):
            for j in range(0, colNum):
                item = tmp[i][j]
                string = item[0].get()
                num = 0
                if len(string) > 0:
                    num = int(string)
                se[i, j] = int(num)
        structureElement = se
        settingWindow.destroy()
        return

    def clean():
        global structureElement, seSize
        for i in range(0, rowNum):
            for j in range(0, colNum):
                item = tmp[i][j]
                entry = item[1]
                entry.delete(0, tk.END)
        structureElement = []
        return

    buttonSave = tk.Button(settingWindow, text='Save', command=save)
    buttonSave.grid(row=rowNum, column=0, columnspan=colNum)
    buttonClean = tk.Button(settingWindow, text='Clean', command=clean)
    buttonClean.grid(row=rowNum + 1, column=0, columnspan=colNum)
    return


def get_SSSEEE():
    ss = genSE()
    print(ss)


# create the window
window = tk.Tk()
# name the window
window.title('Computer Vision Project')
# define size of the window (length * width)
# golden ratio, use letter 'x' not '*' in math
window.geometry('1000x618')

# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menuBar = tk.Menu(window)

# 创建一个File菜单项（默认不下拉）
fileMenu = tk.Menu(menuBar, tearoff=0)

# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menuBar.add_cascade(label='File', menu=fileMenu)

# 在File中加入小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
fileMenu.add_command(label='Open...', command=open_image)

# 创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editMenu = tk.Menu(menuBar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menuBar.add_cascade(label='Edit', menu=editMenu)

# 同样的在 Edit 中加入Roberts operator等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
edgeDetMenu = tk.Menu(editMenu)
editMenu.add_cascade(label='Morphological edge detection', menu=edgeDetMenu)
edgeDetMenu.add_command(label='Standard', command=standard_edge_detection)
edgeDetMenu.add_command(label='External', command=external_edge_detection)
edgeDetMenu.add_command(label='Internal', command=internal_edge_detection)

gradientMenu = tk.Menu(editMenu)
editMenu.add_cascade(label='Morphological gradient', menu=gradientMenu)
gradientMenu.add_command(label='Standard', command=standard_gradient)
gradientMenu.add_command(label='External', command=external_gradient)
gradientMenu.add_command(label='Internal', command=internal_gradient)

editMenu.add_command(label='Conditional dilation', command=cond_dilate)
editMenu.add_command(label='OBR', command=op_open_re)
editMenu.add_command(label='CBR', command=op_close_re)

settingMenu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Settings', menu=settingMenu)
settingMenu.add_command(label="Structure Element size", command=set_SE_size)
settingMenu.add_command(label="Structure Element", command=set_SE)
settingMenu.add_command(label="Se print", command=get_SSSEEE)
# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menuBar)

# 主窗口循环显示
window.mainloop()
