from datetime import datetime
import time

import requests

import config
import log
import mail
import messageBox
from mysqlHelper import getConnStatus, getUnHeHeCount, getUnPdfCount, getUnHeHeWaitTime, getUnCreateWaitTime

from module.connConfig import connConfig
from project_tools import loadByHeaders


def checkConn(rate):
    dataConn = []

    dataConn.append(connConfig("主库 ", config.dbHost, config.dbPort, config.dbUser, config.dbPasswd, config.dbPlatform))
    dataConn.append(connConfig("分库1", config.dbHost, 3122, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库2", config.dbHost, 3123, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库3", config.dbHost, 3124, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库4", config.dbHost, 3125, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库5", config.dbHost, 3126, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库6", config.dbHost, 30127, config.dbUser, "Pwd2018db", ""))
    warnMsg = ''
    retCode = 0;
    for conn in dataConn:
        code, max, count, msg = getConnStatus(conn)
        useRate = round(count / max * 100, 2)
        msg = conn.dbName + " 最大连接数:" + str(max) + ' 当前连接数:' + str(count) + ' 使用率:' + str(useRate) + '%'
        # print(msg)
        if useRate > rate:
            warnMsg = warnMsg + msg + '\n'
            retCode = 1

    return retCode, warnMsg


def loadByHeaders(uid):
    times = 0
    while True:
        imgres = requests.get('http://sstax.cn:1000/cs-third/cer/commonForApi/getCommonAccountInfo',
                              params={'accountSetUid': uid}, headers={'uid': uid})
        if imgres.status_code != 200:
            return imgres.status_code, imgres.reason
        times = times + 1
        if times > 5:
            return imgres.status_code, None
    return imgres.status_code


if __name__ == "__main__":
    CONN_RATE_THRESHOLD=50
    CREATE_PZ_WAIT_COUNT_THRESHOLD=20
    HE_HE_WAIT_TIME_THRESHOLD=120
    PDF_WAIT_THRESHOLD=50
    SLEEP=300
    while True:
        mailMsg = ''
        print(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        hour=datetime.now().hour
        if hour>6 and hour<21:
            try:
                retCode, warnMsg = checkConn(CONN_RATE_THRESHOLD)
                if retCode != 0:
                    # log.w(warnMsg)
                    mailMsg = mailMsg + warnMsg + '\n'
                retCode, minutes, msg = getUnCreateWaitTime()
                if retCode == 0 and minutes>CREATE_PZ_WAIT_COUNT_THRESHOLD:
                    log.w('生成凭证等待:', minutes)
                    mailMsg = mailMsg + "识别成功自动生成凭证等待  时间："+str(minutes) + '分钟\n'
                retCode, minutes, msg = getUnHeHeWaitTime()
                if retCode == 0 and minutes > HE_HE_WAIT_TIME_THRESHOLD:
                    log.w('heheWait_Time:', minutes)
                    mailMsg = mailMsg + "合合识别积压  时间：" + str(minutes) + '分钟\n'
                retCode, count, msg = getUnPdfCount()
                if retCode == 0 and count>PDF_WAIT_THRESHOLD:
                    log.w('pdfCount:', count)
                    mailMsg = mailMsg + "凭证生成pdf积压" + str(count) + '\n'
                retCode, msg = loadByHeaders('20171009-102958-845')
                if retCode != 200:
                    log.w('status_code:', retCode, 'msg:', msg)
                    mailMsg = mailMsg + "third调用 code:" + str(retCode)+"  "+msg + '\n'
                print(mailMsg)
                if len(mailMsg)>0:
                    mail.send("财税警告",mailMsg)
                else:
                    log.w('状态正常')
            except Exception  as e:
                log.e('状态监控异常', e)

        time.sleep(SLEEP)
