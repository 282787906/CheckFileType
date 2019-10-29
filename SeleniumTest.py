import random
import time
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

import config
import log
from ExcelTools import read_document, read_documentInput
from module.AccountSetInfo import AccountSetInfo
from mysqlHelper import getTemplateSubjectById

window_size_w = 1400
window_size_h = 900
current_x = 0
current_y = 0
WHILE_WAIT_SLEEP = 0.5
ACTION_WAIT_SLEEP_SHORT = 0.2
ACTION_WAIT_SLEEP_LONG = 0.3
HOST_THIRD = config.domain
LOAD_PAGE_TIMEOUT = 30


def mouseLeftClick(_driver, x, y):
    global current_x
    offset_x = x - current_x
    current_x = x;
    global current_y
    offset_y = y - current_y
    current_y = y

    # log.d('鼠标左键点击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(offset_x, offset_y).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标 多次使用时偏移累加


def mouseLeftDoubleClick(_driver, x, y):
    global current_x
    offset_x = x - current_x
    current_x = x;
    global current_y
    offset_y = y - current_y
    current_y = y

    # log.d('鼠标左键双击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(offset_x,
                                         offset_y).double_click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标 多次使用时偏移累加


def mouseLocationReset(_driver):
    global current_x
    offset_x = 0 - current_x
    current_x = 0;
    global current_y
    offset_y = 0 - current_y
    current_y = 0

    log.d('mouseLocationReset', offset_x, offset_y)
    ActionChains(_driver).move_by_offset(current_x, current_y).perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标


def mouseRightClick(_driver, x, y):
    global current_x
    offset_x = x - current_x
    current_x = x;
    global current_y
    offset_y = y - current_y
    current_y = y

    log.d('鼠标右键点击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(current_x, current_y).context_click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标


def clearElement(element):
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)


# if __name__ == "__main__":
#     option = webdriver.ChromeOptions()
#     option.add_argument('disable-infobars')
#     driver = webdriver.Chrome(chrome_options=option)
#
#     driver.set_window_size(window_size_w, window_size_h)
#     driver.get("http://www.html580.com/7881/demo")
#     # ActionChains(driver).move_to_element("divBtn").perform()
#     ActionChains(driver).move_by_offset(105, 155).perform()
#     time.sleep(ACTION_WAIT_SLEEP)
#
#     ActionChains(driver).move_by_offset(100, 155).perform()
#     time.sleep(20)
#     driver.quit()
def login(driver, userName, pwd):
    log.d('登录', userName)
    driver.get(HOST_THIRD + "/#/login")
    driver.find_element_by_name('username').send_keys(userName)
    driver.find_element_by_name('password').send_keys(pwd)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    driver.find_element_by_name('btn_login').send_keys(Keys.ENTER)
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/#/dashboard"):
            return 0
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    return 1


