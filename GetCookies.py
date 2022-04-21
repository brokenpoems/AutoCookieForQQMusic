# codeing=utf-8
# Package

import os
import sys
import time
import platform

import qrcode
import qrcode_terminal
from PIL import Image
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.common.by import By


# 全局变量
chrome_options = webdriver.ChromeOptions()
mode = 0
disable = False
cookie = []


# 选择工作模式:0 无窗口 1 有窗口(未完成,因为无法判断用户是否能使用窗口,所以默认无窗口)
def chooce_workmode():
    global chrome_options
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    return


# Debug用函数,输出python表达式字符串和用户向字符串以及数据类型
def output(value):
    print(repr(value))
    print(str(value))
    print(type(value))
    return


# 安全输入数字,避免输入字符串报错
def input_t(str):
    src = input(str)
    while not src.isdigit():
        src = input()
    return eval(src)


# 选择登陆方式 1 qq账号密码 2 qq扫码 3 微信扫码
# disable用于判断qq账号是否异地登陆
def chooce_mode():
    global mode, disable
    mode = 0
    while ((mode == 1 and disable == True)
           or (mode != 1 and mode != 2 and mode != 3 and mode != 4)):
        if(disable):
            mode = input_t("请选择登录方式:\n1.QQ账号密码(已禁用) 2.QQ扫码 3.微信扫码 4.退出\n")
            # output(mode)
        else:
            mode = input_t("请选择登录方式:\n1.QQ账号密码(不推荐) 2.QQ扫码 3.微信扫码 4.退出\n")
            # output(mode)
        if ((mode == 1 and disable == True)
                or (mode != 1 and mode != 2 and mode != 3 and mode != 4)):
            print("输入错误,请重新输入")
    return


# 0 账号或密码错误 1 成功 2 异地登陆
def login_qq_account(account, cipher):
    flag = 1
    global cookie
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
    driver.find_element(By.ID, "u").send_keys(account)
    driver.find_element(By.ID, "p").click()
    driver.find_element(By.ID, "p").send_keys(cipher)
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


# 1 扫码成功 2 扫码失败
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
        # output(flag)
    time.sleep(3)
    cookie = driver.get_cookies()
    driver.quit()
    return flag


# 1 扫码成功 2 扫码失败
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
    return flag


# 登陆 True 成功 False 失败
def login():
    # print("login func")
    global mode, disable
    flag = 0
    if mode == 1:
        account = input("请输入账号:\n")
        # output(account)
        cipher = input("请输入密码：\n")
        # output(cipher)
        flag = login_qq_account(account, cipher)
        while(flag != 1):
            if(flag == 2):
                print("您的账号异地登陆,请更换登陆方式")
                sys.stdout.flush()
                disable = True
                return False
            else:
                print("账号或密码错误")
            account = input("请输入账号:\n")
            # output(account)
            cipher = input("请输入密码：\n")
            # output(cipher)
            flag = login_qq_account(account, cipher)
    elif mode == 2:
        if login_qq_qrcode() != 1:
            return False
    elif mode == 3:
        if login_wechat() != 1:
            return False
    elif mode == 4:
        return True
    return True


# 输出cookie
def outputcookie(flag, file=""):
    if flag == 1:
        outputfile = open(file, "w")
    cookie.reverse()
    for element in cookie:
        if flag == 1:
            print(element['name'], '=', element['value'],
                  end=';', file=outputfile)
        else:
            print(element['name'], '=', element['value'], end=';')
    if flag != 1:
        print("")

#主函数
def main():
    # print("main func")
    chooce_workmode()
    chooce_mode()
    while(not login()):
        chooce_mode()
    if mode != 4:
        flag = input_t("cookie已获取,是否输出到文件(1.是 2.否)\n")
        if flag == 1:
            file = input("请输入文件名:\n")
            outputcookie(flag, file)
        else:
            outputcookie(flag)


if __name__ == '__main__':
    main()
