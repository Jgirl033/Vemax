# coding=utf-8
import jieba.analyse
from index.lib.reverse import InterfaceIndex


class ProfileIndex(InterfaceIndex):
    def addWordDict(self, user_profiles):
        """
        将单个用户的博文进行分词,建立用户-博文-关键词列表对应关系数据
        :param user_profiles: dict,表示用户-博文对应关系数据
        :return: dict,数据格式：{'uid':'','profile':{cid:[]}}
        """
        profile_words = dict()
        profile_words['uid'] = user_profiles['uid']
        profile_words['profile'] = dict()
        for item in user_profiles['profile'].items():
            profile = item[1]
            word_list = jieba.analyse.extract_tags(profile, 3, allowPOS=('n', 'nv'))
            profile_words['profile'][item[0]] = word_list
        return profile_words

    def addIndexDict(self, profile_words):
        """
        整合单个用户所有的博文-关键词关系
        :param profile_words: dict,表示用户-博文关键词列表对应关系数据
        :return: dict,数据格式：[(uid,cid,word)]
        """
        user_words = list()
        uid = profile_words['uid']
        for item in profile_words['profile'].items():
            cid = item[0]
            keywords = item[1]
            for word in keywords:
                user_words.append((uid, cid, word))
        return user_words

    def updateIndex(self, user_words, users_profiles_index):
        """
        将整个系统的索引进行更新
        :param user_words: dict,用户-博文-关键词对应关系数据
        :param users_profiles_index: dict,系统倒排索引
        :return: dict,数据格式:{word:[uid,cid]}
        """
        for item in user_words:
            uid = item[0]
            cid = item[1]
            word = item[-1]
            if word in users_profiles_index.keys():  # 如果旧的倒排索引存在这个特征，则直接把元组(uid,cid)追加到列表后
                users_profiles_index[word].append((uid, cid))
            else:  # 如果旧的倒排索引不存在这个特征，则添加新的键，并赋予键值
                users_profiles_index[word] = list()
                users_profiles_index[word].append((uid, cid))
        return users_profiles_index
