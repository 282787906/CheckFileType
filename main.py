import datetime
import os
import shutil

import requests

import config
import log
from mysqlHelper import getFileTemp
from opencvHelper import checkTaxImg, checkTaxImgDir
from project_tools import loadFile


def main():
    pass


if __name__ == "__main__":
    log.i('start main')
    main()
    url = 'http://sstax.cn:1000/file/origin/91310116MA1JACH52Y/2019/8/20190827124429439294.jpg'

    dirTax = os.path.abspath('.') + '\\dirTax'
    dirUnTax = os.path.abspath('.') + '\\dirUnTax'
    dirProblemTax = os.path.abspath('.') + '\\dirProblemTax'
    dirTemp = os.path.abspath('.') + '\\dirTemp\\'
    template_path = "./templateFile/gmf_small.jpg"

    if not os.path.exists(dirTax):
        os.makedirs(dirTax)
    if not os.path.exists(dirUnTax):
        os.makedirs(dirUnTax)
    if not os.path.exists(dirTemp):
        os.makedirs(dirTemp)
    if not os.path.exists(dirProblemTax):
        os.makedirs(dirProblemTax)
    ret_getFile, data, msg = getFileTemp()
    if ret_getFile == 0:
        start = datetime.datetime.now()
        index = 1
        count = len(data)
        for row in data:
            path = row.name
            hhFlag = row.hh_flag
            url = config.domain + path
            log.i(index, '/', count, 'hhFlag:', hhFlag, 'path:', url)
            index = index + 1
            pathTemp = dirTemp + path.replace('/', '_').replace('file_origin', row.type)
            if not os.path.exists(pathTemp):
                ret_loadFile = loadFile(url, pathTemp)
            else:
                ret_loadFile = 200
            if ret_loadFile == 200:
                rootdir = './templateFile'
                ret_checkTaxImg = checkTaxImgDir(pathTemp, rootdir)
                if ret_checkTaxImg == 0:
                    shutil.copy(pathTemp, dirTax)

                else:

                    if hhFlag == 2:
                        shutil.copy(pathTemp, dirProblemTax)
                    else:
                        shutil.copy(pathTemp, dirUnTax)
            else:
                log.w("文件下载失败:", ret_loadFile)
        end = datetime.datetime.now()
        log.i('耗时：', (end - start).seconds)
    else:
        log.w('ret:', msg)
