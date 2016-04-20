# coding=utf-8

import django
import os
from vemax.models import UserRelationship, Users
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


class UserRelationshipSave:
    def __init__(self):
        pass

    @staticmethod
    def save_close_friend_relationship(uid, friend, relationship):
        ur = UserRelationship()
        ur.user_uid = Users.objects.get(uid=uid)
        ur.friend_uid = friend[0]
        ur.degree = friend[2]
        ur.relationship = relationship
        try:
            ur.save()
            return 0
        except:
            return 1

    @staticmethod
    def save_bigV_relationship(uid, bigV_uid):
        ur = UserRelationship()
        ur.user_uid = Users.objects.get(uid=uid)
        ur.friend_uid = bigV_uid
        ur.degree = 0
        ur.relationship = 'v'
        ur.is_follow = True
        try:
            ur.save()
            return 0
        except:
            return 1
