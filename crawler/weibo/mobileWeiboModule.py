#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-3-13 上午1:05
    @function:线下爬取数据
"""
import cookielib
import re
import urllib
import urllib2
from init import globalModule


headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class MobileWeibo:  # 模拟登陆
    def __init__(self):
        self.cj = cookielib.LWPCookieJar()
        # if cookie_filename is not None:
        #     self.cj.load(cookie_filename)
        # 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        # 创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        self.opener = urllib2.build_opener(self.cookie_processor,
                                           urllib2.HTTPHandler)  # 将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起
        urllib2.install_opener(self.opener)

        self.host_url = ''
        self.url = ''
        self.vk = ''
        self.backurl = ''
        self.rand = ''
        self.password = ''
        self.img = ''
        self.cap = ''

    def get_host_url(self):
        host_url = "http://weibo.cn/pub/"
        url_login_request = urllib2.Request(host_url, headers=headers)
        response = urllib2.urlopen(url_login_request)
        text = response.read()
        pattern = re.compile('<a href=\'(http://login.weibo.cn/login/?.*?)\'>登录</a>')
        self.host_url = re.search(pattern, text).group(1)

    def get_args(self, uname='verification_code'):
        self.get_host_url()
        args_request = urllib2.Request(self.host_url, headers=headers)
        response = urllib2.urlopen(args_request)
        text = response.read()

        url_pattern = re.compile("<form action=\"(.*?)\" method=\"post\">", re.S)
        self.url = 'http://login.weibo.cn/login/' + re.search(url_pattern, text).group(1)

        vk_pattern = re.compile('<input type="hidden" name="vk" value="(.*?)" />')
        self.vk = re.search(vk_pattern, text).group(1)

        backurl_pattern = re.compile("<input type=\"hidden\" name=\"backURL\" value=\"(.*?)\" />")
        self.backurl = re.search(backurl_pattern, text).group(1)

        rand_pattern = re.compile('<form action="\?rand=(.*?)&')
        self.rand = re.search(rand_pattern, text).group(1)

        pwd_pattern = re.compile('<input type="password" name="(.*?)" size="30" />')
        self.password = re.search(pwd_pattern, text).group(1)

        cap_pattern = re.compile('<input type="hidden" name="capId" value=\"(.*?)\" />')
        self.cap = re.search(cap_pattern, text).group(1)

        img_pattern = re.compile('<img src="(.*?)" alt="请打开图片显示" />')
        self.img = re.search(img_pattern, text).group(1)
        project_path = globalModule.get_project_path()
        img_path = project_path + "/static/identify/" + uname + ".png"
        urllib.urlretrieve(self.img, img_path)

    def login(self, uname, pwd, verification_code=None):
        self.get_args(uname)

        verification_code = raw_input("请输入验证码：")

        post_data = {
            "mobile": uname,
            str(self.password): pwd,
            'code': verification_code,
            'submit': "登录",
            'remember': "checked",
            'backURL': self.backurl,
            'vk': self.vk,
            'tryCount': '',
            'capId': self.cap,
            'rand': self.rand
        }
        post_data = urllib.urlencode(post_data)

        request = urllib2.Request(self.url, post_data, headers)
        response = urllib2.urlopen(request)
        text = response.read()
        return text


if __name__ == "__main__":
    m = MobileWeibo()
    username = raw_input("请输入用户名：")
    password = raw_input("请输入密码：")
    print m.login(username, password)
