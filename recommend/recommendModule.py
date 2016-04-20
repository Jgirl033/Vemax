# coding=utf-8
"""
filename=recommendModule.py
author=Adien
date written=03/26/2016
date modify=03/26/2016
program purpose=根具用户关注的内容，向用户推荐具有时效性的好友微博和简介，在大量的人脉信息中，挖掘有用信息和感兴趣的人，
description=词典导入，时间过滤，特征向量建立，基于内容进行微博，简介推荐
"""
import django
import os
from init import globalModule
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()
import jieba.posseg
import datetime
from classify.extractKeysModule import ExtractKeys
from vemax.models import UserRelationship, Information, Profiles


class Recommender:
    def __init__(self, uid):
        self.uid = uid

    def get_bigV_feature_extractwords(self, list_bigV_info):
        print self.uid
        user_fea_vector = []
        blog = ''
        for bigV_info in list_bigV_info:
            for name in jieba.posseg.cut(bigV_info[0]):
                if name.flag == 'nr':
                    user_fea_vector.append(name.word)
                    break
                else:
                    user_fea_vector.append(name.word)
                    for tag in bigV_info[1]:
                        user_fea_vector.append(tag)
                    for weblog in bigV_info[2:]:
                        blog = blog + weblog
                    break
        key_word = ExtractKeys.get_extractwords(blog)
        for word in key_word:
            user_fea_vector.append(word)
        print '用户特征词长度：', len(user_fea_vector)
        return user_fea_vector

    def get_friend_feature_extractwords(self, list_friends_info):
        print self.uid
        list_feature_words = list()
        for i in list_friends_info:
            word_vector = []
            cut_result = jieba.posseg.cut(i[0])
            for word in cut_result:
                if 'n' in word.flag:
                    word_vector.append(word.word)
            list_feature_words.append(word_vector)
        print '-----分词完成-----'
        return list_feature_words

    def get_jaccard_account(self, user_fea_vector, list_feature_words, list_friends_info):
        print self.uid
        for i in range(len(list_feature_words)):
            sim_num = 0
            for word in list_feature_words[i]:
                if word in user_fea_vector:
                    sim_num += 1
            jaccard = sim_num * 1.0 / (len(list_feature_words[i]) + len(user_fea_vector))
            list_friends_info[i].append(jaccard)
        print '-----jaccard计算完成-----'

    def load_dictionary(self, list_bigV_info):
        userdict_path = globalModule.get_project_path() + '/recommend/interest_words.txt'
        jieba.load_userdict(userdict_path)
        for bigV_info in list_bigV_info:
            jieba.add_word(bigV_info[0])
            for tag in bigV_info[1]:
                jieba.add_word(tag)
        print '-----词典导入完成-----'

    def friends_info_filter(self, list_friends_info):
        print self.uid
        now_date = str(datetime.date.today())
        now_date = now_date.split('-')
        now_date = int(now_date[0]) * 10000 + int(now_date[1]) * 100 + int(now_date[2])
        now_date -= 100  # 过滤时间为100，即一个月
        new_friends_info = []
        for friend_info in list_friends_info:
            try:
                date = friend_info[1].split('-')
                date = int(date[0]) * 10000 + int(date[1]) * 100 + int(date[2])
                if now_date <= date:
                    new_friends_info.append(friend_info)
            except:
                continue
        del list_friends_info
        print '-----过滤完成-----'
        print '过滤后待推荐微博数：' + str(len(new_friends_info))
        return new_friends_info

    def recommend(self, user_info, list_friends_info):
        """
        function:基于用户所感兴趣的内容，利用基于内容推荐算法，向用户推荐近期的，可能感兴趣的博文，简介以及其对应好友。
        :param self:
        :param user_info: list[] 包含用户关注的大V信息，第二维中[0]大V名字，[1]大V标签列表 [2:]大V博文
        :param list_friends_info: list[] 第二维中[0]为博文，简介内容 [1]为博文时间，简介默认为今天时间 [2]博文或简介所对应的好友名字
        :return:friends_info: list[]    已排序，内容与输入时一样，为了计算效率，推荐指数为0或者时间在限定以外的已删除，
        """
        self.load_dictionary(user_info)  # 兴趣词典导入
        list_friends_info = self.friends_info_filter(list_friends_info)  # 时间过滤
        print 'jijij'
        user_fea_vector = self.get_bigV_feature_extractwords(user_info)  # 用户提取关键字
        for i in user_fea_vector:
            print i,
        list_feature_words = self.get_friend_feature_extractwords(list_friends_info)
        self.get_jaccard_account(user_fea_vector, list_feature_words, list_friends_info)
        list_friends_info = sorted(list_friends_info, key=lambda x: x[3], reverse=True)
        print '\n-----推荐结果：-----'
        for i in list_friends_info[0:10]:
            print i[3], i[0], i[1], i[2]
        return list_friends_info


if __name__ == '__main__':
    list_bigV_all = list()
    list_friend_all = list()
    list_obj_friend = UserRelationship.objects.filter(user_uid='3294598585')
    for item in list_obj_friend:
        db_info = Information.objects.get(uid=item.friend_uid)
        if item.relationship == 'v':
            bigV_all = list()
            bigV_all.append(db_info.username)
            str_tags = db_info.tags
            list_tags = str_tags.split('`')
            bigV_all.append(list_tags)

            list_profiles = Profiles.objects.filter(uid=item.friend_uid)
            for profile in list_profiles:
                bigV_all.append(profile.content)
            list_bigV_all.append(bigV_all)
        else:
            for obj_profile in Profiles.objects.filter(uid=item.friend_uid):
                list_friend_all.append([obj_profile.content, obj_profile.time, db_info.username])

    r = Recommender('22222')
    print r.recommend(list_bigV_all, list_friend_all)
