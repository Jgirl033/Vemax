# coding:utf-8
import urllib2
import re
import datetime
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


def get_date(old_date):
    """
    转换微博博文发表日期
    :param old_date:原先显示在博文中的时间
    :return:date　转化后具有严格格式的时间
    """
    if '月' in old_date:
        pattern = re.compile('(.*?)月(.*?)日')
        date = re.findall(pattern, old_date)
        today = datetime.date.fromtimestamp(time.time())
        year = str(today.year)
        new_date = year + '-' + date[0][0] + '-' + date[0][1]
    elif '-' in old_date:
        new_date = old_date[:10]
    else:
        new_date = datetime.date.today()
    return str(new_date)


class Profile:
    def __init__(self, uid):
        self.uid = uid

    def get_profile(self):
        """
        爬取博文
        :return:返回博文字典，keys为cid,value为博文
        """
        list_profile = []
        for i in range(1, 6):  # 爬取前5页博文,大概是50条
            str_profile_url = 'http://weibo.cn/' + self.uid + '/profile?page=' + str(i)
            req = urllib2.Request(url=str_profile_url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            pattern = re.compile(
                    '<div>.*?<span class="ctt">(.*?)</span>.*?<a href="http://weibo.cn/attitude.*?'
                    '(赞.*?)<.*?(转发.*?)<.*?(评论.*?)<.*?<span class="ct">(.*?)&nbsp')
            list_profile_all = re.findall(pattern, page)
            for item in list_profile_all:
                print item
                str_remove = re.compile('<.*?>')
                text = re.sub(str_remove, '', item[0])
                profile_date = get_date(item[4])
                list_profile.append((text, item[1], item[2], item[3], profile_date))
        return list_profile

    def get_user_profile(self):
        """
        将博文数据整合成字典形式
        :return: 用户的博文字典
        """
        if not isinstance(self.uid, (str)):  # 判断输入uid是否为字符串
            print 'Arg must be str'
        else:
            user_profiles = dict()
            profile = Profile(self.uid)  # 实例化Profile类
            list_profile = profile.get_profile()  # 调用Profile中的GetProfile方法，返回博文字典
            # keys为cid，values为博文文本
            user_profiles['uid'] = self.uid
            user_profiles['profile'] = list_profile  # 构建博文字典
            return user_profiles

    def get_new_profile(self, url, pattern):
        """
        爬取最新的博文
        :param url: 链接
        :param pattern: 正则表达式
        :return:
        """
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        page = response.read()
        text = re.findall(pattern, page)
        new_profile = re.sub(re.compile('<.*?>'), '', ''.join(text[0]))
        return new_profile

    def get_new_profile_all(self):
        """
        爬取一条最新原创博文和一条最新转发博文
        :return:list,博文列表（原创+转发）
        """
        # 最新一条原创微博
        original_url = 'http://weibo.cn/' + self.uid + '/profile?filter=1'  # 原创微博页面
        original_pattern = re.compile(
                '<div>.*?<span class="ctt">(.*?)</span>.*?<a href="http://weibo.cn/attitude.*?'
                '(赞.*?)<.*?(转发.*?)<.*?(评论.*?)<.*?<span class="ct">(.*?)&nbsp')
        original_new_profile = self.get_new_profile(original_url, original_pattern)

        # 最新一条转发微博
        last_forward_url = 'http://weibo.cn/' + self.uid + '/profile'  # 全部微博页面
        last_forward_pattern = re.compile(
                '转发了&nbsp.*?<span class="ctt">(.*?)</span>.*?'
                '(赞.*?)<.*?(转发.*?)<.*?(评论.*?)<.*?<span class="ct">(.*?)&nbsp')
        last_forward_profile = self.get_new_profile(last_forward_url, last_forward_pattern)
        list_profile = [original_new_profile, last_forward_profile]
        return list_profile
