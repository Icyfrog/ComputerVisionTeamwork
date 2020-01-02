import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

import cv2
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageTk
import label

# init the global variable
imageLable = None
imagePath = ''
imagePathList = []
img_list = [
    "./image/test11.jpg",
    "./image/test12.jpg",
    "./image/test31.jpg",
    "./image/test34.jpg",
    "./image/test35.jpg"
]


# fit_size: change the size of the picture to fit the window
def fit_size(imageSize):
    windowSize = (1280, 800)
    ratio = float(imageSize[0]) / float(imageSize[1])
    height = float(windowSize[0]) / ratio
    length = float(windowSize[1]) * ratio

    if height > windowSize[1]:
        return int(length), windowSize[1]
    else:
        return windowSize[0], int(height)


def edit_images():
    fileNames = tkinter.filedialog.askopenfilenames()
    fileNamesList = list(fileNames)
    global imagePathList
    imagePathList = fileNamesList
    for i in imagePathList:
        print(i)
        label.oneFile(i)

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


def main():
    label.oneFile(imagePath)
    # label.oneDir('./demo')
    outputPath = imagePath + 'dir/output.jpg'
    output = cv2.imread(outputPath, 1)
    ''' 另一种展示图片的方式
    cv2.namedWindow('output', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('output', 1000, 1000)
    cv2.imshow('output', output)  # 展示图片，arg1：弹出form窗口的名称。arg2：图片
    cv2.waitKey(0)  # 暂停窗口
    cv2.destoryAllWindows()
    '''
    img_2 = output[:, :, [2, 1, 0]]
    plt.figure(figsize=(12, 8))
    plt.imshow(img_2), plt.axis('off')
    plt.show()
    ''' 另一种展示图片的方式
    im = Image.open(outputPath)
    im.show()
    '''


def settings():
    print('set settings!')


# create the window
window = tk.Tk()
# name the window
window.title('Computer Vision Project')
# define size of the window (length * width)
# golden ratio, use letter 'x' not '*' in math
window.geometry('1280x800')

# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menuBar = tk.Menu(window)

# 创建一个File菜单项（默认不下拉）
fileMenu = tk.Menu(menuBar, tearoff=0)

# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menuBar.add_cascade(label='File', menu=fileMenu)

# 在File中加入小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
fileMenu.add_command(label='Open...', command=open_image)
fileMenu.add_separator()  # 添加一条分隔线
fileMenu.add_command(label='Settings', command=settings)

# 创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editMenu = tk.Menu(menuBar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menuBar.add_cascade(label='Edit', menu=editMenu)

# 同样的在 Edit 中加入Roberts operator等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
editMenu.add_command(label='Edit one image', command=main)
editMenu.add_command(label='Edit images...', command=edit_images)

# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menuBar)

# 主窗口循环显示
# window.mainloop()


if __name__ == '__main__':
    # main()
    window.mainloop()
