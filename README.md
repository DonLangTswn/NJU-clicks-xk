简介：一个利用selenium的自动化补退选脚本工具，助你实现无痛连点补退选～

> 上次更新 README：2025.9.16
> 
> ❌8.25：**发现小土豆插件在选课时会报错**，因此`clicks-potato.py`似乎不可用了，建议暂时使用不依赖小土豆插件的`clicks-no-potato.py`，静待小土豆插件恢复……

### *写在前面*

1. 此脚本仅适用于补退选期间的**辅助工具**，不太适用于**抢**课哦
2. 使用期间请**关闭VPN**等网络系统代理（南大VPN除外），建议保持屏幕常亮**不睡眠**，否则容易异常终止
3. 🌟 建议**小土豆插件 + 收藏课程**结合使用
4. 提示「Got one! 」不一定是选中了，只是监测到有新课程弹出
5. 若要查看选课结果，请**不要**在脚本开启的Chrome中操作，建议在南大APP中查看

> **⚠️ 此脚本仅作为辅助工具，供学习交流使用。杜绝一切恶性竞争、恶意扰乱系统的行为！**

*\*欢迎 add issues，期待大神共同修改*✨

---

## 前置准备：

1. 支持 Windows、macOS、Linux 系统

2. 运行前请确保本机已下载 **Google Chrome** 浏览器

   > chrome 官网下载：https://www.google.com/chrome/index.html

3. 接下来打开解压的`xk`文件夹，修改`config.json`文件中的以下内容：

   * `UserId`后面改为自己的学号
   * `PassWd`后面改为选课系统的帐户密码
   * `Campus`后面改为所在的校区代码，仙林校区：`XL`，鼓楼校区：`GL`，苏州校区：`SZ`，浦口校区：`PK`
   
   如下图：
   
   ![./assets/配置.png](https://raw.githubusercontent.com/DonLangTswn/NJU-clicks-xk/main/assets/配置.png)



## 开始运行！

### 运行`clicks-no-potato`

> ⚠️小土豆插件故障时临时启用，建议在插件恢复正常时仍使用`click-potato.py`

脚本不依赖于小土豆插件，无需下载插件，直接通过南大选课网站页面进行，因此**无法在收藏页**进行筛选。无小土豆插件、直接在南大选课网站页面操作触发系统报错几率较高，因此建议刷新时间不要太短。

`clicks-no-potato`脚本会自动打开南大选课网站，你需要自己**手动点击验证码**，完成后点击 **“登录”**。之后脚本会根据用户指定，到相应的页面进行自动刷新、监测未满课程，并自动点击选择。

**运行方式**：

指令和`clicks-potato.py`大致相同：

```shell
python3 .\clicks-no-potato.py -c [列名] -t [刷新间隔]
# 默认：column = 'general', timeout = 1.2
python3 clicks-no-potato.py
```

* 列名：`-c` / `--column`，可选择**通识**（`general`）、**科学之光**（`science`）、**公选**（`public`）、**体育**（`sport`）

* 刷新间隔时间：`-t` / `--timeout`，≥ 0.6（s），建议在1s左右最稳定



### 运行`clicks-potato`

#### 配置脚本

1. 命令行运行`clicks-pre.py`（ 运行前需要**打开魔法**🪜）

   ```bash
   python3 clicks-pre.py
   ```

2. 程序会自动检测并添加所需的 python 依赖库，并自动下载/更新**最新的 Chrome WebDriver**

3. 一切准备就绪后，脚本会自动打开 google 的扩展商店并搜索小土豆插件（PotatoPlus），并自动点击“添加到chrome”

4. 在弹出来的窗口**点击确认“添加扩展程序”**，添加成功即可通过 `Ctrl+C` 终止运行程序

> 你也可以在弹出的 chrome 浏览器中手动搜索添加小土豆插件，不过一定要在脚本弹出的浏览器中添加；另外要确保前面的 python 依赖检测通过

![./assets/小土豆.png](https://raw.githubusercontent.com/DonLangTswn/NJU-clicks-xk/main/assets/小土豆.png)



#### 运行`clicks-potato`脚本

脚本依赖于小土豆插件，所以请先完成上一步配置

> 运行前请关闭魔法🪜（南大 VPN 除外）

`clicks-potato`脚本会自动打开南大选课网站，⚠️**第一次运行需要在页面打开“启用 PotatoPlus (Beta)”开关**。打开后，你需要自己手动点击验证码，完成后点击 **“登录”**。之后脚本会根据用户指定，到相应的页面进行自动刷新、监测未满课程，并自动点击选择。

![./assets/登录.png](https://raw.githubusercontent.com/DonLangTswn/NJU-clicks-xk/main/assets/登录.png)

💡由于选课网站自带的收藏页面没有「过滤已满」和「过滤冲突」选项，且公共、体育等页面常常有少人课、空课霸榜，所以推荐**小土豆 + 收藏页**的方法：先将所有想选的课添加到收藏，之后利用`clicks-potato`选择收藏页，进行自动化选课

**运行方式**：

```shell
python3 clicks-potato.py -c [列名] -t [刷新间隔]
# 默认：column = 'favorite', timeout = 1.2
python3 clicks-potato.py
```

* 列名：`-c` / `--column`，可选择**通识**（`general`）、**科学之光**（`science`）、**公选**（`public`）、**体育**（`sport`）和**收藏**（`favorite`）
* 刷新间隔时间：`-t` / `--timeout`，≥ 0.6（s），建议在1s左右最稳定

![./assets/运行.png](https://raw.githubusercontent.com/DonLangTswn/NJU-clicks-xk/main/assets/运行.png)
