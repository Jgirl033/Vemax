# coding=utf-8
import json

import django
import os
from vemax.models import Classify, Users, UserRelationship, Information

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


class ClassSave:
    def __init__(self, list_class=None):
        if list_class is None:
            self.list_class = ['健康养生', '军事历史', '时政', '公益', '读书',
                               '电视剧', 'IT互联网', '教育', '艺术', '电影',
                               '动漫', '游戏', '旅游', '美食', '摄影', '萌宠',
                               '服装美容', '体育', '设计', '综艺', '星座',
                               '音乐', '健身', '财经']
        else:
            self.list_class = list_class

    def save_all_class(self):
        for item in self.list_class:
            c = Classify()
            c.id = self.list_class.index(item) + 1
            c.class_name = item
            c.img_url = '../static/image/classify/' + str(self.list_class.index(item) + 1) + '.png'
            c.save()

    @staticmethod
    def save_classify_relation(uid, class_name):
        class_id = Classify.objects.get(class_name=class_name).id
        file_relation = '../static/image/d3/' + uid + str(class_id) + '.json'
        fp = open(file_relation, 'w')
        fp.write(json.dumps(get_classify_relation(uid, class_name)))
        fp.close()


def get_classify_relation(uid, class_name):
    db_user = Users.objects.get(uid=uid)
    user_info = Information.objects.get(uid=db_user.uid)
    dict_relation = dict()
    dict_relation['nodes'] = list()  # 定义节点
    dict_relation['edges'] = list()  # 定义连边
    set_friend_relation = set(UserRelationship.objects.filter(user_uid=uid))

    list_classify_friend = list()
    for friend in set_friend_relation:
        db_info = Information.objects.get(uid=friend.friend_uid)
        if class_name in db_info.class_tags:  # 只获取本类别的好友
            dict_relation['nodes'].append(
                    {'name': db_info.username, 'image': "../static/image/circle/" + db_info.uid.uid + ".png"})
            list_classify_friend.append(friend)
    for user in list_classify_friend:
        for element in list_classify_friend:
            if UserRelationship.objects.filter(user_uid=user.user_uid.uid, friend_uid=element.friend_uid,
                                               is_fans=True,
                                               is_follow=True).count() == 1:
                dict_relation['edges'].append(
                        {"source": dict_relation['nodes'].index(
                                {'name': user_info.username,
                                 'image': "../static/image/circle/" + user_info.uid.uid + ".png",
                                 'uid': user_info.uid.uid}),
                            "target": dict_relation['nodes'].index(
                                    {'name': db_info.username,
                                     'image': "../static/image/circle/" + db_info.uid.uid + ".png",
                                     'uid': db_info.uid.uid}),
                            "relation": ''}
                )
    return dict_relation
