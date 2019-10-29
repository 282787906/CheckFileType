import datetime
import math

import cv2
import numpy as np

import log
from config import debug
from project_tools import loadFile

method = eval('cv2.TM_CCOEFF_NORMED')


# 相似度匹配
# return 返回代码（retcode）
# retcode =0 成功
# retcode =1 原图小于模板
# retcode =2 模板相似度小于阈值
def checkTaxImg(img, template_path):
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # img =     directionCorrection(img);
    w, h = img.shape[::-1]
    # 加载将要搜索的图像模板
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    # 记录图像模板的尺寸
    w_template, h_template = template.shape[::-1]
    if w < w_template or h < h_template:
        return 1

    # 购买方模板'E:\\lqg\\Workspace\\python\\CheckFileType\\dirTemp\\3_91420502MA496LGY2F_2019_8_20190828154506700118.jpg'

    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc

    # 正向模板相似度阈值
    if max_val < 0.5:
        if debug:
            log.i('模板匹配：', '非增票', max_val)
        return 2

    else:
        if debug:
            log.i('模板匹配：', '增票', template_path, max_val)
        return 0


# 模板匹配（多模板 路径传参）
# return 0 匹配成功
#         1 匹配失败
#         2 尺寸不符合

def checkTaxImgDir(img_path, rootdir):
    list = cv2.os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    imgOld = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    w, h = imgOld.shape[::-1]
    if w != 1300 or h < 700:
        log.i('匹配失败 尺寸不符合', '宽度：', w, '高度', h)
        return 2
    img = directionCorrection2(imgOld);
    # cv2.imshow("input2", imgOld)
    # cv2.imshow(img_path, img)
    # cv2.waitKey(0)
    # cv2.imshow("img1", img)

    img = img[150:450, 0:350]  # 裁剪坐标为[y0:y1, x0:x1]
    # cv2.imshow('img1', img)
    # cv2.waitKey(0)
    for i in range(0, len(list)):
        template_path = cv2.os.path.join(rootdir, list[i])
        if h >= 820:  # 电子发票
            if not list[i].startswith('gmf_dz'):
                continue
        if h < 820:  # 非电子发票
            if list[i].startswith('gmf_dz'):
                continue
        ret_checkTaxImg = checkTaxImg(img, template_path)

        log.i('匹配：', h, img_path, template_path)
        if ret_checkTaxImg == 0:
            log.i('匹配成功：', img_path, template_path)
            # cv2.os.remove(img_path)
            return 0

    return 1


# 模板匹配（多模板 路径传参）
# return 0 匹配成功
#         1 匹配失败
#         2 尺寸不符合

def checkTaxImgResize(img_path, temp_path):
    imgOld = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    w, h = imgOld.shape[::-1]
    if w != 1300 or h < 700:
        log.i('匹配失败 尺寸不符合', '宽度：', w, '高度', h)
        return 2
    if h >= 820:  # 电子发票
        if not temp_path.startswith('gmf_dz'):
            return 2
        if h < 820:  # 非电子发票
            if temp_path.startswith('gmf_dz'):
                return 2

    img = directionCorrection2(imgOld);
    # cv2.imshow("input2", imgOld)
    # cv2.imshow(img_path, img)
    # cv2.waitKey(0)
    # cv2.imshow("img1", img)

    img = img[150:450, 0:350]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imshow('img1', img)
    cv2.waitKey(0)
    template_path = cv2.os.path.join(rootdir, temp_path)
    ret_checkTaxImg = checkTaxImg(img, template_path)
    log.i('匹配：', h, img_path, template_path)
    if ret_checkTaxImg == 0:
        log.i('匹配成功：', img_path, template_path)
        cv2.os.remove(img_path)
        return 0

    return 1


def showImg(rootdir):
    list = cv2.os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = cv2.os.path.join(rootdir, list[i])
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(image, 50, 150, apertureSize=3)

        # 霍夫变换
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
        if x1 == x2 or y1 == y2:
            return
        t = float(y2 - y1) / (x2 - x1)
        rotate_angle = math.degrees(math.atan(t))
        if rotate_angle > 45:
            rotate_angle = -90 + rotate_angle
        elif rotate_angle < -45:
            rotate_angle = 90 + rotate_angle
        if rotate_angle > -1 and rotate_angle < 1:
            cv2.imshow("imput", image)
            cv2.waitKey(0)
        else:

            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            log.d('倾斜角度', rotate_angle)
            M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

            cv2.imshow("imput2", image)
            cv2.imshow("output2", rotated)

            cv2.waitKey(0)


def checkDir(rootdir):
    list = cv2.os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    index = 1
    count = len(list)
    for i in range(0, len(list)):
        path = cv2.os.path.join(rootdir, list[i])
        temp = './templateFile'
        ret_checkTaxImg = checkTaxImgDir(path, temp)
        log.i(index, '/', count, path, '模板匹配：', 'checkTaxImg', ret_checkTaxImg)
        index = index + 1


def showImgWH(rootdir):
    list = cv2.os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = cv2.os.path.join(rootdir, list[i])
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        h, w = image.shape[:2]
        if (h < 820):
            log.d('image 高度：', h, '宽度：', w, list[i])
            cv2.imshow("output", image)
            cv2.waitKey(0)
        log.d('image 高度：', h, '宽度：', w)


