# codeing=utf-8
# Package
# python 自带库
import os
import sys
import time
import platform
import configparser
# 第三方库
import qrcode
import qrcode_terminal
from PIL import Image
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.common.by import By

debug = False

# 全局变量
loginmode = 0
configuse = False
headless = False
fileuse = False
qqaccout = ""
qqcipher = ""
filename = ""
config = configparser.ConfigParser()
chrome_options = webdriver.ChromeOptions()


# Debug用函数,输出python表达式字符串和用户向字符串以及数据类型或者输出函数名
def output(value="", funcname=""):
    global debug
    if debug:
        print(funcname)
        print(repr(value))
        print(str(value))
        print(type(value))
    return


# 载入配置文件
def Load_config():
    global loginmode, configuse, headless
    global qqaccout, qqcipher, fileuse, filename
    output(funcname="Load_config")
    config.read('config.ini', encoding='utf-8')
    if config.has_section('config'):
        if(config.has_option('config', 'loginmode')):
            loginmode = config.getint('config', 'loginmode')
        if(config.has_option('config', 'configuse')):
            configuse = config.getboolean('config', 'configuse')
        if(config.has_option('config', 'headless')):
            headless = config.getboolean('config', 'headless')
        if(config.has_option('config', 'qqaccout')):
            qqaccout = config.get('config', 'qqaccout')
        if(config.has_option('config', 'qqcipher')):
            qqcipher = config.get('config', 'qqcipher')
        if(config.has_option('config', 'fileuse')):
            fileuse = config.getboolean('config', 'fileuse')
        if(config.has_option('config', 'filename')):
            filename = config.get('config', 'filename')


# 载入浏览器配置
def ChromeSetting():
    output(funcname="ChromeSetting")
    global headless
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")


# 安全输入数字,避免输入字符串报错
def input_t(str):
    output(funcname="input_t")
    src = input(str)
    while not src.isdigit():
        src = input()
    return eval(src)


# 手动输入配置
def chooce_mode():
    output(funcname="chooce_mode")
    global loginmode, headless, fileuse
    global qqaccout, qqcipher, filename
    loginmode = 0
    headless = fileuse = False
    qqaccout = qqcipher = filename = ""
    # 登录模式 1.QQ账号密码 2.QQ扫码 3.微信扫码
    while (loginmode != 1 and loginmode != 2 and loginmode != 3):
        loginmode = input_t("请选择登录方式:\n1.QQ账号密码(不推荐) 2.QQ扫码 3.微信扫码\n")
        # output(loginmode)
        if (loginmode != 1 and loginmode != 2 and loginmode != 3):
            print("输入错误,请重新输入")
    if(loginmode == 1):
        print("您选择了QQ账号密码登陆")
        qqaccout = input("请输入账号:\n")
        output(value=qqaccout)
        qqcipher = input("请输入密码：\n")
        output(value=qqcipher)

    # 浏览器显示方式 1.无窗口 2.有窗口
    tempint = 0
    while (tempint != 1 and tempint != 2):
        tempint = input_t("请选择浏览器显示方式:\n1.无窗口 2.有窗口\n")
        if (tempint != 1 and tempint != 2):
            print("输入错误,请重新输入")
    if tempint == 1:
        headless = True
    else:
        headless = False

    # 文件输出 1.输出到文件 2.直接输出
    tempint = 0
    while (tempint != 1 and tempint != 2):
        tempint = input_t("成功获取后是否输出到文件:\n1.输出到文件 2.直接输出\n")
        if (tempint != 1 and tempint != 2):
            print("输入错误,请重新输入")
    if tempint == 1:
        fileuse = True
    else:
        fileuse = False
    if(fileuse):
        print("您选择了输出到文件")
        filename = input("请输入输出文件名:\n")
        output(value=filename)
    return


# 0 账号或密码错误 1 成功 2 异地登陆
def login_qq_account():
    flag = 1
    global cookie, qqaccout, qqcipher
    # 生成浏览器
    driver = webdriver.Chrome(options=chrome_options)
    code = driver.get("https://y.qq.com/")
    print("打开网页中")
    driver.find_element(By.CLASS_NAME, "top_login__link").click()
    print("登陆中")
    time.sleep(5)
    # 自动输入账号密码
    driver.switch_to.frame("login_frame")
    driver.switch_to.frame("ptlogin_iframe")
    driver.find_element(By.ID, "switcher_plogin").click()
    driver.find_element(By.ID, "u").click()
    driver.find_element(By.ID, "u").send_keys(qqaccout)
    driver.find_element(By.ID, "p").click()
    driver.find_element(By.ID, "p").send_keys(qqcipher)
    driver.find_element(By.ID, "p").send_keys('\n')
    # driver.switch_to_default_content()
    time.sleep(3)
    # 异地登陆 & 账密错误判断
    if(len(driver.find_elements(By.ID, "qlogin")) != 0):
        str = driver.find_element(By.ID, "qlogin").get_attribute("style")
        if(str == "display: block;"):
            flag = 2
            # 异地登陆
        else:
            # 账号密码错误
            flag = 0
    cookie = driver.get_cookies()
    driver.quit()
    return flag


