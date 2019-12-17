from numpy import *
import cv2


def bin_erosion(ori_img, se, center=None):
    img_height = len(ori_img)
    img_width = len(ori_img[0])
    se_height = len(se)
    se_width = len(se[0])
    # init center
    if center == None:
        center = [int(se_height / 2), int(se_width / 2)]
    # init ret_img
    ret_height = img_height
    ret_width = img_width
    ret_img = [[0] * ret_width for k in range(ret_height)]
    # create ret_img
    for h in range(ret_height):
        for w in range(ret_width):
            flag = True
            for se_h in range(se_height):
                for se_w in range(se_width):
                    th_h = int(h + se_h)
                    th_w = int(w + se_w)
                    if th_h + 1 < img_height and th_w + 1 < img_width:
                        if se[se_h][se_w] != 0 and ori_img[th_h][th_w] == 0:
                            flag = False
            if flag:
                ret_img[h][w] = 255
    return array(ret_img)


def bin_dilation(ori_img, se, center=None):
    img_height = len(ori_img)
    img_width = len(ori_img[0])
    se_height = len(se)
    se_width = len(se[0])
    # init center
    if center == None:
        center = [int(se_height / 2), int(se_width / 2)]
    # init ret_img
    ret_height = img_height
    ret_width = img_width
    ret_img = [[0] * ret_width for k in range(ret_height)]
    # create ret_img
    for h in range(img_height):
        for w in range(img_width):
            inta = ori_img[h][w]
            if inta != 0:
                for se_h in range(se_height):
                    for se_w in range(se_width):
                        if se[se_h][se_w] != 0:
                            if (h + se_h + 1) < ret_height and (w + se_w + 1) < ret_width:
                                ret_img[h + se_h][w + se_w] = 255
    return array(ret_img)


def gray_dilation(ori_img, se):
    img_height = len(ori_img)
    img_width = len(ori_img[0])
    se_height = len(se)
    se_width = len(se[0])
    # create procedure imgs
    # each img based on (ori_img and 1 block of se)
    # size=ret_img
    pcd_imgs = []
    ret_height = img_height + se_height - 1
    ret_width = img_width + se_width - 1
    for i in range(se_height):
        for j in range(se_width):
            th_img = [[-inf] * ret_width for k in range(ret_height)]  # init array
            for h in range(img_height):
                for w in range(img_width):
                    th_img[h + i][w + j] = ori_img[h][w] + se[i][j]
            pcd_imgs.append(th_img)
    # calculate MAX for each pixel
    ret_img = [[-inf] * ret_width for k in range(ret_height)]
    for h in range(ret_height):
        for w in range(ret_width):
            vals = []
            for item in pcd_imgs:
                vals.append(item[h][w])
            ret_img[h][w] = max(vals)
    return array(ret_img)


def gray_erosion(ori_img, se):
    img_height = len(ori_img)
    img_width = len(ori_img[0])
    se_height = len(se)
    se_width = len(se[0])
    # create procedure imgs
    # each img based on (ori_img and 1 block of se)
    # size=ret_img
    pcd_imgs = []
    ret_height = img_height + se_height - 1
    ret_width = img_width + se_width - 1
    for i in range(se_height):
        for j in range(se_width):
            th_img = [[-inf] * ret_width for k in range(ret_height)]  # init array
            for h in range(img_height):
                for w in range(img_width):
                    th_img[h + se_height - i - 1][w + se_width - j - 1] = ori_img[h][w] - se[i][j]
            pcd_imgs.append(th_img)
    # calculate MIN for each pixel
    ret_img = [[-inf] * ret_width for k in range(ret_height)]
    for h in range(ret_height):
        for w in range(ret_width):
            vals = []
            for item in pcd_imgs:
                vals.append(item[h][w])
            ret_img[h][w] = min(vals)
    w = se_width - 1
    h = se_height - 1
    return array(ret_img)[h:-h, w:-w]

