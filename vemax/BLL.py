# coding=utf-8
import multiprocessing
from init.server_remote import start_register_crawler
from crawler.relation.friendModule import UserMessage
from vemax import DAL


class User:
    def __init__(self):
        pass

    @staticmethod
    def sys_register(user, verification_code, r):
        """
        判断用户是否成功注册
        :param r:
        :param verification_code: 用户验证码
        :param user: obj,是Users的实例对象
        :return:int,如果用户用户名与密码跟数据库中的数据匹配,则注册失败，返回0,否则成功，返回１,并对用户账号密码的一致性以及验证码进行判断
        """
        is_user = DAL.User.get_user(user)
        if is_user.count() == 0:
            text = r.register(user.username, user.pwd, verification_code)
            if '退出' in text:
                uid = UserMessage.user_id()
                dict_user = dict()
                dict_user['username'] = user.username
                dict_user['uid'] = uid
                dict_user['password'] = user.pwd
                dict_user['is_register'] = True
                p = multiprocessing.Process(target=start_register_crawler, args=(uid,))
                p.start()  # 爬取用户的亲密好友信息
                if DAL.User.create_user(dict_user) == 1:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    @staticmethod
    def sys_login(user):
        """
        判断用户是否成功登录
        :param user: obj,是Users的实例对象
        :return:int,如果用户用户名与密码跟数据库中的数据匹配,则登录成功，否则失败
        """
        is_user = DAL.User.get_user(user)
        if is_user.count() == 0:
            return 0
        else:
            return is_user

    @staticmethod
    def show_information(uid):
        """
        显示用户个人基本信息
        :param uid: str,用户唯一微博uid
        :return:dict,用户个人所有基本信息
        """
        dict_user_information = DAL.User.get_information(uid=uid)
        return dict_user_information


class Profile:
    def __init__(self):
        pass

    @staticmethod
    def show_profile(uid):
        list_profiles = DAL.Profile.get_profile(uid)
        return list_profiles


class Relationship:
    def __init__(self):
        pass

    @staticmethod
    def show_classify(uid):
        dict_classify_friend = DAL.Relationship.get_classify_friend(uid)
        return dict_classify_friend

    @staticmethod
    def show_relationship(uid):
        dict_close_friend = DAL.Relationship.get_close_friend(uid)
        return dict_close_friend
