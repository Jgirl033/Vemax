# coding=utf-8
import math
import jieba
import operator
import django
import os
from index.reserve_index import ReserveIndex, load_fileset
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()
from vemax.models import UserRelationship, Profiles, Information

reload(sys)
sys.setdefaultencoding("utf-8")


class BM25Model:
    def __init__(self, related_index, query):
        self.related_index = related_index
        self.document = related_index.document
        self.avg_len = self.get_avg_len_doc()
        self.query_words = list(jieba.cut(query))
        self.reDoc = self.get_doc_related()
        self.b = 0.75
        self.k1 = 1.2
        self.k2 = 200

    def get_avg_len_doc(self):
        """
        function: 计算文档的平均长度​
        :return: 文档的平均长度​
        """
        sum = 0
        for doc in self.related_index.document:
            sum += doc.__len__()
        avg_len_doc = float(sum) / self.related_index.document.__len__()
        return avg_len_doc

    def get_word_fre(self, word):
        """
        function: 单词在文档中出现的频数,不含重复
        :param word: 特定单词
        :return: 频数
        """
        frequency = 0
        for doc in self.document:
            if word.encode('utf-8') in doc:
                frequency += 1
        return frequency

    @staticmethod
    def get_word_doc_fre(word, doc):
        """
        function:特定单词在特定文档中出现的次数
        :param word: 特定单词
        :param doc:特定文档
        :return: 出现的次数
        """
        num = 0
        words = jieba.cut(doc)
        for w in words:
            if w == word:
                num += 1
        return num

    def get_word_query(self, word):
        """
        function:统计特定单词在查询列表出现的次数
        :param word:特定单词
        :return:出现的次数
        """
        qf = self.query_words.count(word)
        return qf

    @staticmethod
    def count_doc(doc):
        """
        function: 统计文档集合的大小
        :param doc: 文档集合
        :return:文档集合的大小
        """
        dl = doc.__len__()
        return dl

    def get_doc_related(self):
        """
        function:找出与查询相关联的文档集合
        :return:文档集合
        """
        doc_related = []
        for word in self.query_words:
            if word.encode('utf-8'):
                li = self.related_index.query(word)
                if li is None:
                    continue
                doc_related += li
        doc_related = list(doc_related)
        return doc_related

    def BM25(self, doc_related):
        """
        function:计算BM25值
        :param doc_related: 与查询相关联的文档集合
        :return: BM25值]
            print '--------'
        """
        sum = 0
        N = self.document.__len__()
        for word in self.query_words:
            n = self.get_word_fre(word)
            part1 = float(N - n + 0.5) / (n + 0.5)
            part1 = math.log(part1)
            f = self.get_word_doc_fre(word, doc_related)
            k = self.k1 * ((1 - self.b) + self.b * float(self.count_doc(doc_related)) / self.avg_len)
            part2 = float(self.k1 + 1) * f / (k + f)
            qf = self.get_word_fre(word)
            part3 = float(self.k2 + 1) * qf / (self.k2 + qf)
            bm25 = part1 * part2 * part3
            sum += bm25
        return sum

    def rank_doc(self):
        """
        function:对文档的BM25值进行排序
        :return:经BM25排序后的文档集合
        """
        dict_rank_score = {}
        for doc in self.reDoc:
            dict_rank_score[doc] = self.BM25(self.document[doc])
        sorted_x = sorted(dict_rank_score.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_x


if __name__ == '__main__':
    search_text = '从那时候开始'
    list_friend = UserRelationship.objects.filter(user_uid_id='3294598585')
    list_document = []
    list_user = []
    list_profile = []
    for item in list_friend:
        # print item.friend_uid
        if item.relationship == 'v':
            pass
        else:
            # list_user.append(item.friend_uid + '.txt')
            db_info = Information.objects.get(uid=item.friend_uid)
            str_intro_profiles = db_info.intro + '`'
            for element in Profiles.objects.filter(uid=item.friend_uid):
                str_intro_profiles += element.content + '`'
            li = str_intro_profiles.split('`')
            number = li.__len__()
            for i in range(0, number, 1):
                list_user.append(str(item.friend_uid).replace('.txt', ''))
                list_document.append(li[i])
    obj_index_user = ReserveIndex(list_document)
    bm = BM25Model(obj_index_user, search_text)
    sorted_x = bm.rank_doc()
    count = 0
    list_user_intro = []

    print len(list_user)
    print len(list_document)
    # for item in list_user:
    #     print item
    for x in sorted_x:
        # print x[0]
        if search_text in bm.document[x[0]]:
            dict_user = dict()
            print 'doc num:', x[0], 'point:', x[1], 'source:', list_user[x[0]]
            print bm.document[x[0]]
            print '--------'
            count += 1
            print list_user[x[0]]
            dict_user['uid'] = list_user[x[0]].replace('.txt', '')
            print dict_user['uid']
            information = Information.objects.get(uid=dict_user['uid'])
            dict_user['point'] = x[1]
            dict_user['username'] = information.username
            dict_user['content'] = bm.document[x[0]]
            dict_user['source'] = 'From:简介'
            list_user_intro.append(dict_user)
    for item in list_user_intro:
        print item
