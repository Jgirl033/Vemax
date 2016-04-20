# coding:utf-8
import urllib2
import re
import time
import random
from collections import Counter

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


def get_uid(uid):  # 有的微博用户会修改uid，所以应该对uid进行验证,也就是最终得到数字uid
    """
    获得好友真正的uid
    :param uid:好友修改过的uid
    :return:好友真正的uid
    """
    url = 'http://weibo.cn/' + uid
    req = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(req)
    page = response.read()
    pattern = re.compile('<a href="/im/chat.uid=(.*?)&')
    text = re.findall(pattern, page)
    return text[0]


class MessagePage:
    def __init__(self):
        pass

    @staticmethod
    def get_chat_page():
        chat_page = ''
        for i in range(1, 30):
            url = 'http://weibo.cn/msg/?&page=' + str(i)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            chat_page += page + '`'
        return chat_page

    @staticmethod
    def get_at_me_page():
        at_me_page = ''
        for i in range(1, 30):
            url = 'http://weibo.cn/at/weibo?&page=' + str(i)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            at_me_page += page + '`'
        return at_me_page

    @staticmethod
    def get_comment_page():
        comment_page = ''
        for i in range(1, 30):
            url = 'http://weibo.cn/msg/comment/receive?&page=' + str(i)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            comment_page += page + '`'
        return comment_page

    @staticmethod
    def get_message_page():
        chat_page = MessagePage.get_chat_page()
        at_me_page = MessagePage.get_at_me_page()
        comment_page = MessagePage.get_comment_page()
        dict_message_page = dict()
        dict_message_page['chat'] = chat_page
        dict_message_page['at_me'] = at_me_page
        dict_message_page['comment'] = comment_page
        return dict_message_page


class RealFriend:  # 相互关注好友,使用本人账号爬取

    def __init__(self):
        pass

    @staticmethod
    def get_page_num():
        """
        得到页数
        :return:str 页数
        """
        url = 'http://weibo.cn/attgroup/bilateral?cat=user&rl=0&'
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        page = response.read()
        pattern = re.compile('&nbsp;1/(.*?)页')
        text = re.findall(pattern, page)
        if len(text) > 0:
            return text[0]
        else:
            return '1'

    @staticmethod
    def get_real_friend():
        """
        爬取相互关注好友列表
        :return:dict,数据格式:{uid:username,uid2:username2}
        """
        friend_dict = dict()
        page_num = RealFriend.get_page_num()  # 获得相互关注好友的页数
        for i in range(1, int(page_num)):  # 访问相互关注页面
            url = 'http://weibo.cn/attgroup/bilateral?cat=user&f=atts&vt=4&page=' + str(i)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            time.sleep(random.randint(3, 5))
            pattern = re.compile('<tr><td valign="top">.*?<img src="(.*?)" alt="pic" /></a></td>'
                                 '<td valign.*?href="/u?/?(.*?)\?vt=4">(.*?)<.*?(粉丝.*?)&')
            f_list = re.findall(pattern, page)

            for item in f_list:
                if item[1].isdigit():
                    if len(item[1]) == 10:
                        friend_dict[item[1]] = item[2]
                    else:
                        real_uid = get_uid(item[1])
                        friend_dict[real_uid] = item[2]
                else:
                    real_uid = get_uid(item[1])
                    friend_dict[real_uid] = item[2]
        return friend_dict


class MessageFriend:  # 存在通信关系的朋友,使用本人账号爬取

    def __init__(self):
        pass

    @staticmethod
    def chat(page):
        chat_friend = {}
        pattern = re.compile('<a href="/u/(.*?)">(.*?)</a>.*?class="cc">共(.*?)条对话')
        c_list = re.findall(pattern, page)
        for item in c_list:
            chat_friend[item[0]] = float(item[2])  # 形式添加一个项
        return chat_friend

    @staticmethod
    def at_me(page, uid):
        friend_list = []
        pattern = re.compile('<a class="nk" href="http://weibo.cn/u/(.*?)">(.*?)</a>')
        a_list = re.findall(pattern, page)
        for item in a_list:
            if item[0] == uid:
                pass
            else:
                friend_list.append(item[0])
        return friend_list

    @staticmethod
    def comment(page):
        friend_list = list()
        pattern = re.compile('<a href="/u/(.*?)">(.*?)</a>')
        c_list = re.findall(pattern, page)
        for item in c_list:
            if u'我' in item[1]:
                pass
            else:
                friend_list.append(item[0])
        return friend_list


