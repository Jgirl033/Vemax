# coding:utf-8
import urllib2
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class BigV:  # 好友关注的大v,使用非本人账号爬取
    def __init__(self, uid):
        self.uid = uid

    def get_bigV(self):
        """
        获取关注的大V的源代码文本
        :return: 大V源代码文本列表
        """
        list_bigV = []
        for i in range(1, 2):
            url = 'http://weibo.cn/' + str(self.uid) + '/follow?page=' + str(i)  # 好友关注
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            print page
            pattern = re.compile('top"><a href=".*?>(.*?table)')
            list_bigV = re.findall(pattern, page)
        for item in list_bigV:
            print item
        return list_bigV

    def get_bigV_uid(self):
        """
        获取关注的大V的uid列表
        :return: 大V的uid列表
        """
        list_bigV_uid = []
        list_bigV_text = BigV(self.uid).get_bigV()
        for item in list_bigV_text:
            pattern = re.compile('(.*?)</a>.*?alt="V".*?(粉丝.*?)<br/>.*?uid=(.*?)&')  # （大V的名字）和（大V的ID）
            list_bigV_name_uid = re.findall(pattern, item)
            if len(list_bigV_name_uid) > 0:
                list_bigV_uid.append(list_bigV_name_uid[0][2])

        return list_bigV_uid

    def get_bigV_name(self):
        """
        获取关注的大V的name列表
        :return:返回大V的name列表
        """
        list_bigV_name = []
        list_bigV_text = BigV(self.uid).get_bigV()
        for item in list_bigV_text:
            pattern = re.compile('(.*?)</a>.*?alt="V".*?(粉丝.*?)<br/>.*?uid=(.*?)&')  # （大V的名字）和（大V的ID）
            list_bigV_name_uid = re.findall(pattern, item)
            if len(list_bigV_name_uid) > 0:
                list_bigV_name.append(list_bigV_name_uid[0][0])
        return list_bigV_name
