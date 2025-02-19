简介：一个利用selenium的自动化补退选脚本工具，助你实现无痛连点抢课～

> 上次更新README：2025.2.19

### *写在前面*

1. 建议**小土豆插件 + 收藏课程**结合使用
2. 抢课期间请**关闭VPN**等网络系统代理
3. 后台运行时建议保持屏幕常亮**不睡眠**，否则容易异常终止
4. 提示「Got one! 」提示不一定是选中了，只是监测到有新课程弹出
5. 欢迎add issure，期待大神共同修改✨

---

### 前置准备：

1. 目前仅支持Windows系统

2. 运行前请确保已下载**Google Chrome**和的Google Chrome的**Web Driver**

   * 下载**Google Chrome**：

     > https://www.google.com/chrome/index.html

   * 下载Google Chrome的**Web Driver**：

     > https://googlechromelabs.github.io/chrome-for-testing/

     访问上面的WebDriver下载网址，看到“Stable”下面的支持的Google Chrome最低版本号

     ![.\assets\配置1.jpg](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E9%85%8D%E7%BD%AE1.jpg)

   * 打开自己的Google Chrome，点击“设置-关于Chrome”查看当前版本号是否已更新，即大于等于上面的版本号（一般点进去就会自动更新）

     ![.\assets\配置2.jpg](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E9%85%8D%E7%BD%AE2.jpg)

   * 找到自己的系统规格（win32 / win64）对应的**chromedriver**（注意⚠️是chromedriver，不是chrome也不是chrome-headless-shell ）

   * 下载得到的压缩包，提取压缩包里面的`chromedriver.exe`，添加至`xk`文件夹下的`webDriver`目录下

3. python依赖库需提前下载好～：

   命令行运行：

   ```shell
   pip3 install selenium
   pip3 install colorama
   ```

   > 如果仍然提示缺少库，就继续pip install ...即可

4. 接下来打开解压的`xk`文件夹（建议用vscode），修改`config.json`文件中的以下内容：

   * `UserId`后面改为自己的学号
   * `PassWd`后面改为自己选课系统的帐户密码

   如下图

   ![.\assets\配置3.png](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E9%85%8D%E7%BD%AE3.png)

### 开始运行！

在xk文件夹下打开命令行，输入:

```shell
python3 .\clicks_xk.py
```

如果看到屏幕上弹出来一个Chrome小窗，并加载进入了选课界面，则表示成功～：

![.\assets\运行1.png](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E8%BF%90%E8%A1%8C1.png)



#### 配置小土豆

🌟*建议**小土豆 + 收藏课程**结合使用*

1. 首先运行`clicks-pre.py`，这个脚本会自动打开google的插件商店并搜索小土豆插件（PotatoPlus），并点击下载，因此需要运行前手动**打开魔法**🪜
2. 在弹出来的窗口点击确认“添加扩展程序”，添加成功即可关闭窗口，并终止运行程序

![.\assets\小土豆.png](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E5%B0%8F%E5%9C%9F%E8%B1%86.png)

#### 运行clicks-potato（推荐）

`clicks-potato`脚本会自动打开南大选课网站，需要根据验证码信息在**命令行**手动输入验证码，之后脚本会根据用户指定，到相应的页面进行自动刷新、监测未满课程，并自动点击选择。

脚本依赖于小土豆插件，所以请先完成上一步配置

💡由于选课网站自带的收藏页面没有「过滤已满」和「过滤冲突」选项，且公共、体育页面常常有少人课、空课霸榜，所以推荐**小土豆 + 收藏**的方法：先将所有想选的课添加到收藏，之后利用`clicks-potato`选择收藏页，进行自动化选课

**运行方式**：

```shell
python3 .\clicks-potato.py -c [列名] -t [刷新间隔]
```

* 列名：`-c` / `--column`，可选择**公共**（`public`）、**体育**（`sport`）和**收藏**（`favorite`）
* 刷新间隔时间：`-t` / `--timeout`，≥ 0.6（s），建议在1s左右最稳定

![.\assets\运行2.png](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E8%BF%90%E8%A1%8C2.png)



#### 运行clicks-xk

`clicks_xk`脚本会自动打开南大选课网站，需要根据验证码信息在**命令行**手动输入验证码，之后脚本会根据用户指定，到相应的页面进行自动刷新、监测未满课程，并自动点击选择。

脚本不依赖于小土豆插件，直接通过南大选课网站页面进行，因此无法在收藏页进行筛选。

**运行方式**：

```shell
python3 .\clicks_xk.py -c [列名] -t [刷新间隔]
```

* 列名：`-c` / `--column`，可选择**公共**（`public`）、**体育**（`sport`）
* 刷新间隔时间：`-t` / `--timeout`，≥ 0.6（s），建议在1s左右最稳定

![.\assets\运行3.png](https://github.com/DonLangTswn/NJU-clicks-xk/blob/main/assets/%E8%BF%90%E8%A1%8C3.png)
