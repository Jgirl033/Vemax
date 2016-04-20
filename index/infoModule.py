# coding=utf-8
import jieba.analyse
from index.lib.reverse import InterfaceIndex


class InfoIndex(InterfaceIndex):
    def addWordDict(self, user_info):
        """
        将单个用户的简介分词，提取简介特征，并加入标签特征
        :param user_info: dict,用户的资料,包括简介intro和标签tags
        :return: dict,数据格式：{'uid':'','tags':[],'intro':[]}
        """
        info_words = dict()  # 资料能够提供的关键词
        info_words['uid'] = user_info['uid']  # 资料的用户id
        info_words['tags'] = list()  # 资料的标签列表
        for item in user_info['tags']:
            info_words['tags'].append(item.decode('utf-8'))  # 标签需要变成unicode
        intro = user_info['intro']
        word_list = jieba.analyse.extract_tags(intro, 3, allowPOS=('n', 'nv'))
        info_words['intro'] = word_list
        return info_words

    def addIndexDict(self, info_words):
        """
        整合单个用户所有的资料（简介和关键词）-关键词关系
        :param info_words: dict,表示用户-资料关键词列表对应关系数据
        :return: dict,数据格式：[(uid,source,word)]
        """
        user_words = []
        uid = info_words['uid']
        for word in info_words['tags']:
            user_words.append((uid, 't', word))
        for word in info_words['intro']:
            user_words.append((uid, 'i', word))
        return user_words

    def updateIndex(self, user_words, users_info_index):
        """
        将整个系统的索引进行更新
        :param user_words: dict,用户-来源-关键词对应关系数据
        :param users_info_index:
        :return:dict,数据格式:{
                        'intro':{word:[uid1,uid2]}
                        'tags' :{word:[uid1,uid2]}
                        }
        """

        for item in user_words:
            uid = item[0]
            source = item[1]
            word = item[-1]

            if source == 'i':
                info_index = users_info_index['intro']
            else:
                info_index = users_info_index['tags']
            if word == '':
                pass
            else:
                if word in info_index.keys():  # 如果旧的倒排索引存在这个特征，则直接把元组uid追加到列表后
                    info_index[word].append(uid)
                else:  # 如果旧的倒排索引不存在这个特征，则添加新的键，并赋予键值
                    info_index[word] = list()
                    info_index[word].append(uid)
        return users_info_index
