# coding=utf-8
import json
import os
import re
from configparser import ConfigParser
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup

config = ConfigParser()
config.read("config.ini")

SAVE_PATH = config.get("spider", "SAVE_PATH")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}


class MusicNeedPayError(Exception):
    """下载付费音乐时错误"""
    pass


class GetMusicTitleError(Exception):
    """获取音乐标题时发生错误"""
    pass


class AntiSpiderError(Exception):
    """网易反爬虫机制导致的错误"""

    def __init__(self, msg):
        self.msg = msg


def get_music(url) -> bin:
    """官方api获取音乐文件"""
    api = 'http://music.163.com/song/media/outer/url?id='  # 官方的，自带反爬虫特效呃呃
    music_id = re.search('.*id=([0-9]+)', url, re.I).group(1)
    full_url = api + music_id

    try:
        music = requests.get(full_url).content
    except Exception:
        return None

    if len(music) < 1024:  # 被网易反爬虫机制发现，不返回错误信息
        raise AntiSpiderError(music.decode("utf-8"))
    if len(music) < 1024 * 200:  # 下载付费音乐错误，返回404页面，大小大概100kb
        raise MusicNeedPayError
    else:
        return music


def get_music2(url) -> bin:
    """第三方api爬取音乐"""
    api = 'https://api.imjad.cn/cloudmusic/?type=song&br=320000&id='  # 第三方，作者说不要用来做爬虫来着
    music_id = re.search('.*id=([0-9]+)', url, re.I).group(1)
    full_url = api + music_id
    msg = requests.get(full_url).text
    url = json.loads(msg)["data"][0]["url"]

    if not url:
        raise MusicNeedPayError
    try:
        music = requests.get(url).content
    except Exception:
        return None
    return music


def get_music_title(url) -> str:
    """提取某一首音乐的标题"""
    url = url.replace("#/", "")
    try:
        html = requests.get(url, headers=HEADERS).text
        title = re.search('<em class="f-ff2">(.*)</em>', html, re.IGNORECASE).group(1)
    except Exception:
        raise GetMusicTitleError
    return title


def get_music_list(playlist_url) -> list:
    """获取音乐列表中所有音乐的id和标题"""
    playlist_url = playlist_url.replace("#/", "")
    html = requests.get(playlist_url, headers=HEADERS).text
    soup = BeautifulSoup(html, 'lxml')
    find_list = soup.find('ul', class_="f-hide").find_all('a')

    music_list = []
    for a in find_list:
        music_id = a['href'].replace('/song?id=', '')
        music_title = a.text
        music_list.append({'id': music_id, 'title': music_title})
    return music_list  # 返回 [{'id':123, 'title':'xxxx'},{'id':456, 'title':'xxxx'}, ... ]


def get_all_title(playlist_url) -> list:
    """只获取整个列表所以音乐的名字"""
    data = get_music_list(playlist_url)
    return [i["title"] for i in data]  # 返回 ['xxx', 'xxxx', ...]


def down_music(url, path=SAVE_PATH):
    """下载音乐到指定目录"""
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        title = get_music_title(url)
    except GetMusicTitleError:
        print("无法获取歌曲标题")
        title = 'null'

    print("开始下载：{}".format(title))

    try:
        full_path = path + os.sep + title + '.mp3'
        with open(full_path, 'wb') as f:
            f.write(get_music(url))
    except MusicNeedPayError:
        print("下载失败：{} 为收费歌曲，无法下载 !!!".format(title))
    except AntiSpiderError as e:
        print("下载失败：受到网易反爬虫机制阻止,原因：{}".format(e))
    except Exception as e:
        print("下载失败：下载过程中发生其他错误 {}".format(e))


def down_music_list(music_list_url, path=SAVE_PATH):
    """下载列表中所有音乐"""
    music_list = get_music_list(music_list_url)
    for music in music_list:
        url = 'https://music.163.com/#/song?id=' + music['id']
        down_music(url, path)


def run(url):
    """新开一个进程开始爬取"""
    t = Process(target=down_music_list, args=(url,))
    t.start()


if __name__ == '__main__':
    pass
    # url = 'https://music.163.com/#/song?id=28445778'
    # music_list = 'https://music.163.com/#/playlist?id=2246999955'
    # down_music(url)
    # down_music_list(music_list)
