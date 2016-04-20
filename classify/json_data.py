#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-3-17 下午4:50
    @function:生成某个兴趣类别的好友间关系的json文件
"""
import json
import django
import os
from vemax.models import UserRelationship, Information, Users, Classify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


def get_classify_relation(uid, class_name):
    db_user = Users.objects.get(uid=uid)
    user_info = Information.objects.get(uid=db_user.uid)
    dict_relation = dict()
    dict_relation['nodes'] = list()  # 定义节点
    dict_relation['edges'] = list()  # 定义连边
    list_friend_relation = UserRelationship.objects.filter(user_uid=uid)
    list_classify_friend = list()
    for friend in list_friend_relation:
        db_info = Information.objects.get(uid=friend.friend_uid)
        if class_name in db_info.class_tags:  # 只获取本类别的好友
            dict_relation['nodes'].append(
                    {'name': db_info.username, 'image': "../static/image/user_circle/" + db_info.uid.uid + ".png"})
            list_classify_friend.append(friend)
    for user in list_classify_friend:
        for element in list_classify_friend:
            if UserRelationship.objects.filter(user_uid=user.user_uid.uid, friend_uid=element.friend_uid,
                                               is_fans=True,
                                               is_follow=True).count() == 1:
                dict_relation['edges'].append(
                        {"source": dict_relation['nodes'].index(
                                {'name': user_info.username,
                                 'image': "../static/image/user_circle/" + user_info.uid.uid + ".png",
                                 'uid': user_info.uid.uid}),
                            "target": dict_relation['nodes'].index(
                                    {'name': db_info.username,
                                     'image': "../static/image/user_circle/" + db_info.uid.uid + ".png",
                                     'uid': db_info.uid.uid}),
                            "relation": ''}
                )
    return dict_relation


def save_classify_relation(uid, class_name):
    class_id = Classify.objects.get(class_name=class_name).id
    file_relation = '../static/image/d3/' + uid + str(class_id) + '.json'
    fp = open(file_relation, 'w')
    fp.write(json.dumps(get_classify_relation(uid, class_name)))
    fp.close()