def createAccount(driver, accountSetInfo):
    accountSetInfo = AccountSetInfo('companyName', 'taxidCode000000000', 1, 2018, 8, 1, '小企业会计制度多行业科目体系', '默认组', '伊文科技',
                                    '通用公式')
    log.d('建账')
    driver.get(HOST_THIRD + "/#/third/customer")

    driver.find_element_by_id('btn_company_add').send_keys(Keys.ENTER)
    driver.find_element_by_name('input_company_name').send_keys(accountSetInfo.companyName)

    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(accountSetInfo.taxidCode)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    type = accountSetInfo.taxType
    if type == 0:
        driver.find_elements_by_class_name('el-radio')[0].click()  # 0小规模 1 一般纳税人 2申报周期 月 3 申报周期 季度
        driver.switch_to.active_element.send_keys(Keys.TAB)
    else:
        driver.find_elements_by_class_name('el-radio')[1].click()  # 0小规模 1 一般纳税人 2申报周期 月 3 申报周期 季度
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    yearStr = driver.find_elements_by_class_name('el-date-picker__header-label')[0].text
    monthStr = driver.find_elements_by_class_name('el-date-picker__header-label')[1].text
    year = int(yearStr.split(' ')[0])
    month = int(monthStr.split(' ')[0])
    lastYear = driver.find_element_by_class_name('el-icon-d-arrow-left')
    lastMonth = driver.find_elements_by_class_name('el-icon-arrow-left')[1]
    nextYear = driver.find_element_by_class_name('el-icon-d-arrow-right')
    nextMonth = driver.find_elements_by_class_name('el-icon-arrow-right')[1]

    years = accountSetInfo.startDateYear - year
    if years < 0:
        for i in range(-1 * years):  # <<
            ActionChains(driver).move_to_element(lastYear).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
    if years > 0:
        for i in range(years):  # >>
            ActionChains(driver).move_to_element(nextYear).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
    months = accountSetInfo.startDateMonth - month
    if months < 0:
        for i in range(-1 * months):  # <<
            ActionChains(driver).move_to_element(lastMonth).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
    if months > 0:
        for i in range(months):  # >>
            ActionChains(driver).move_to_element(nextMonth).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)

    driver.switch_to.active_element.send_keys(Keys.ENTER)
    print("mouseRightClick  Over")
    ActionChains(driver).move_to_element(driver.find_element_by_name("select_account_system")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    accountSystems = driver.find_elements_by_name('li_account_system')
    for i in range(len(accountSystems)):
        driver.find_element_by_name("select_account_system").send_keys(Keys.DOWN)
        if accountSystems[i].text == accountSetInfo.accountSystem:
            ActionChains(driver).move_to_element(accountSystems[i]).click().perform()
            break

        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_org_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    orgs = driver.find_elements_by_name('li_org_id')
    for i in range(len(orgs)):
        driver.find_element_by_name("select_org_id").send_keys(Keys.DOWN)
        if orgs[i].text == accountSetInfo.org:
            ActionChains(driver).move_to_element(orgs[i]).click().perform()
            break

        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_zx_center")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    zxCenters = driver.find_elements_by_name('li_zx_center')

    for i in range(len(zxCenters)):
        driver.find_element_by_name("select_zx_center").send_keys(Keys.DOWN)
        if zxCenters[i].text == accountSetInfo.zxCenter:
            ActionChains(driver).move_to_element(zxCenters[i]).click().perform()
            break
        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_zcfzgs")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    zcfzgs = driver.find_elements_by_name('li_zcfzgs')
    for i in range(len(zcfzgs)):
        driver.find_element_by_name("select_zcfzgs").send_keys(Keys.DOWN)
        if zcfzgs[i].text == accountSetInfo.zcfzgs:
            ActionChains(driver).move_to_element(zcfzgs[i]).click().perform()
            break

        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_auditer_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    auditerIds = driver.find_elements_by_name('li_auditer_id')
    for i in range(len(auditerIds)):
        driver.find_element_by_name("select_auditer_id").send_keys(Keys.DOWN)
        if "审核员" in auditerIds[i].text:
            ActionChains(driver).move_to_element(auditerIds[i]).click().perform()
            driver.find_element_by_name("select_auditer_id").send_keys(Keys.ESCAPE)
            break
        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_input_user_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    inputUserIds = driver.find_elements_by_name('li_input_user_id')
    for i in range(len(inputUserIds)):
        driver.find_element_by_name("select_input_user_id").send_keys(Keys.DOWN)
        if "录入员" in inputUserIds[i].text:
            ActionChains(driver).move_to_element(inputUserIds[i]).click().perform()
            driver.find_element_by_name("select_input_user_id").send_keys(Keys.ESCAPE)
            break
        time.sleep(ACTION_WAIT_SLEEP_SHORT)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_information_officer_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    informationOfficerIds = driver.find_elements_by_name('li_information_officer_id')
    ActionChains(driver).move_to_element(informationOfficerIds[0]).click().perform()
    driver.find_element_by_name("select_information_officer_id").send_keys(Keys.ESCAPE)
    time.sleep(ACTION_WAIT_SLEEP_LONG)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_scanner_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    scannerIds = driver.find_elements_by_name('li_scanner_id')
    ActionChains(driver).move_to_element(scannerIds[0]).click().perform()
    driver.find_element_by_name("select_scanner_id").send_keys(Keys.ESCAPE)
    time.sleep(ACTION_WAIT_SLEEP_LONG)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_declarer_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    declarerIds = driver.find_elements_by_name('li_declarer_id')
    ActionChains(driver).move_to_element(declarerIds[0]).click().perform()
    driver.find_element_by_name("select_declarer_id").send_keys(Keys.ESCAPE)
    time.sleep(ACTION_WAIT_SLEEP_LONG)

    ActionChains(driver).move_to_element(driver.find_element_by_name("select_info_completion_id")).click().perform()
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    infoCompletionIds = driver.find_elements_by_name('li_info_completion_id')
    ActionChains(driver).move_to_element(infoCompletionIds[0]).click().perform()
    driver.find_element_by_name("select_info_completion_id").send_keys(Keys.ESCAPE)
    time.sleep(ACTION_WAIT_SLEEP_LONG)

    driver.find_element_by_name('input_sb_taxrate').send_keys('22')
    driver.find_element_by_name('input_sb_stock').send_keys('33')
    driver.find_element_by_name('input_scanning_date').send_keys('1')
    driver.find_element_by_name('input_checkout_date').send_keys('28')
    driver.find_element_by_name('input_sb_stock_proportion1').send_keys('1')
    driver.find_element_by_name('input_sb_stock_proportion2').send_keys('2')
    driver.find_element_by_name('input_sb_stock_proportion3').send_keys('3')
    driver.find_element_by_name('input_sb_stock_proportion4').send_keys('4')
    driver.find_element_by_name('input_sb_stock_proportion5').send_keys('5')
    driver.find_element_by_name('btn_save').send_keys(Keys.ENTER)


def toThird(driver, company, tax):
    log.d('进账簿', company)
    driver.get(HOST_THIRD + "/#/third/customer")
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    driver.find_element_by_id('input_company').send_keys(company)
    driver.find_element_by_id('btn_company_sreach').send_keys(Keys.ENTER)
    count = 0
    while count < LOAD_PAGE_TIMEOUT:
        elements = driver.find_elements_by_name('btn_to_third')
        elements_name = driver.find_elements_by_name('span_companyName')
        if len(elements) == 1 and len(elements_name) == 1 and elements_name[0].text == company:
            break
        if count == LOAD_PAGE_TIMEOUT - 1:
            log.e("账套查询结果数量：", len(elements))
            return 2
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    elements[0].send_keys(Keys.ENTER)
    # time.sleep(1)
    # mouseLeftClick(driver, 1040, 225)  # 进账簿

    # count = 0
    # while count < LOAD_PAGE_TIMEOUT:
    #     if 'cer/certificate/jdtj' in driver.current_url:
    #         print(driver.find_element_by_class_name('company-name').text)
    #         return 0
    #     count = count + 1
    #     time.sleep(WHILE_WAIT_SLEEP)
    driver.get_cookies()
    if company == driver.find_element_by_class_name('company-name').text and \
            tax == driver.get_cookie('tax_code')['value']:
        return 0
    return 1


def addCertificateWithOutPartner(driver):
    log.d('新增凭证')
    driver.get(HOST_THIRD + "/cs-third/cer/certificate/toAddCertificate")
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/cs-third/cer/certificate/toAddCertificate"):
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    alertDiv = driver.find_element_by_id('alertDiv')
    startX = alertDiv.location['x'] + 100 + 135
    startY = alertDiv.location['y'] + 150

    file = 'C:\\Users\\Liqg\\Desktop\\book1.xlsx'
    ret, documents, msg = read_document(file)
    if ret != 0:
        log.e('加载凭证文件失败', msg)
        return
    if len(documents) == 0:
        log.w('加载凭证文件数量为0')
        return
    for document in documents:
        count = 0
        while (count < LOAD_PAGE_TIMEOUT):
            if ('零元整' == driver.find_element_by_id('hjjesx').text):
                break
            count = count + 1
            log.w('等待零元整', count)
            time.sleep(WHILE_WAIT_SLEEP)
        mouseLeftDoubleClick(driver, startX, startY)

        for index in range(len(document)):
            documentDetail = document[index]
            clearElement(driver.switch_to_active_element())
            driver.switch_to_active_element().send_keys(documentDetail.summary)

            driver.switch_to_active_element().send_keys(Keys.TAB)
            driver.switch_to_active_element().send_keys(documentDetail.account_code)
            driver.switch_to_active_element().send_keys(Keys.TAB)
            if documentDetail.debit_amount != '\\N':  # 钱在借方
                print(documentDetail.debit_amount)

                clearElement(driver.switch_to_active_element())
                driver.switch_to_active_element().send_keys(documentDetail.debit_amount)  # 如果钱在借方。 tab时直接换行
            else:
                print(documentDetail.credit_amount)
                clearElement(driver.switch_to_active_element())  # 清空借方默认金额
                driver.switch_to_active_element().send_keys(Keys.TAB)
                clearElement(driver.switch_to_active_element())
                driver.switch_to_active_element().send_keys(documentDetail.credit_amount)
            if (index != len(document) - 1):
                driver.switch_to_active_element().send_keys(Keys.TAB)
        #
        driver.find_element_by_id('btn_xzpz_add_and_save').send_keys(Keys.ENTER)
    return 0


def addCertificateWithPartner(driver):
    log.d('新增凭证')
    driver.get(HOST_THIRD + "/cs-third/cer/certificate/toAddCertificate")
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/cs-third/cer/certificate/toAddCertificate"):
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    alertDiv = driver.find_element_by_id('alertDiv')
    startX = alertDiv.location['x'] + 100 + 135
    startY = alertDiv.location['y'] + 150

    file = 'C:\\Users\\Liqg\\Desktop\\book1.xlsx'
    ret, documents, msg = read_document(file)
    if ret != 0:
        log.e('加载凭证文件失败', msg)
        return
    if len(documents) == 0:
        log.w('加载凭证文件数量为0')
        return
    for document in documents:
        count = 0
        while (count < LOAD_PAGE_TIMEOUT):
            if ('零元整' == driver.find_element_by_id('hjjesx').text):
                break
            count = count + 1
            log.w('等待零元整', count)
            time.sleep(WHILE_WAIT_SLEEP)
        mouseLeftDoubleClick(driver, startX, startY)

        for index in range(len(document)):
            documentDetail = document[index]
            clearElement(driver.switch_to_active_element())
            driver.switch_to_active_element().send_keys(documentDetail.summary)
            driver.switch_to_active_element().send_keys(Keys.TAB)

            driver.switch_to_active_element().send_keys(documentDetail.account_code)
            # driver.switch_to_active_element().send_keys(Keys.TAB)
            if documentDetail.partner_name != '\\N':  # 往来类型
                time.sleep(ACTION_WAIT_SLEEP_LONG)
                # driver.find_element_by_id('select2-wldw-container').send_keys(Keys.ENTER)
                # driver.find_element_by_id('select2-wldw-container').send_keys(documentDetail.partner_name)

                driver.find_element_by_id('wldw_sub').send_keys(Keys.ENTER)

            driver.switch_to_active_element().send_keys(Keys.TAB)
            if documentDetail.debit_amount != '\\N':  # 钱在借方
                print(documentDetail.debit_amount)
                clearElement(driver.switch_to_active_element())
                driver.switch_to_active_element().send_keys(documentDetail.debit_amount)  # 如果钱在借方。 tab时直接换行
            else:
                print(documentDetail.credit_amount)
                clearElement(driver.switch_to_active_element())  # 清空借方默认金额
                driver.switch_to_active_element().send_keys(Keys.TAB)
                clearElement(driver.switch_to_active_element())
                driver.switch_to_active_element().send_keys(documentDetail.credit_amount)
            if (index != len(document) - 1):
                driver.switch_to_active_element().send_keys(Keys.TAB)
        #
        driver.find_element_by_id('btn_xzpz_add_and_save').send_keys(Keys.ENTER)
    return 0


def toCertificateInput(driver):
    log.d('录入凭证')

    file = 'C:\\Users\\Liqg\\Desktop\\book1.xlsx'
    ret, documents, msg = read_documentInput(file)
    if ret != 0:
        log.e('加载凭证文件失败', msg)
        return
    if len(documents) == 0:
        log.w('加载凭证文件数量为0')
        return
    spCount = 0
    cpCount = 0
    nblzCount = 0
    for document in documents:
        if document[0].type == 1:
            spCount = spCount + 1
        if document[0].type == 2:
            cpCount = cpCount + 1
        if document[0].type == 3:
            nblzCount = nblzCount + 1

    document = documents[0]
    driver.get(HOST_THIRD + "/cs-third/cer/certificate/toCertificateInput")
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/cs-third/cer/certificate/toCertificateInput"):
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)

    driver.find_element_by_id('uniformCreditCode').send_keys(document[0].tax_no)
    driver.find_element_by_id('currentDate').click()
    years = document[0].year - int(driver.find_elements_by_class_name('datepicker-switch')[1].text)

    if years < 0:
        for i in range(-1 * years):  # <<
            ActionChains(driver).move_to_element(driver.find_elements_by_class_name('prev')[1]).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
    if years > 0:
        for i in range(years):  # >>
            ActionChains(driver).move_to_element(driver.find_elements_by_class_name('next')[1]).click().perform()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
    months = driver.find_elements_by_class_name('month')
    for month in months:
        if str(document[0].month) in month.text:
            ActionChains(driver).move_to_element(month).click().perform()
            break
    isOpenOriginCertificate = 0
    for documentIndex in range(len( documents)):

        document = documents[documentIndex]
        ActionChains(driver).move_to_element(
            driver.find_elements_by_class_name('iCheck-helper')[document[0].type - 1]).click().perform()

        driver.find_element_by_class_name("btn-success").send_keys(Keys.ENTER)
        # print('原始凭证',driver.find_element_by_class_name('allcount').text.split('   ')[1] )

        if isOpenOriginCertificate == 0:  # 打开原始凭证
            isOpenOriginCertificate = 1
            driver.find_element_by_id("originCertificate").send_keys(Keys.ENTER)
            driver.find_element_by_id("originCertificateConfirm").send_keys(Keys.ENTER)
            handles = driver.window_handles
            time.sleep(ACTION_WAIT_SLEEP_LONG)

            driver.switch_to_window(handles[0]);  # switch back to main screen

            time.sleep(ACTION_WAIT_SLEEP_LONG)
            count = int(driver.find_element_by_class_name('allcount').text.split('   ')[1][4:])
            if count == 0:
                log.i('原始凭证不存在')
                return
            if document[0].type == 1 and count < spCount:
                log.i('原始凭证收票数量不足', count, spCount)
                return
            if document[0].type == 2 and count < cpCount:
                log.i('原始凭证出票数量不足', count, cpCount)
                return
            if document[0].type == 3 and count < nblzCount:
                log.i('原始凭证内部流转数量不足', count, nblzCount)
                return
        divBtn = driver.find_element_by_id('divBtn')
        ActionChains(driver).move_to_element(divBtn).perform()
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        smallClasses = driver.find_elements_by_xpath("//ul[@class = 'dropspan-ul']/li")
        for i in range(len(smallClasses)):
            ActionChains(driver).move_to_element(smallClasses[i]).perform()
            templates = driver.find_elements_by_xpath("//ul[@class = 'dropspan-ul']/li[" + str(i + 1) + "]/ul/li")
            isbreak = 0
            for j in range(len(templates)):
                if templates[j].text == document[0].TEMPLATED_NAME:
                    ActionChains(driver).move_to_element(templates[j]).click().perform()
                    isbreak = 1
                    break
            if isbreak == 1:
                break
            if i == len(smallClasses) - 1:
                print('模板未找到', document[0].TEMPLATED_NAME)
                return 2, '模板未找到', document[0].TEMPLATED_NAME
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        ret_getFile, dataTemplates, msg = getTemplateSubjectById(document[0].TEMPLATED_ID)
        if ret_getFile != 0 or len(dataTemplates) == 0:
            log.e('加载模板失败', msg)
            return
        # ActionChains(driver).move_to_element(
        #     driver.find_element_by_class_name('sz-zkm')).click().perform()
        # time.sleep(ACTION_WAIT_SLEEP_LONG)

        sj = 1
        hasBank = 0
        for detail in document :
            for template in dataTemplates:
                isSum = 0
                if template.kmCode in detail.account_code:
                    if (template.subjectType == 1 or template.subjectType == 2) and template.jdType == 0:
                        isSum = 1
                    if template.subjectType == 3 and template.jdType == 1:
                        isSum = 1
                    if (template.subjectType == 4 or template.subjectType == 5) and sj == 1:
                        isSum = 1
                        sj == 0
                    id = 'ts' + str(template.tsId)
                    if isSum == 0:
                        elementInput = driver.find_element_by_id(id)
                        # if elementInput.text!='':
                        clearElement(elementInput)
                        if template.jdType == 0:
                            elementInput.send_keys(str(detail.credit_amount))
                        else:
                            elementInput.send_keys(str(detail.debit_amount))
                    # else:
                    if getFeatureCdByCode(template.kmCode) == 2:  # 银行
                        # sz_zkm=driver.find_element(By.CLASS_NAME,'sz-zkm')
                        sz_zkm = driver.find_element_by_class_name('sz-zkm')
                        print('location', driver.find_element_by_class_name('sz-zkm').location['x'],
                              driver.find_element_by_class_name('sz-zkm').location['y'])
                        # mouseRightClick(driver,driver.find_element_by_class_name('sz-zkm').location['x'],
                        #       driver.find_element_by_class_name('sz-zkm').location['y'])
                        # driver.execute_script(
                        #     "arguments[0].setAttribute('style', arguments[1]);",
                        #     driver.find_element_by_class_name('sz-zkm'),
                        #     "border: 1px solid red;"  # 边框border:2px; red红色
                        # )
                        # ActionChains(driver).move_to_element(
                        #     driver.find_element_by_class_name('sz-zkm')).context_click().perform()
                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        driver.find_element_by_class_name('sz-zkm').click()
                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        while (count < LOAD_PAGE_TIMEOUT):
                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            select2ZzkmContainer = driver.find_element_by_id('select2-zkm-container')
                            if select2ZzkmContainer != None:
                                break
                            # elements = driver.find_elements_by_class_name('select2-selection')
                            count = count + 1
                            if count == LOAD_PAGE_TIMEOUT:
                                log.e("等待select2-selection弹出框超时")
                                return 2
                            time.sleep(WHILE_WAIT_SLEEP)
                            # ActionChains(driver).move_to_element(
                            #     driver.find_element_by_class_name('sz-zkm')).click().perform()

                            driver.find_element_by_class_name('sz-zkm').click()
                        driver.find_element_by_id('select2-zkm-container').click()

                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        driver.find_element_by_class_name('select2-search__field').send_keys(detail.account_code)
                        hasBank = 1
                        count = 0
                        while (count < LOAD_PAGE_TIMEOUT):
                            if detail.account_code + '--' in driver.find_element_by_class_name(
                                    'select2-results__option').text:
                                driver.switch_to_active_element().send_keys(Keys.DOWN)
                                driver.switch_to_active_element().send_keys(Keys.ENTER)
                                break
                            count = count + 1
                            time.sleep(WHILE_WAIT_SLEEP)
                        driver.find_element_by_id('zkm_sub').click()
                    elif getFeatureCdByCode(template.kmCode) == 4 or getFeatureCdByCode(template.kmCode) == 5:  # 往来
                        count = 0
                        # ActionChains(driver).move_to_element(
                        #     driver.find_element_by_class_name('sz-wldw')).click().perform()
                        element = driver.find_element_by_css_selector('div[class*="sz-wldw"]')
                        driver.execute_script("arguments[0].click();", element)
                        # driver.find_element_by_class_name('sz-wldw').click()
                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        if hasBank == 1:
                            elements = driver.find_elements_by_class_name('select2-selection')
                            while (count < LOAD_PAGE_TIMEOUT):
                                time.sleep(ACTION_WAIT_SLEEP_LONG)
                                print('dengdai', count, len(elements))
                                if len(elements) == 2:
                                    break
                                elements = driver.find_elements_by_class_name('select2-selection')
                                count = count + 1
                                if count == LOAD_PAGE_TIMEOUT:
                                    log.e("等待select2-selection弹出框超时")
                                    return 2
                                time.sleep(WHILE_WAIT_SLEEP)
                            for i in range(len(elements)):
                                aria_labelledby = elements[i].get_attribute('aria-labelledby')
                                if aria_labelledby == 'select2-wldw-container':
                                    ActionChains(driver).move_to_element(elements[i]).click().perform()
                        else:
                            select2_selection = driver.find_element_by_class_name('select2-selection')
                            ActionChains(driver).move_to_element(
                                driver.find_element_by_class_name('select2-selection')).click().perform()

                        # select2_selection= WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_class_name('select2-selection'))
                        # ActionChains(driver).move_to_element(select2_selection).click().perform()
                        # driver.find_element_by_id('select2-wldw-container').click()
                        # WebDriverWait(driver, 10).until(
                        #     lambda driver: driver.find_element_by_id('select2-wldw-container')).click()

                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        driver.find_element_by_class_name('select2-search__field').send_keys(detail.partner_name)
                        time.sleep(ACTION_WAIT_SLEEP_LONG)
                        count = 0
                        while (count < LOAD_PAGE_TIMEOUT):
                            if detail.partner_name in driver.find_element_by_class_name(
                                    'select2-results__option').text:
                                driver.switch_to_active_element().send_keys(Keys.DOWN)
                                driver.switch_to_active_element().send_keys(Keys.ENTER)
                                break
                            count = count + 1
                            time.sleep(WHILE_WAIT_SLEEP)
                        driver.find_element_by_id('wldw_sub').click()
        currentImgIdOld = driver.get_cookie('current_img_id')['value']
        driver.find_element_by_id("remark").send_keys("selenium 录入")

        time.sleep(ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_id('save').click()

        time.sleep(ACTION_WAIT_SLEEP_LONG)
        count = 0
        while (count < LOAD_PAGE_TIMEOUT):

            currentImgIdNew = driver.get_cookie('current_img_id')['value']

            log.d('点击保存等待', count, 'currentImgIdNew', currentImgIdNew, 'currentImgIdOld', currentImgIdOld)
            if currentImgIdNew != currentImgIdOld:
                # print('currentImgIdNew', currentImgIdNew, 'currentImgIdOld', currentImgIdOld)
                log.i(documentIndex, '录入凭证成功', detail.document_id)
                break
            count = count + 1
            if count == LOAD_PAGE_TIMEOUT:
                log.e(documentIndex, '录入凭证保存等待超时', detail.document_id)
                return 3, '录入凭证保存等待超时'
            time.sleep(WHILE_WAIT_SLEEP)

        time.sleep(ACTION_WAIT_SLEEP_LONG)

    log.i('录入凭证结束')

    time.sleep(60)
    return 0


def addExpensesClaimSheer(driver):
    log.d('费用报销单')
    driver.get(HOST_THIRD + "/cs-third//third/expensesClaimSheer/list")
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/cs-third//third/expensesClaimSheer/list"):
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    count = 0

    while (count < 3):
        log.d('新增费用报销单', count)
        inputs = driver.find_elements_by_class_name('summary')
        inputs[0].send_keys('123123123')
        driver.switch_to_active_element().send_keys(Keys.TAB)
        driver.switch_to_active_element().send_keys("123123")
        driver.switch_to_active_element().send_keys(Keys.TAB)
        driver.switch_to_active_element().send_keys('1')
        driver.find_element_by_id('save_btn').click()
        countAlert = 0
        while (countAlert < LOAD_PAGE_TIMEOUT):
            msg = driver.find_element_by_class_name('bootbox-body')
            if msg.text == '保存成功':
                driver.switch_to_active_element().click()
                count = count + 1
                break
            if '失败' in msg.text:
                log.e("费用报销单保存失败")
                return 2
            if countAlert == LOAD_PAGE_TIMEOUT - 1:
                log.e("等待弹出框超时")
                return 2
            # log.w('等待弹出框', countAlert)
            countAlert = countAlert + 1
            time.sleep(WHILE_WAIT_SLEEP)

        time.sleep(1)
    log.d('费用报销单结束')

    return 0


def addPartner(driver, partnerName):
    log.d('新增往来单位')
    driver.get(HOST_THIRD + "/cs-third/con/contactsunit/contactsunitlist")
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        if (driver.current_url == HOST_THIRD + "/cs-third/con/contactsunit/contactsunitlist"):
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)

    # driver.find_element_by_id('company').click()
    # driver.find_element_by_id('people').click()
    driver.find_element_by_id('add').click()

    time.sleep(ACTION_WAIT_SLEEP_LONG)
    driver.find_element_by_id('partnerName').send_keys(partnerName)
    time.sleep(ACTION_WAIT_SLEEP_LONG)
    driver.find_element_by_id('contactFormBtn').click()

    time.sleep(ACTION_WAIT_SLEEP_LONG)
    count = 0
    while (count < LOAD_PAGE_TIMEOUT):
        names = driver.find_elements_by_class_name('kh-text')
        deletes = driver.find_elements_by_id('deleteContact')
        for index in range(len(names)):
            print(index, names[index].text, partnerName)
            if names[index].text == partnerName:
                log.d('新增往来单位结束')
                # deletes[index].click()
                # log.d('删除往来单位结束')
                return 0
        elementsError = driver.find_elements_by_class_name('error')
        if len(elementsError) == 2 and elementsError[1].text != '':
            log.e('新增往来单位失败', elementsError[1].text)
            break
        count = count + 1
        time.sleep(WHILE_WAIT_SLEEP)
    return 0


