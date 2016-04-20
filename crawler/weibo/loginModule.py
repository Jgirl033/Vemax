#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-3-11 上午10:49
    @function:实现微脉登陆
"""
import urllib
import urllib2
from mobileWeiboModule import MobileWeibo
import sys
reload(sys)
sys.setdefaultencoding('utf8')


headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class Login(MobileWeibo):
    def __init__(self):
        MobileWeibo.__init__(self)

    def login(self, uname, pwd, verification_code=None):
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
    m = Login()
    username = raw_input("请输入用户名：")
    password = raw_input("请输入密码：")
    print m.login(username, password)