# 输出二维码
def outputqrcode(driver):
    driver.get_screenshot_as_file("scanf.png")
    barcodes = decode(Image.open('./scanf.png'))
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")
    # print(barcode_url)
    if(platform.system() == 'Windows'):
        img = qrcode.make(barcode_url)
        img.save("qrcode.png")
        os.startfile("qrcode.png")
        print("请扫描打开的图片")
    else:
        qrcode_terminal.draw(barcode_url)
        print("请扫描输出的二维码")
    sys.stdout.flush()
    os.remove("scanf.png")
    return


# True 扫码成功 False 扫码失败
def login_qq_qrcode():
    global cookie
    flag = 0
    # 生成浏览器
    driver = webdriver.Chrome(options=chrome_options)
    print("打开网页中")
    driver.get("https://y.qq.com/")
    print("获取二维码中")
    driver.find_element(By.CLASS_NAME, "top_login__link").click()
    time.sleep(5)
    driver.switch_to.frame("login_frame")
    driver.switch_to.frame("ptlogin_iframe")
    # 用户扫码
    url = driver.find_element(By.ID, "qrlogin_img").get_attribute("src")
    outputqrcode(driver)
    while(driver.find_element(By.ID,
                              "qrlogin_step2").get_attribute(
            "style").find("display: block;") == -1):
        if(url != driver.find_element(By.ID,
                                      "qrlogin_img").get_attribute("src")):
            url = driver.find_element(
                By.ID, "qrlogin_img").get_attribute("src")
            outputqrcode(driver)
    print("扫码成功!请在手机上确认登陆")
    # ToDo : 判断用户取消扫码(页面无法提供)
    while flag != 1 and flag != 2:
        flag = input_t("已确认?1.是 2.否(重新开始)\n")
    time.sleep(3)
    cookie = driver.get_cookies()
    driver.quit()
    if flag == 1:
        return True
    else:
        return False


# True 扫码成功 False 扫码失败
def login_wechat():
    # 生成浏览器
    global cookie
    flag = 0
    driver = webdriver.Chrome(options=chrome_options)
    print("打开网页中")
    driver.get("https://y.qq.com/")
    driver.find_element(By.CLASS_NAME, "top_login__link").click()
    print("获取二维码中")
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "微信登录").click()
    driver.switch_to.frame("_login_frame_wechat_")
    url = driver.find_element(
        By.CLASS_NAME, "web_qrcode_img").get_attribute("src")
    outputqrcode(driver)
    while driver.find_element(By.ID, "wx_after_scan").get_attribute(
            "style") == "display: none;":
        if(url != driver.find_element(
                By.CLASS_NAME, "web_qrcode_img").get_attribute("src")):
            url = driver.find_element(
                By.CLASS_NAME, "web_qrcode_img").get_attribute("src")
            outputqrcode(driver)
    print("扫码成功!请在手机上确认登陆")
    while flag != 1 and flag != 2:
        flag = input_t("已确认?1.是 2.否(重新开始)\n")
        # output(flag)
    time.sleep(3)
    cookie = driver.get_cookies()
    driver.quit()
    if flag == 1:
        return True
    else:
        return False


# 登陆 True 成功 False 失败
def login():
    global loginmode
    flag = 0
    if loginmode == 1:
        flag = login_qq_account()
        if(flag == 2):
            print("您的账号异地登陆,请更换登陆方式")
            return False
        elif flag == 0:
            print("账号或密码错误,请检查后重新开始")
            return False
    elif loginmode == 2:
        if not login_qq_qrcode():
            return False
    elif loginmode == 3:
        if not login_wechat():
            return False
    return True


# 输出cookie
def outputcookie():
    global fileuse, filename
    if fileuse:
        outputfile = open(filename, "w")
    cookie.reverse()
    for element in cookie:
        if fileuse:
            print(element['name'], '=', element['value'],
                  end=';', file=outputfile)
        else:
            print(element['name'], '=', element['value'], end=';')
    if not fileuse:
        print("")



# 主函数
def main():
    output(funcname="main")
    Load_config()
    if(not configuse):
        chooce_mode()
    ChromeSetting()
    global loginmode, headless, fileuse
    global qqaccout, qqcipher, filename
    output(loginmode)
    output(headless)
    output(fileuse)
    output(qqaccout)
    output(qqcipher)
    output(filename)
    if(login()):
        outputcookie()
    #ConfigParserObject.write(open(filename, 'w'))


if __name__ == '__main__':
    main()
