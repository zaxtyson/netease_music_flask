# coding=utf-8
from configparser import ConfigParser
from time import strftime

from flask import Flask, render_template, request

from netease import run, get_all_title

app = Flask(__name__)
config = ConfigParser()
config.read("config.ini")

authority = dict(config.items("user"))  # 从配置文件读取用户和密码


@app.route('/submit', methods=['GET', 'POST'])
def result():
    data = request.form

    if not data:  # 非登陆用户
        status = "非法访问"
        info = "请不要直接访问本地址！\n\n你应该返回歌单提交页,输入相应信息后提交"
        return render_template('submit.html', info=info, status=status)

    if data["user"] not in authority.keys():
        status = "无访问权限"
        info = "用户名：{}\n\n该用户没有得到官方认证\n\n本页面不提供外部用户注册\n\n需要账号请加群找群主或管理".format(data["user"])
        return render_template('submit.html', info=info, status=status)

    if data["passwd"] != authority[data["user"]]:
        status = "密码错误"
        info = "你好{}，你的密码错额~\n\n如果忘记密码，请在QQ联系群主或管理".format(data["user"])
        return render_template('submit.html', info=info, status=status)

    # 合法用户
    url = data["url"]
    if url.isdigit():  # 用户只提交歌单ID
        print("=========================")
        url = "https://music.163.com/#/playlist?id=" + url

    run(url)  # 开始爬取

    status = "提交成功"
    info = """提交用户:{0}\n提交时间:{1}\n歌单链接:{2}\n歌曲列表:\n> {3}\n
            """.format(data["user"], strftime("%Y-%m-%d %X"), url,
                       "\n> ".join(get_all_title(url))
                       )
    return render_template('submit.html', status=status, info=info)


@app.route('/')
def login():
    return render_template('index.html')


# 开启使用url直接访问文件内容，仅测试时开启
# import os
# from flask import make_response
# @app.route('/<path>')
# def today(path):
#     base_dir = os.path.dirname(__file__)
#     resp = make_response(open(os.path.join(base_dir, path)).read())
#     resp.headers["Content-type"] = "application/json;charset=UTF-8"
#     return resp


if __name__ == '__main__':
    debug = config.getboolean("flask", "DEBUG")
    port = config.getint("flask", "PORT")
    ip = config.get("flask", "LISTEN_IP")
    app.run(debug=debug, port=port, host=ip)
