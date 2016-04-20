# coding=utf-8
import os
import re
import jieba


def load_dataset(filename):
    datafile = open(filename)
    document = datafile.readlines()
    return document


def load_fileset(folder):
    """
    function: 从好友的文件夹中加载数据，形成documents（微博总和）和list_document（微博归档）
    :param folder:
    :return: documents , list_document
    """
    files = os.listdir(folder)
    documents = []
    list_document = []
    for item in files:
        filename = folder + '/' + item
        weibo_file = open(filename, 'r')
        data = weibo_file.read()
        li = data.split('`')
        number = li.__len__()
        for i in range(0, number, 1):
            list_document.append(str(item).replace('.txt', ''))
            documents.append(li[i])
    return documents, list_document


class ReserveIndex:
    def __init__(self, document):
        self.document = document  # document是一个文件列表, 每一个元素代表一个文件,即一条微博
        self.set_words = ()
        self.dict_words = dict()
        self.get_word_set()
        self.get_word_index()

    @staticmethod
    def remove_emoji(sentence):
        """
        function: 去除表情词
        :param sentence:
        :return: sentence
        """
        return re.sub('\[.*?\]', '', sentence)

    def get_word_set(self):
        """
        function: 分词,获得词语集合
        :return:
        """
        list_word = list()
        for doc in self.document:
            sentence = self.remove_emoji(doc)
            words = jieba.cut(sentence)
            for word in words:
                list_word.append(word.encode('utf-8'))
        self.set_words = set(list_word)

    def get_word_index(self):
        """
        function:建立倒排索引
        :return:
        """
        for word in self.set_words:
            self.dict_words[word] = ()
            list_words = list()
            for doc in self.document:
                if word in doc:
                    list_words.append(self.document.index(doc))
            self.dict_words[word] = list_words

    def save_word_index(self, filename):
        """
        function:将倒排索引存储在某个特定的文件
        :param filename:
        :return:
        """
        file_obj = open(filename, 'wb')
        for word in self.dict_words:
            string = word + ':'
            for i in self.dict_words[word]:
                string = string + str(i) + '`'
            string += '\n'
            file_obj.write(string)
        file_obj.close()
        print 'ok'

    def query(self, word):
        """
        function:查询,有就返回文件列表,无则返回空值
        :param word:
        :return:
        """
        if word.encode('utf-8') not in self.dict_words:
            return None
        list_query = self.dict_words[word.encode('utf-8')]
        return list_query
