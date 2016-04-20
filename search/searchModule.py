# coding=utf-8

import re


class Search:
    def __init__(self):
        pass

    @staticmethod
    def one_word_query(word, invertedIndex):  # 查询一个单词在哪些文档中
        if word in invertedIndex.keys():
            return [filename for filename in invertedIndex[word]]
        else:
            return []

    @staticmethod
    def free_text_query(self, string):
        pattern = re.compile('[\W_]+')
        string = pattern.sub(' ', string)
        result = []
        for word in string.split():
            result += self.one_word_query(word)
        return list(set(result))
