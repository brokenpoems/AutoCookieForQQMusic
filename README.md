# AutoCookieForQQMusic

Get Cookie From QQMusic Website Without Opening browser

# 运行前置

GoogleChrome(已在Windows10以及CentOS做测试)或Chromium(未测试)

# 运行环境:

1. Python 3(3.6+为最佳)
2. Python的一些库:

- `selenium`(`Windows 10:4.1.3,CentOS 7:3.141.0`)
- `pyzbar`(`Windows 10 & CentOS 7:0.1.9`)
- `qrcode`(`Windows 10 & CentOS 7:7.3.1`)
- `qrcode-terminal`(`Windows 10 & CentOS 7:0.8`)
- `Pillow`(`Windows 10:9.1.0,CentOS 7:8.4.0`)

3. `Chrome` 以及对应的 `ChromeDriver` (`Windows 10:100.0.4896.60,CentOS 7:99.0.4844.84`)
   CentOS 7下的Chrome安装
   
   ```bash
   wget http://dl.google.com/linux/chrome/rpm/stable/x86_64//google-chrome-stable-99.0.4844.84-1.x86_64.rpm
   sudo yum localinstall google-chrome-stable-99.0.4844.84-1.x86_64.rpm
   ```
   
   CentOS 7下ChromeDriver安装:我直接`yum install chromedrive`了
   Windows 10我直接安装普通Chrome然后添加`Path`了
   ChromeDriver的话是用`https://chromedriver.storage.googleapis.com`
   找到对应版本安装
4. CentOS 7还要安装zbar库
   
   ```bash
   sudo yum install zbar-devel 
   sudo yum install zbar
   ```

# ToDo:

* [ ] 优化扫码的判断
* [ ] 浏览器是否显示的配置
* [ ] 引入配置文件
* [ ] 使用Action编译

# bug?

请提交[New Issue](https://github.com/brokenpoems/AutoCookieForQQMusic/issues/new/choose)或[博客反馈](https://brokenpoems.cf/archives/65/)
