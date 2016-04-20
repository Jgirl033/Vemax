# coding=utf-8
from vemax.models import Users, Information, UserRelationship, Profiles
import re


class User:
    def __init__(self):
        pass

    @staticmethod
    def create_user(dict_user):  # 前端输入创建用户
        user = Users()
        user.username = dict_user['username']
        user.pwd = dict_user['password']
        user.uid = dict_user['uid']
        user.is_register = True  # 如果是True则说明我们已经获得了用户的账号和密码
        user.is_crawler = False
        try:
            user.save()
            return 1
        except:
            return 0

    @staticmethod
    def get_user(user):
        list_user = Users.objects.filter(username=user.username, pwd=user.pwd)
        return list_user

    @staticmethod
    def get_information(uid):
        information = Information.objects.get(uid=uid)
        dict_information = dict()
        dict_information['uid'] = uid
        dict_information['info'] = dict()
        dict_information['info']['sex'] = information.sex
        dict_information['info']['intro'] = information.intro
        dict_information['info']['img'] = information.image_url
        dict_information['info']['tags'] = information.tags
        dict_information['info']['address'] = information.address
        dict_information['info']['birthday'] = information.birthday
        dict_information['info']['name'] = information.username
        dict_information['info']['study'] = information.study_experience
        dict_information['info']['work'] = information.work_experience
        return dict_information


class Profile:
    def __init__(self):
        pass

    @staticmethod
    def get_profile(uid):
        list_obj_profiles = Profiles.objects.filter(uid=uid)
        list_profiles = list()
        for obj in list_obj_profiles:
            list_profiles.append(obj.content)
        return list_profiles


class Relationship:
    def __init__(self):
        pass

    @staticmethod
    def get_classify_friend(uid):
        list_relationship_obj = UserRelationship.objects.filter(user_uid=uid)
        dict_classify = dict()
        for item in list_relationship_obj:
            user_info = Information.objects.get(uid=item.friend_uid)  # 获取用户好友的信息
            if user_info.class_tags is None:
                continue
            list_class_tags = re.split(',', user_info.class_tags)
            del list_class_tags[-1]
            for tags in list_class_tags:
                if dict_classify.has_key(tags):
                    pass
                else:
                    dict_classify[tags] = list()
                dict_classify[tags].append((user_info.uid.uid, user_info.username))
        return dict_classify

    @staticmethod
    def get_close_friend(uid):
        list_relationship_obj = UserRelationship.objects.filter(user_uid=uid).order_by('degree')
        list.reverse(list(list_relationship_obj))
        dict_index = dict()
        count = list_relationship_obj.count()
        i = 1
        while count > 0:
            dict_index[list_relationship_obj[count - 1].friend_uid] = i
            i += 1
            count -= 1
        dict_relation = dict()
        for item in list_relationship_obj:
            close_friend = Information.objects.get(uid=item.friend_uid)
            if dict_relation.has_key(item.relationship):
                pass
            else:
                dict_relation[item.relationship] = list()
            dict_relation[item.relationship].append(
                    (close_friend.uid_id, close_friend.username, close_friend.intro, close_friend.tags, item.degree,
                     dict_index[item.friend_uid]))
        return dict_relation