class CloseFriend:  # 亲密好友,经过相互关注好友与通讯好友分析筛选得出

    def __init__(self):
        pass

    @staticmethod
    def is_friend(real_friend, message_friend):
        """
        判断是否为好友
        :param real_friend: 相互关注的好友的列表
        :param message_friend: 通讯好友列表
        :return:好友列表中相互关注的好友
        """
        list_friend = []
        for i in message_friend:
            if i in real_friend:
                list_friend.append(i)
            else:
                pass
        return list_friend

    @staticmethod
    def comment_at_me(real_friend, comment_at_friend):

        print '筛选后'
        dict_comment_at = dict()
        try:
            appear_time = Counter(CloseFriend.is_friend(real_friend, comment_at_friend))  # 出现次数
            values = appear_time.values()
            max_num = float(max(values))  # 出现次数最大值
            min_num = float(min(values))  # 出现次数最小值
            order_appear_time = sorted(appear_time.iteritems(), key=lambda asd: asd[1],
                                       reverse=True)  # asd:asd[1]是按键值，asd:asd[0]是按键
            for item in order_appear_time:
                if max_num == min_num:
                    print '不可归一化'
                else:
                    result = (float(item[1]) - min_num) / (max_num - min_num)  # 归一化
                    dict_comment_at[item[0]] = result
        except:
            print '无互动好友'
        return dict_comment_at

    @staticmethod
    def chat(real_friend, chat_friend):

        print '筛选后'
        dict_chat = {}
        try:
            for i in chat_friend.keys():
                if i in real_friend:
                    pass
                else:
                    chat_friend.pop(i)  # 删除不在好友列表里
            values = chat_friend.values()
            max_num = max(values)  # 出现次数最大值
            min_num = min(values)  # 出现次数最小值
            order_appear_time = sorted(chat_friend.iteritems(), key=lambda asd: asd[1],
                                       reverse=True)  # asd:asd[1]是按键值，asd:asd[0]是按键
            for item in order_appear_time:
                if max_num == min_num:
                    print '不可归一化'
                    dict_chat[item[0]] = 1.0
                else:
                    result = (float(item[1]) - min_num) / (max_num - min_num)  # 归一化
                    dict_chat[item[0]] = result
        except:
            print '无互动好友'
        return dict_chat

    @staticmethod
    def get_close_friend(real_friend, dict_message_page):

        chat_friend = MessageFriend.chat(dict_message_page['chat'])
        chat_real_friend = CloseFriend.chat(real_friend, chat_friend)
        print chat_real_friend
        comment_friend = MessageFriend.comment(dict_message_page['comment'])
        comment_real_friend = CloseFriend.comment_at_me(real_friend, comment_friend)
        print comment_real_friend
        at_me_friend = MessageFriend.at_me(dict_message_page['at_me'],dict_message_page['uid'])
        at_me_real_friend = CloseFriend.comment_at_me(real_friend, at_me_friend)
        print at_me_real_friend
        for i, j in chat_real_friend.items():
            if i in comment_real_friend.keys():
                comment_real_friend[i] += j
            else:
                comment_real_friend[i] = j
        for m, n in comment_real_friend.items():
            if m in at_me_real_friend.keys():
                at_me_real_friend[m] += n
            else:
                at_me_real_friend[m] = n
        list_close_friend = sorted(at_me_real_friend.iteritems(), key=lambda asd: asd[1],
                                   reverse=True)  # asd:asd[1]是按键值，asd:asd[0]是按键
        for item in list_close_friend[:15]:  # 选出排名前十五的好友
            print item
        return list_close_friend


class FriendCloseFriend:  # 朋友的朋友

    def __init__(self):
        pass

    @staticmethod
    def get_friend_close_friend(uid):
        """
        爬取好友的亲密好友
        :param uid: 好友的uid
        :return:排名前三的亲密好友字典
        """
        f_list = []
        dict_friend_close_friend = {}
        for i in range(0, 20):
            url = 'http://weibo.cn/at/weibo?uid=' + uid + '&page=' + str(i)
            req = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            pattern = re.compile('<a class="nk" href="http://weibo.cn/u/(.*?)">(.*?)</a>')
            text = re.findall(pattern, page)
            for item in text:
                if item[0] == uid:  # 是本人
                    pass
                else:
                    f_list.append((item[0], item[1]))
        sort = Counter(f_list)  # 统计出现次数
        sort_list = sorted(sort.iteritems(), key=lambda asd: asd[1], reverse=True)
        for item in sort_list[:3]:  # 输出次数前三
            print item[0][1], item[1]  # 输出好友昵称和出现次数
            dict_friend_close_friend[(item[0])[0]] = item[0][1]
        return dict_friend_close_friend


class UserMessage:  # 获取uid,使用本人账号登录
    def __init__(self):
        pass

    @staticmethod
    def user_id():
        url = 'http://weibo.cn'
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        page = response.read()
        pattern = re.compile('<a href="/at/weibo\?uid=(.*?)">')
        list_uid = re.findall(pattern, page)
        return list_uid[0]
