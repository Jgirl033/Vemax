#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-4-6 下午10:26
    @function:
"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()
from vemax.models import Users


def get_project_path():
    project_path = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    return project_path.replace('/init', '')


def is_start_crawler():
    """
    判断是否启动爬虫系统
    :return: 如果是0,则不启动,否则,则启动
    """
    list_users = Users.objects.filter(is_crawler=False)
    if list_users.count() == 0:
        return 0
    else:
        return list_users


def is_start_classify():
    """
    判断是否启动好友分类系统
    :return: 如果是0,则不启动,否则,则启动
    """
    list_users = Users.objects.filter(is_register=True, is_crawler=True, is_classify=False)
    if list_users.count() == 0:
        return 0
    else:
        return list_users


def is_exist(uid):
    """
    判断用户是不是已经在数据库中
    :type uid: str
    :param uid: 用户微博id
    :return: 如果是0,则说明用户不在库中,如果是1,则说明用户在库中
    """
    list_user = Users.objects.filter(uid=uid)
    if list_user.count() == 0:
        return 0
    else:
        return 1
