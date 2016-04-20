# coding=utf-8

"""
filename=interest_classify
author=Adien
date written=01/13/2015
date modify=01/23/2015
program purpose=对好友进行兴趣分类
description=加载训练集与测试集,特征提取,建立分类模型, 预测测试属性
"""
import django
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import HashingVectorizer
from extractKeysModule import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


class UserClassify:  # 针对特定微博用户对其进行归类
    def __init__(self):
        self.category = ['健康养生', '军事历史', '时政', '公益', '阅读', '电视剧', 'IT科技',
                         '教育', '艺术', '电影', '漫画', '游戏', '旅游', '美食', '摄影', '萌宠',
                         '服装美容', '体育', '设计', '综艺', '星座', '音乐', '健身', '财经']

    @staticmethod
    def load_train_set():
        """
        function:读入训练集
        :return:    list    训练集
        """
        set_train = []  # 训练集
        for item in range(1, 25):
            project_path = globalModule.get_project_path()
            txt_path = project_path + '/classify/classlib/'
            f = open(txt_path + str(item) + '.txt')  # 类别库文件地址
            set_train.append(f.read())
        return set_train

    def category_sort(self, classify_result):
        """
        function:对分类结果排序
        :param classify_result:   list    通过SVM算法所得到的好友对各分类的权值
        :return:                  list[3] 排序后最匹配的三种兴趣
        """
        tag = []
        tag[:] = self.category[:]
        n = len(tag) - 1
        for i in range(len(tag) - 1):
            for j in range(n):
                if classify_result[j + 1] < classify_result[j]:
                    r = classify_result[j + 1]
                    t = tag[j + 1]
                    classify_result[j + 1] = classify_result[j]
                    tag[j + 1] = tag[j]
                    classify_result[j] = r
                    tag[j] = t
            n -= 1
        return_num = 0
        for k in range(len(classify_result)):
            if classify_result[k] < 0.0414:
                return_num = k + 1
            else:
                break
        if return_num > 3:
            return_num = 3
        if return_num == 0:
            return_num = 1
        return tag[:return_num]

    def feature_extraction(self, test):
        """
        function:特征提取
        :param test:
        :return:训练特征,测试特征
        """
        train = self.load_train_set()
        vectorizer = HashingVectorizer(stop_words='english', non_negative=True, n_features=25000)
        fea_train = vectorizer.fit_transform(train)  # 特征提取
        fea_test = vectorizer.fit_transform(test)  # 特征提取
        return fea_train, fea_test

    def svm(self, test):
        """
        :param test:   list      测试集包含各好友以及他们所关注大V的标签
        :return:       list[][]   返回若干个兴趣
        """
        fea_train, fea_test = self.feature_extraction(test)
        type_train = []
        for item in range(1, len(self.category) + 1):
            type_train.append(item)
        svclf0 = SVC(kernel='linear', probability=True)
        svclf0.fit(fea_train, type_train)  # 训练分类器
        classification_result = svclf0.predict_proba(fea_test)
        return classification_result

    def bayes(self, test):
        """
        :param test:   list      测试集包含各好友以及他们所关注大V的标签
        :return:       list[][3] 测试集最匹配的三个兴趣
        """
        fea_train, fea_test = self.feature_extraction(test)
        category_train = []
        for k in range(1, len(self.category) + 1):
            category_train.append(k)
        clf = MultinomialNB(alpha=0.8)
        clf.fit(fea_train, category_train)
        classification_result = clf.predict_proba(fea_test)
        return classification_result

    def classify(self, str_tags, user_profiles, list_bigV_tags):
        """
        :param list_bigV_tags: 用户关注的大V所对应标签，标签是string，以'/'分割
        :param str_tags:
        :param user_profiles:    list     用户转发的博文
        :return interest        list
        """
        p = ''
        for profile in user_profiles:
            p += profile
        user_profiles = extract_keywords(p, 15)
        user_profiles = '`'.join(user_profiles) + '`'
        t = ''
        big_v_tags = t.decode('utf-8')
        user_tags_result = self.svm([str_tags]) * 0.5
        user_profile_result = self.svm([user_profiles]) * 0.1
        big_v_tags_result = self.svm([big_v_tags]) * 0.4
        print user_profile_result
        print big_v_tags_result
        result = user_profile_result + user_tags_result + big_v_tags_result
        interest = self.category_sort(list(result)[0])
        return interest
