# 网易云音乐歌单下载
****
提交网易云的歌单链接或者ID，自动爬取音乐并同步到校内网
****

##说明：
这是学校内网计划的一部分，因为经常有同学听着广播站的歌，突然来了感觉，却不知道歌名(\*/ω＼*)。为了解决`今天早上广播站那歌叫什么名字啊`这样的问题，写了这个网易云音乐的爬虫，随便给我们的内网添加一些功能（教室电脑没有网络真麻烦）

本爬虫基于`python3`，前端使用了`flask`框架，做了简单的用户认证，毕竟不可能人人都提交链接吧，这个给广播站的同学先用用

值得注意的是，网易云付费音乐还是没有搞头，除了氪金别无他法，(｀・ω・´)你们就想天鹅屁吃。要是哪个小伙计愿意贡献VIP的话，咱们可以一起倒腾一个真正的网易云爬虫 (╹◡╹)ﾉ

爬虫下载音乐用到的api有两个，一个是网易官方：http://music.163.com/song/media/outer/url?id=xxx，一个是第三方的：https://api.imjad.cn/cloudmusic/。因为有api可用，所以绕过了解析音乐真实地址过程中参数的解密操作（省事不少）。但是网易那边有`反爬虫`机制，爬了一段时间可能IP被ban~

所以说啦，这个爬虫目前功能并不完善，但是~~应该~~后面我还会更新的~~吧？~~

##预览
![home](https://raw.githubusercontent.com/zaxtyson/netease_music_flask/master/png/home.png "主页")

![submit](https://raw.githubusercontent.com/zaxtyson/netease_music_flask/master/png/submit.png "提交页")

##食用方法
1.安装依赖库：`requests`、`BeautifulSoup`、`Flask`
```
pip3 install requests bs4 flask
```
如果安装过程有问题请检查是否有管理员权限，其他问题自己解决


2.配置`config.ini`
```ini
[flask]
PORT = 5000  # 监听的端口号，记得防火墙放行
DEBUG = false  # 调试模式，正式服务时关闭
LISTEN_IP = 127.0.0.1  # 监听的地址，0.0.0.0表示监听全部网卡，127.0.0.1只监听本地网卡

[spider]
SAVE_PATH = ./temp  # 爬虫音乐保存路径

[user]
test = root   # 这里设置用户和密码，格式：用户名 = 密码
```


3.运行爬虫
```
python3 run.py
```
如果想让爬虫作为后台服务，linux系统使用
```ini
nohup python3 run.py &
```
或者添加计划任务
```ini
crontab -e
```

Windows系统请把`run.py`重命名为`run.pyw`，然后按Win+X，打开`计算机管理` > `计划任务程序`，将`run.pyw`加入计划任务，配置自动启动