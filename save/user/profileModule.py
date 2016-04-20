# coding=utf-8

import django
import os
import datetime
import re
from vemax.models import Profiles, Users
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


class ProfileSave:
    def __init__(self):
        pass

    @staticmethod
    def save_profile(user_profiles):
        uid = user_profiles['uid']
        cid = 0
        for item in Profiles.objects.filter(uid=uid):
            if int(item.cid) >= cid:
                cid = int(item.cid)
        for item in user_profiles['profile']:
            print item
            p = Profiles()
            p.uid = Users.objects.get(uid=uid)
            if Profiles.objects.filter(uid=uid, content=item[0]).count() == 1:  # 避免博文出现重复
                print '博文内容冲突！'
                pass
            cid += 1
            p.cid = cid  # 这里是关键步骤，采用的是采取当前该用户值最大的一个cid，并在词cid的基础上递增
            p.time = datetime.datetime.strptime(item[4], '%Y-%m-%d')
            pattern = re.compile('\[(.*?)\]')
            p.content = item[0]
            p.like_count = re.search(pattern, item[1]).group(1)
            p.forward_count = re.search(pattern, item[2]).group(1)
            p.comment_count = re.search(pattern, item[3]).group(1)
            try:
                p.save()
            except:
                continue
        return 0