# 方向矫正
def directionCorrection(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 截图 [y0:y1, x0:x1]
    # image = imag[0:128, 0:512]
    image = image[150:650, 100:1200]  # 裁剪坐标为[y0:y1, x0:x1]
    edges = cv2.Canny(image, 50, 200)
    # cv2.imshow("edges", edges)
    # 霍夫变换
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 255, minLineLength=60, maxLineGap=10)
    lines1 = lines[:, 0, :]
    # 提取为二维
    rotate_list = []
    sum = 0
    count = 0
    for x1, y1, x2, y2 in lines1[:]:
        t = float(y2 - y1) / (x2 - x1)
        rotate_angle = math.degrees(math.atan(t))
        if rotate_angle > 5 or rotate_angle < - 5 or x2 - x1 < 150:
            continue
        # cv2.line(image, (x1, y1), (x2, y2), (0, 225, 255), 1)
        rotate_list.append(rotate_angle)
        sum = sum + rotate_angle
        count = count + 1
        log.d('倾斜角度————', rotate_angle)
    rotate_angle = sum / count
    log.d('平均角度1————', rotate_angle)
    sum = 0
    count = 0
    # cv2.imshow("edgesLine", edges)
    rotate_list.sort()  # 默认升序排列
    log.d(rotate_list)
    index = 0
    for i in rotate_list:
        if index > len(rotate_list) * 0.2 and index < len(rotate_list) * 0.8:
            sum = sum + i
            count = count + 1

            log.d('倾斜角度2————', i)
        index = index + 1
    rotate_angle = sum / count

    log.d('平均角度2————', rotate_angle)

    if rotate_angle > -1 and rotate_angle < 1:
        return image
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    log.d('倾斜角度', rotate_angle)

    rotate_angle = calculationAngle(image, 0.6, 5)
    M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated


# 方向矫正
def directionCorrection2(image):
    imageCut = image[150:650, 100:1200]  # 裁剪坐标为[y0:y1, x0:x1]
    rotate_angle = calculationAngle(imageCut, 0.6, 5)
    if rotate_angle > -0.5 and rotate_angle < 0.5:
        return image
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # cv2.imshow("rotated", rotated)
    return rotated


# 计算倾斜角度
# samplingRate 采样率（取到得角度集合舍去最大最小只取中间）0.6
# maxDeviation 最大偏移  超过会忽略 5度
def calculationAngle(image, samplingRate, maxDeviation):
    try:

        edges = cv2.Canny(image, 50, 200)
        # 霍夫变换
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 255, minLineLength=60, maxLineGap=10)
        lines1 = lines[:, 0, :]
        # 提取为二维
        rotate_list = []
        sum = 0
        count = 0
        for x1, y1, x2, y2 in lines1[:]:
            if x2 == x1:
                continue
            t = float(y2 - y1) / (x2 - x1)
            rotate_angle = math.degrees(math.atan(t))
            if rotate_angle > maxDeviation or rotate_angle < - maxDeviation or x2 - x1 < 150:
                continue
            # cv2.line(image, (x1, y1), (x2, y2), (0, 225, 255), 1)
            rotate_list.append(rotate_angle)
            sum = sum + rotate_angle
            count = count + 1
            # log.d('倾斜角度————', rotate_angle)
        if (count == 0):
            return 0
        rotate_angle = sum / count
        # log.d('平均角度1————', rotate_angle)
        sum = 0
        count = 0
        # cv2.imshow("edgesLine", edges)
        rotate_list.sort()  # 默认升序排列
        # log.d(rotate_list)
        index = 0
        minIndex = len(rotate_list) * (1 - samplingRate) / 2
        maxIndex = len(rotate_list) * (1 - (1 - samplingRate) / 2)

        # log.d('采样率', samplingRate, 'minIndex', minIndex, 'maxIndex', maxIndex)
        for i in rotate_list:
            if index > minIndex and index < maxIndex:
                sum = sum + i
                count = count + 1

                # log.d('倾斜角度2————', i)
            index = index + 1
        if (count == 0):
            return 0
        rotate_angle = sum / count

        # log.d('平均角度2————', rotate_angle)
        return rotate_angle
    except BaseException as e:
        log.e(e)
        return 0


def cut():
    img = cv2.imread(cv2.os.path.abspath('test1.jpg'))
    log.d(img.shape)
    cropped = img[0:710, 0:1300]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imshow("output", cropped)
    directionCorrection(cropped)
    cv2.waitKey(0)


if __name__ == "__main__":
    log.i('start main')
    # file_origin_91310116MA1JAKP71J_2019_8_20190827143013540260.jpg
    url = 'http://sstax.cn:1000/file/origin/91310116MA1J9XA09T/2019/8/20190829082204839652.jpg'
    path = cv2.os.path.abspath('test.jpg')
    # template_path = "./templateFile/gmf_1_170.jpg"
    # loadFile(url, path)

    # ret_checkTaxImg =  checkTaxImg(path, template_path)
    # log.i('模板匹配：', 'checkTaxImg', ret_checkTaxImg)
    start = datetime.datetime.now()
    rootdir = './templateFile'
    # ret_checkTaxImg = checkTaxImgDir(path, rootdir)
    # log.i('模板匹配：', 'checkTaxImg', ret_checkTaxImg)

    # showImg('./dirProblemTax')
    # showImgWH('./dirProblemTax')
    # showImgWH('./dirTax')
    checkDir('./dirProblemTax');

    # image = cv2.imread(path)
    # directionCorrection(image);
    end = datetime.datetime.now()
    log.i('耗时：', (end - start).seconds)
    # cut()

