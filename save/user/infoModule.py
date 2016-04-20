# coding=utf-8

import Image
from PIL import ImageDraw
import urllib
import django
import os
from init import globalModule
from vemax.models import Information, Users
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vemax.settings")  # 环境设置必须在引用models前
django.setup()


class UserSave:
    def __init__(self):
        pass

    @staticmethod
    def save_users(dict_user):
        """
        用户注册时,存储用户的微博账号和密码和id
        爬取用户好友时,获得新的用户账号,存储好友的微博账号和id,密码使用默认形式888888
        :param dict_user:
        :return: 如果存储成功,返回 0,否则返回 1
        """
        u = Users()
        u.username = dict_user['username']
        u.uid = dict_user['uid']
        u.pwd = dict_user['password']
        try:
            u.save()
            return 0
        except:
            return 1


class InfoSave:
    def __init__(self):
        pass

    @staticmethod
    def save_intro_tags(user_info):
        uid = user_info['uid']
        information = Information()
        information.uid = Users.objects.get(uid=uid)
        information.username = user_info['info']['name']
        information.sex = user_info['info']['sex']
        information.intro = user_info['info']['intro']
        information.image_url = user_info['info']['img']
        information.tags = user_info['info']['tags']
        information.address = user_info['info']['address']
        information.birthday = user_info['info']['birthday']
        if not user_info['info'].has_key('V'):
            information.user_class = 'N'
        else:
            information.user_class = 'Y'
        information.is_organization = user_info['info']['organization']
        information.study_experience = user_info['info']['study']
        information.work_experience = user_info['info']['work']
        InfoSave.save_circle_img(uid, user_info['info']['img'])
        try:
            information.save()
            return 0
        except:
            return 1

    @staticmethod
    def save_circle_img(uid, img_url):
        path_img = globalModule.get_project_path() + '/static/image/user/' + uid + ".png"
        while True:
            try:
                urllib.urlretrieve(img_url, path_img)
                break
            except:
                continue
        img = Image.open(path_img).convert("RGBA")
        size = img.size
        r2 = min(size[0], size[1])
        if size[0] != size[1]:
            img = img.resize((r2, r2), Image.ANTIALIAS),
        circle = Image.new('L', (r2, r2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, r2, r2), fill=255)
        alpha = Image.new('L', (r2, r2), 255)
        alpha.paste(circle, (0, 0))
        img.putalpha(alpha)
        img.save(globalModule.get_project_path() + '/static/image/user_circle/%s.png' % uid)
