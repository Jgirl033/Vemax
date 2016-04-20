# coding=utf-8
import jieba
import jieba.analyse
import jieba.posseg as pseg

from init import globalModule


class ExtractKeys:
    def __init__(self):
        pass

    @staticmethod
    def get_stopwords():  # 将停用词表的停用词加载到变量中
        project_path = globalModule.get_project_path()
        txt_path = project_path + '/classify/stopwords.txt'
        file_stopwords = open(txt_path, 'r')
        list_stopwords = []
        lines = file_stopwords.readlines()
        for word in lines:
            list_stopwords.append(word.decode('utf-8'))
        return list_stopwords

    @staticmethod
    def cut_words(list_words):
        list_new_words = []
        for word in list_words:
            if word.__len__() >= 2:
                list_new_words.append(word)
        return list_new_words

    @staticmethod
    def cut_words_with_speech(sentence):
        words = pseg.cut(sentence)
        list_words = []
        for word in words:
            if 'n' in word.flag:
                list_words.append(word.word)
        return list_words

    @staticmethod
    def get_extractwords(list_words, num=None):
        if num is None:
            num = len(list_words) / 50
        sentence = ','.join(list_words)
        words = jieba.analyse.extract_tags(sentence, num)
        list_words = []
        for w in words:
            list_words.append(w)
        return list_words

    @staticmethod
    def delete_stopwords(stopwords, list_word):  # 删除句子中的停用词成分
        list_keywords = []
        for word in list_word:
            if word not in stopwords:
                list_keywords.append(word)
        return list_keywords


def extract_keywords(sentence, num):
    """

    :param sentence:需要进行关键词提取的文本
    :param num:提取的关键词的数量
    :return:关键词列表
    """
    stopwords = ExtractKeys.get_stopwords()
    words = ExtractKeys.cut_words(ExtractKeys.cut_words_with_speech(sentence))
    list_words = ExtractKeys.delete_stopwords(stopwords, words)
    list_extractwords = ExtractKeys.get_extractwords(list_words, num)
    return list_extractwords
