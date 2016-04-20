# coding=utf-8
__author__ = 'jgirl'

# 抽象类加抽象方法就等于面向对象编程中的接口
from abc import ABCMeta, abstractmethod


class InterfaceIndex(object):
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    @abstractmethod  # 抽象方法
    def addWordDict(self, user_profiles):
        pass

    @abstractmethod  # 抽象方法
    def addIndexDict(self, profile_words):
        pass

    @abstractmethod  # 抽象方法
    def updateIndex(self, user_words, users_profiles_index):
        pass
