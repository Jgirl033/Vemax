#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-3-11 上午10:43
    @function:负责启动爬取所有用户的资料,博文的爬虫系统,部署在本地电脑
"""
import django
import os
import re

from classify.classifyModule import UserClassify
from classify.json_data import save_classify_relation
from crawler.relation.classifyModule import FriendAnalyse, FriendClassify
from crawler.user.infoModule import UserMessage
from crawler.user import profileModule
from crawler.relation.bigVModule import BigV
from init.globalModule import is_exist, is_start_crawler, is_start_classify

from crawler.weibo.mobileWeiboModule import MobileWeibo
from recommend.recommendModule import Recommender
from save.classify.classifyModule import ClassSave
from save.user.infoModule import InfoSave, UserSave
from save.user.profileModule import ProfileSave
from save.relation.relationModule import UserRelationshipSave
from vemax.BLL import Relationship, Profile, User
from vemax.models import Users, Friend, Classify, UserRelationship, Information, Profiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


def start_classify(uid):
    user_friends = Relationship.show_relationship(uid)  # 获得用户的好友列表
    # user_friends.append(uid)
    list_user_uid = list()
    for friend in user_friends:
        for element in user_friends[friend]:
            list_user_uid.append(element[0])

    list_user_uid.append(uid)

    for user in list_user_uid:
        user_info = User.show_information(user)
        print user_info
        str_user_tags = user_info['info']['tags'].replace(",", "`")
        list_user_profiles = Profile.show_profile(user)
        list_obj_bigV = UserRelationship.objects.filter(relationship='v')
        list_bigV_tags = list()
        for obj in list_obj_bigV:
            bigV_info = User.show_information(obj.friend_uid)
            str_bigV_tags = bigV_info['info']['tags'].replace(",", "`")
            list_bigV_tags.append(str_bigV_tags)
        result = UserClassify().classify(str_user_tags, list_user_profiles, list_bigV_tags)
        user_class_tags = ''
        for i in result:
            user_class_tags += i + ','
        user_info = Information.objects.get(uid=user)
        user_info.class_tags = user_class_tags
        user_info.save()

    user = Users.objects.get(uid=uid)
    user.is_classify = True
    user.save()


def start_crawler(uid, close_friend=None):
    """
    启动爬虫系统，爬取对应用户的资料,博文,关注的大V
    :param close_friend:
    :param uid:
    :return:
    """
    user = UserMessage(uid)
    user_info = user.get_user_info()  # 用户资料所有信息
    print InfoSave.save_intro_tags(user_info)
    print '---爬取存储用户资料成功！---'

    p = profileModule.Profile(uid)
    user_profiles = p.get_user_profile()  # 用户第一页博文，大概是10条
    print user_profiles
    print ProfileSave.save_profile(user_profiles)
    print '---爬取存储用户微博成功！---'

    bV = BigV(uid)
    print bV.get_bigV()
    for element in bV.get_bigV_uid():
        if is_exist(element) == 1:
            pass
        else:
            print '出现大Ｖ：' + element
            dict_user = dict()
            dict_user['uid'] = element
            dict_user['password'] = '888888'
            dict_user['username'] = ''
            print UserSave.save_users(dict_user)

            user = UserMessage(element)
            user_info = user.get_user_info()  # 用户资料所有信息
            user_info['info']['V'] = 'Y'
            print InfoSave.save_intro_tags(user_info)
        print UserRelationshipSave.save_bigV_relationship(uid, element)
        user_profiles = profileModule.Profile(str(element)).get_user_profile()
        print ProfileSave.save_profile(user_profiles)
    print '---爬取存储用户关注大V的资料,博文和关系成功！---'

    if close_friend is not None:  # 使用注册过的用户进行亲密好友的信息的提取
        print '---开始爬取好友信息---'
        friend_list = FriendAnalyse.get_friend_info(close_friend)  # 亲密好友信息
        user_list = FriendAnalyse.get_user_info(uid)  # 用户信息
        for element in FriendClassify.relation_sort(user_list, friend_list).items():
            for ele in element[1]:
                if is_exist(ele[0]) == 0:
                    dict_user = dict()
                    dict_user['uid'] = ele[0]
                    dict_user['password'] = '888888'
                    dict_user['username'] = ''  # 这是用户的注册账号
                    print UserSave.save_users(dict_user)

                    user = UserMessage(str(ele[0]))
                    user_info = user.get_user_info()  # 用户资料所有信息
                    print InfoSave.save_intro_tags(user_info)

                    user_profiles = profileModule.Profile(str(ele[0])).get_user_profile()
                    print ProfileSave.save_profile(user_profiles)
                else:
                    pass
                UserRelationshipSave.save_close_friend_relationship(uid, ele, element[0])
    # 爬取成功后将is_crawler字段修改为True
    user = Users.objects.get(uid=uid)
    user.is_crawler = True
    user.save()


def start_recommend(uid):
    list_bigV_all = list()
    list_friend_all = list()
    list_obj_friend = UserRelationship.objects.filter(user_uid=uid)
    for item in list_obj_friend:
        if item.relationship == 'v':
            bigV_all = list()
            db_info = Information.objects.get(uid=item.friend_uid)
            bigV_all.append(db_info.username)
            str_tags = db_info.tags
            list_tags = str_tags.split('`')
            bigV_all.append(list_tags)

            list_profiles = Profiles.objects.filter(uid=item.friend_uid)
            for profile in list_profiles:
                bigV_all.append(profile.content)
            list_bigV_all.append(bigV_all)
        else:
            db_info = Information.objects.get(uid=item.friend_uid)
            # if db_info.intro != '':
            #     list_friend_all.append([db_info.intro, str(datetime.date.today()), db_info.username])
            for obj_profile in Profiles.objects.filter(uid=item.friend_uid):
                list_friend_all.append([obj_profile.content, obj_profile.time, db_info.username])
    r = Recommender(uid)
    count = 0
    dict_recommend = dict()
    for item in r.recommend(list_bigV_all, list_friend_all):
        count += 1
        obj_recommend = dict()
        obj_recommend['username'] = item[2]
        obj_recommend['content'] = item[0]
        dict_recommend[count] = obj_recommend
    return dict_recommend


def other_login():
    """
    用于爬虫的账号密码
    """
    username = '18819423747'
    password = 'xie5321927'
    MobileWeibo().login(username, password)


if __name__ == "__main__":
    # ClassSave().save_all_class()
    # other_login()
    while True:
        if is_start_classify() == 0:
            print
            pass
        else:
            for item in is_start_classify():
                start_classify(item.uid)
                for class_obj in Classify.objects.filter():
                    save_classify_relation(item.uid, class_obj.class_name)
                    # if is_start_crawler() == 0:  # 说明没有新入库的用户,程序处于持续等待
                    #     pass
                    # else:
                    #     list_user = is_start_crawler()
                    #     for item in list_user:
                    #         while item.is_register:
                    #             tuple_close_friend = list()
                    #             if Friend.objects.filter(uid=item.uid).count() == 0:
                    #                 print '1'
                    #                 continue
                    #             else:
                    #                 print '2'
                    #                 obj_close_friend = Friend.objects.get(uid=item.uid)
                    #                 str_close_friend = obj_close_friend.list_friend
                    #             list_close_friend = re.findall('\(.*?\)', str_close_friend)
                    #             for friend in list_close_friend:
                    #                 tuple_friend = re.split(', ', friend.replace('(', '').replace(')', ''))
                    #                 tuple_close_friend.append((tuple_friend[0].replace("'", ""), tuple_friend[1]))
                    #             user_id = str(item.uid)
                    #             start_crawler(user_id, tuple_close_friend)
                    #             break
