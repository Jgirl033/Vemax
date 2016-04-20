# coding:utf-8
import re
import urllib2
import time
import random

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class TagPage:  # 爬取好友标签及关注的大V的标签
    def __init__(self, uid):
        self.uid = uid

    def get_tag_page(self):
        url = 'http://weibo.cn/account/privacy/tags/?uid=' + str(self.uid)  # 好友标签所在页面
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        webpage = response.read()
        time.sleep(random.randint(3, 5))
        return webpage


class UserTag:  # 获取资料,使用非本人账号登录
    def __init__(self, uid):
        self.page = TagPage(uid).get_tag_page()
        self.uid = uid

    def get_tag(self):
        """
        爬取微博标签
        :return:   返回标签集
        """
        pattern = re.compile('&amp;stag=1">(.*?)</a>')
        list_tag = re.findall(pattern, self.page)
        str_tag = ','.join(list_tag)
        return str_tag


class BaiduTag:
    def __init__(self, item):
        self.item = item

    def get_baidu_tag(self):
        set_tag = list()
        try:
            url = 'https://www.baidu.com/s?wd=' + str(self.item)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            pattern = re.compile('<a href="(http://www.baidu.com/link.*?)".*?百度百科')
            list_baike_url = re.findall(pattern, page)
            str_baike_url = ''.join(list_baike_url)  # 百科链接

            req = urllib2.Request(url=str_baike_url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            pattern = re.compile('<s..n class="taglist">(.*?)</s..n>', re.S)
            list_tag = re.findall(pattern, page)

            for item in list_tag:
                pattern0 = re.compile('<.*?>')
                tag = re.sub(pattern0, '', item.strip())
                set_tag.append(tag)  # 从百科爬到的标签集
        except ValueError:
            pass
        return set_tag
