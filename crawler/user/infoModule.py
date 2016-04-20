# coding:utf-8

import re
import urllib2
import time
import random
from tagModule import UserTag

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class InfoPage:  # 获取资料页面源代码
    def __init__(self, uid):
        self.uid = uid

    def get_info_page(self):
        url = 'http://weibo.cn/' + str(self.uid) + '/info'
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        webpage = response.read()
        time.sleep(random.randint(3, 5))  # 减缓爬虫速度
        return webpage


class UserMessage:  # 获取资料,使用非本人账号登录
    def __init__(self, uid):
        self.page = InfoPage(uid).get_info_page()
        self.uid = uid

    def get_name(self):  # 用户昵称
        pattern = re.compile('<div class="c">昵称:(.*?)<br/>')
        list_name = re.findall(pattern, self.page)
        username = ''.join(list_name)
        return username

    def get_sex(self):  # 性别
        pattern = re.compile('性别:(.*?)<br/>')
        list_sex = re.findall(pattern, self.page)
        sex = ''.join(list_sex)
        return sex

    def get_feel(self):  # 感情状况
        pattern = re.compile('<div class="c">感情状况：(.*?)<br/>')
        list_feel = re.findall(pattern, self.page)
        feel = ''.join(list_feel)
        return feel

    def get_img_url(self):  # 头像
        pattern = re.compile('<div class="c"><img src="(.*?)" alt="头像"')
        if re.search(pattern, self.page):
            img_url = re.search(pattern, self.page).group(1)
        else:
            img_url = ''
        return img_url

    def get_intro(self):  # 简介
        """
        爬取简介
        :return:返回简介（str）
        """
        pattern = re.compile('简介<?/?a?>?:(.*?)<br/>')
        list_intro = re.findall(pattern, self.page)
        intro = ','.join(list_intro)
        return intro

    def get_address(self):  # 地区
        pattern = re.compile('地区<?/?a?>?:(.*?)<br/>')
        list_address = re.findall(pattern, self.page)
        address = ','.join(list_address)
        return address

    def get_birthday(self):  # 生日
        pattern = re.compile('生日.*?:(.*?)<br/>')
        list_birthday = re.findall(pattern, self.page)
        birthday = ''.join(list_birthday)
        return birthday

    def get_cer_message(self):  # 认证信息
        pattern = re.compile('认证信息<?/?a?>?：(.*?)<br/>')
        list_cer_message = re.findall(pattern, self.page)
        cer_message = ','.join(list_cer_message)
        return cer_message

    def get_study_experience(self):  # 学习经历
        pattern = re.compile('学习经历</div><div class="c">·(.*?)<br/></div>')
        list_study = re.findall(pattern, self.page)
        str_study = ''
        for item in list_study:
            item = item.replace('&nbsp', '').replace('<br/>', '')
            str_study = str_study + item + ','
        return str_study

    def get_work_experience(self):  # 工作经历
        pattern = re.compile('工作经历</div><div class="c">·(.*?)<br/></div>')
        list_work = re.findall(pattern, self.page)
        str_work = ''
        for item in list_work:
            item = item.replace('&nbsp', '').replace('<br/>', '')
            str_work = str_work + item + ','
        return str_work

    def get_tags(self):
        """
        爬取好友标签
        :return:返回好友标签字典 user_tag
        """
        obj_ut = UserTag(self.uid)  # 实例化WeiboTag类
        tag = obj_ut.get_tag()  # 调用Tag方法，返回标签集,字符串
        user_tag = dict()
        user_tag['tags'] = tag  # 构建标签字典
        return user_tag

    def is_organization(self):
        """
        判断大V是非组织还是组织
        :return:boolean 如果是非组织，返回true,否则,返回false
        """
        url = "http://weibo.cn/" + self.uid + "?vt=4"
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        webpage = response.read()
        pattern = re.compile("5337.gif")  # 这是组织的正则表达式
        if re.findall(pattern, webpage).__len__() > 0:
            is_person = True
        else:
            is_person = False
        return is_person

    def get_user_info(self):
        """
        将资料数据整合成字典形式
        :return: 用户的资料字典
        """
        user_info = dict()
        user_info['uid'] = self.uid
        user_info['info'] = dict()
        user_info['info']['name'] = self.get_name()
        user_info['info']['img'] = self.get_img_url()
        user_info['info']['intro'] = self.get_intro()
        user_info['info']['tags'] = self.get_tags()['tags']
        user_info['info']['sex'] = self.get_sex()
        user_info['info']['birthday'] = self.get_birthday()
        user_info['info']['address'] = self.get_address()
        user_info['info']['study'] = self.get_study_experience()
        user_info['info']['work'] = self.get_work_experience()
        user_info['info']['cer'] = self.get_cer_message()
        user_info['info']['feel'] = self.get_feel()
        user_info['info']['organization'] = self.is_organization()
        return user_info
