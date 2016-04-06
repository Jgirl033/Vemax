# coding=utf-8
from django.db import models


# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50, null=True)  # 微博用户名
    uid = models.CharField(max_length=15, primary_key=True)  # 微博用户唯一的识别id
    pwd = models.CharField(max_length=20)  # 微博密码
    is_register = models.BooleanField(default=False)  # 用户在库是否已经登录过
    is_crawler = models.BooleanField(default=False)  # 用户在库是否已经爬过
    is_classify = models.BooleanField(default=False)

    def __unicode__(self):
        return self.uid


class Information(models.Model):
    uid = models.OneToOneField(Users)  # 外键是User用户uid
    username = models.CharField(max_length=50)
    image_url = models.URLField()  # 头像链接的路径
    sex = models.CharField(max_length=5)  # 男，女或空值
    birthday = models.CharField(max_length=20)  # 不能是日期，因为有的生日显示星座
    address = models.CharField(max_length=100)
    intro = models.TextField()
    tags = models.CharField(max_length=100)
    work_experience = models.TextField(null=True)
    study_experience = models.TextField()
    user_degree = models.CharField(max_length=5)  # 是不是大V
    user_class = models.CharField(max_length=50)  # 经过分类算法得出的用户类别
    class_tags = models.CharField(max_length=50, null=True)
    is_organization = models.BooleanField()  # 用户是个人还是组织

    def __unicode__(self):
        return self.username


class Friend(models.Model):
    uid = models.OneToOneField(Users)
    list_friend = models.CharField(max_length=5000, null=True)

    def __unicode__(self):
        return self.uid.uid


class UserRelationship(models.Model):
    user_uid = models.ForeignKey(Users)  # 外键是User用户uid
    friend_uid = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20)
    degree = models.FloatField()
    is_follow = models.BooleanField(default=False)  # user follows friend
    is_fans = models.BooleanField(default=False)  # friend follows user

    class Meta:
        unique_together = ("user_uid", "friend_uid")

    def __unicode__(self):
        return self.user_uid.uid


class Profiles(models.Model):
    uid = models.ForeignKey(Users)  # 外键是User用户uid
    cid = models.CharField(max_length=10)
    content = models.TextField()
    time = models.DateField()
    like_count = models.IntegerField()
    forward_count = models.IntegerField()
    comment_count = models.IntegerField()

    class Meta:
        unique_together = ("uid", "cid")

    def __unicode__(self):
        return self.uid.uid


class Classify(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    class_name = models.CharField(max_length=10)
    img_url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.class_name
