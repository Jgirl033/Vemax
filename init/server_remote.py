#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-3-24 下午3:43
    @function:负责启动爬取已注册的用户的好友源代码的爬虫系统,部署在阿里云
"""
import urllib
import urllib2
from crawler.relation.friendModule import RealFriend, CloseFriend, MessagePage
from init.globalModule import is_start_crawler
from vemax.models import Friend

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


def start_register_crawler(uid):
    print u'开始爬取用户：' + uid
    dict_message_page = MessagePage.get_message_page()
    dict_message_page['uid'] = uid
    real_friend = RealFriend.get_real_friend()
    close_friend = CloseFriend.get_close_friend(real_friend, dict_message_page)

    url = 'http://127.0.0.1:8008/friend_analyse'
    post_data = {
        'uid': uid,
        'close_friend': close_friend
    }
    post_data = urllib.urlencode(post_data)

    request = urllib2.Request(url, post_data, headers)
    response = urllib2.urlopen(request)
    text = response.read()
    if text == 'success':
        print 'success!'
    else:
        print 'fail!'

if __name__ == "__main__":
    while True:
        if is_start_crawler() == 0:
            pass
        else:
            for item in is_start_crawler():
                if Friend.objects.filter(uid=item.uid).count() == 0:
                    if item.is_register is False:
                        pass
                    else:
                        start_register_crawler(item.uid)
                else:
                    pass

