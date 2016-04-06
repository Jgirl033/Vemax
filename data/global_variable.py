#!/usr/bin/env python
# coding: utf-8

"""
    @author: Jgirl
    @time: 16-4-6 下午10:26
    @function:
"""
import os


def get_project_path():
    project_path = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    return project_path.replace('/data','')