# def addExpensesClaimSheer(driver):
#     log.d('费用报销单')
#     driver.get(HOST_THIRD + "/cs-third//third/expensesClaimSheer/list")
#     count = 0
#     while (count < LOAD_PAGE_TIMEOUT):
#         if (driver.current_url == HOST_THIRD + "/cs-third//third/expensesClaimSheer/list"):
#             break
#         count = count + 1
#         time.sleep(WHILE_WAIT_SLEEP)
#     count = 0
#     while (count < 3):
#         inputs = driver.find_elements_by_class_name('summary')
#         inputs[0].send_keys('123123123')
#         driver.switch_to_active_element().send_keys(Keys.TAB)
#         driver.switch_to_active_element().send_keys("123123")
#         driver.switch_to_active_element().send_keys(Keys.TAB)
#         driver.switch_to_active_element().send_keys('1')
#         driver.find_element_by_id('save_btn').click()
#         count = count + 1
#     time.sleep(10)
#     log.d('费用报销单结束')
# return 0


def main():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=option)
    driver.set_window_size(window_size_w, window_size_h)
    driver.implicitly_wait(5)
    # driver.switch_to_active_element()
    ret = login(driver, 'lxhw', '12344321')
    if (ret != 0):
        print('登陆失败')
        return
    accountSetInfo = AccountSetInfo('companyName', 'taxidCode000000000', 1, 2018, 8, 1, '物流行业科目体系', '默认组', '伊文科技',
                                    '通用公式')
    # createAccount(driver, accountSetInfo)
    # time.sleep(ACTION_WAIT_SLEEP_LONG)
    # ret = toThird(driver, '新疆物流2', '123123123234234234')
    # ret = toThird(driver, '宜昌市西陵区艾垒商务咨询服务部', '91420502MA49877MX8')
    # if (ret != 0):
    #     print('进账簿失败', ret)
    #     return

    # time.sleep(ACTION_WAIT_SLEEP_LONG)
    # ret = addPartner(driver,'往来单位'+str(random.randint(1000,9999)))
    # if (ret != 0):
    #     print('添加往来单位失败', ret)
    #     return

    # time.sleep(ACTION_WAIT_SLEEP_LONG)
    # ret = addCertificateWithPartner(driver)
    # if (ret != 0):
    #     print('新增凭证失败', ret)
    #     return
    # time.sleep(ACTION_WAIT_SLEEP_LONG)

    ret = toCertificateInput(driver)
    if (ret != 0):
        time.sleep(60)
        log.e('凭证录入失败', ret)
    # ret = addExpensesClaimSheer(driver)
    # if (ret != 0):
    #     print('费用报销单失败', ret)
    # print('over')
    # time.sleep(ACTION_WAIT_SLEEP_LONG)
    time.sleep(5)
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.


def getFeatureCdByCode(code):
    if code.startswith('1002'):
        return 2
    if code in '122101' or code == '224102' or code == '224104':
        return 5
    if code in ['112101', '112102', '1122', '1123', '1131', '122102', '220101', '220102', '2202', '2203', '224103',
                '224105', '4001']:
        return 4
    return 1


if __name__ == "__main__":
    main()
    # print('cd',getFeatureCdByCode('100202'))
