# coding=utf-8
import json

import re
import simplejson
from django.contrib.auth import authenticate, login as user_login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from index.reserve_index import ReserveIndex
from init.server_local import start_recommend
from search.BM25 import Search
from vemax import BLL
from vemax.models import Information, UserRelationship, Users, Classify, Profiles, Friend
from django import forms
from crawler.weibo.loginModule import Login
from crawler.weibo.registerModule import Register
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class UserForm(forms.Form):
    """
        用户验证，判断是不是通过登录进入
    """
    username = forms.CharField(label='username:', error_messages={'required': 'Please input your username'},
                               max_length=100)
    password = forms.CharField(label='password:', error_messages={'required': 'Please input your password'},
                               widget=forms.PasswordInput())


r = Register()


def register_view(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            verification_code = request.POST['verification_code']
            db_user = Users()
            db_user.username = username
            db_user.pwd = password
            if BLL.User.sys_register(db_user, verification_code, r) == 1:
                return HttpResponseRedirect("init")
            else:
                r.get_args()
                return render_to_response('register.html', {"img_url": r.img})
    else:
        r.get_args()
        return render_to_response('register.html', {"img_url": r.img})


def init_view(request):
    return render_to_response('init.html')


l = Login()


def login_view(request):
    """
    １．前端往后台发送数据都是使用post方式传输，请求分为注册和登陆
    ２．分析前端的具体请求，返回相应页面给用户，如果是注册，则跳转到register页面，如果是登陆则跳转到homepage页面
    :param request:
    :return:
    """
    if request.method == 'POST':
        if request.POST.has_key('register'):  # 如果用户点击了"sign up"按钮,则说明用户选择注册页面
            return HttpResponseRedirect('register')
        else:
            uf = UserForm(request.POST)
            if uf.is_valid():
                username = uf.cleaned_data['username']
                password = uf.cleaned_data['password']
                user = authenticate(username=username, password=password)

                db_user = Users()
                db_user.username = username
                db_user.pwd = password
                is_user = BLL.User.sys_login(db_user)

                if is_user.count() == 1:
                    if user is None:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            user_login(request, user)
                    return HttpResponseRedirect('homepage')  # 重定向
    else:
        l.get_args()
        return render_to_response("login.html", {"img_url": l.img})


def logout_view(request):
    logout(request)
    # l.get_args()
    return render_to_response("login.html", {"img_url": l.img})


def homepage_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')  # 用户未登录，则重定向
    page = request.GET.get('page')
    if not page:
        page = 'relationship'  # 默认显示关系页面
    else:
        if page == 'information':
            if request.GET.get('username'):
                page = 'information?username=' + request.GET.get('username')
        elif page == 'search':
            if request.method == 'POST':
                search_text = request.POST['search_input']
                page = 'search?content=' + search_text
            else:
                if request.GET.get('content'):
                    page = 'search?content=' + request.GET.get('content')
        else:
            pass
    db_user = Users.objects.get(username=request.user.username)
    information = Information.objects.get(uid=db_user.uid)
    list_class_tags = re.split(',', information.class_tags)
    count = 0
    dict_class_tags = dict()
    for item in list_class_tags:
        count += 1
        dict_class_tags[count] = item
        if count == 3:
            break

    dict_recommend = start_recommend(db_user.uid)
    rec = dict()

    p = Profiles.objects.filter().order_by('-time')[0]
    p_info = Information.objects.get(uid=p.uid)
    rec['username'] = p_info.username
    str_recommend = p.content
    for item in dict_recommend:
        str_recommend = item['1']['content']
        rec['username'] = item['1']['username']
    rec['content'] = str_recommend

    return render_to_response("homepage.html",
                              {'name': information.username, 'intro': information.intro, 'html': page,
                               'recommend': rec, 'dict_class_tags': dict_class_tags})


def information_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')  # 重定向
    page = request.GET.get('username')
    if not page:
        db_user = Users.objects.get(username=request.user.username)
        information = Information.objects.get(uid=db_user.uid)
    else:
        information = Information.objects.get(username=page)
        db_user = Users.objects.get(uid=information.uid.uid)
    uid = db_user.uid
    profile = Profiles.objects.filter(uid=uid).order_by('cid')[0]

    list_bigV = UserRelationship.objects.filter(user_uid=uid, relationship='v')
    str_bigV = ''
    for item in list_bigV:
        friend_info = Information.objects.get(uid=item.friend_uid)
        str_bigV += friend_info.username + ','

    db_user_self = Users.objects.get(username=request.user.username)
    list_relation_classify = UserRelationship.objects.filter(user_uid=db_user_self.uid, friend_uid=uid)
    if list_relation_classify.count() == 0:
        relation_classify = '本人'
    else:
        relation_classify = list_relation_classify[0].relationship

    return render_to_response("information.html",
                              {'name': information.username, 'intro': information.intro, 'profile': profile.content,
                               'tags': information.tags, 'bigV': str_bigV, 'uid': uid,
                               'class_tags': information.class_tags, 'relation_classify': relation_classify})


def information_data(request):
    db_user = Users.objects.get(username=request.user.username)
    dict_user_info = BLL.User.show_information(uid=db_user.uid)
    result = simplejson.dumps(dict_user_info)
    return HttpResponse(result, content_type='application/javascript')


def relationship_view(request):
    db_user = Users.objects.get(username=request.user.username)
    list_close_friend_uid = UserRelationship.objects.filter(user_uid=db_user.uid)
    list_close_friend = list()
    for item in list_close_friend_uid:
        close_friend = Information.objects.get(uid=item.friend_uid)
        list_close_friend.append(close_friend)
    return render_to_response("relationship.html")


def relationship_data(request):
    db_user = Users.objects.get(username=request.user.username)
    dict_close_friend = BLL.Relationship.show_relationship(uid=db_user.uid)
    result = json.dumps(dict_close_friend)
    return HttpResponse(result, content_type='application/javascript')


def classify_view(request):  # 显示所有分类属性
    db_user = Users.objects.get(username=request.user.username)
    dict_user_info = BLL.User.show_information(uid=db_user.uid)
    dict_user_classify_friends = BLL.Relationship.show_classify(uid=db_user.uid)
    str_user_classify = ''
    for item in dict_user_classify_friends:
        str_user_classify += item + ','
    return render_to_response("classify.html",
                              {'uid': dict_user_info['uid'], 'name': dict_user_info['info']['name'],
                               'friends_classify': str_user_classify})


def classify_data(request):
    dict_classify = dict()
    db_user = Users.objects.get(username=request.user.username)
    dict_classify['uid'] = db_user.uid
    dict_classify['class'] = dict()
    for item in Classify.objects.filter():
        dict_classify['class'][item.class_name] = (item.id, item.img_url)
    result = json.dumps(dict_classify)
    return HttpResponse(result, content_type='application/javascript')


def classify_detail_view(request):
    db_user = Users.objects.get(username=request.user.username)
    page = request.GET.get('page')
    obj_class = Classify.objects.get(class_name=page)
    class_id = obj_class.id
    class_name = obj_class.class_name
    file_relation = '../static/image/d3/' + db_user.uid + str(class_id) + '.json'
    return render_to_response("interest.html",
                              {'interest': class_name, 'file_relation': file_relation})  # 向前端传输列表时需要先dumps


def friend_analyse(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        close_friend = request.POST['close_friend']
        db_user = Users.objects.get(uid=uid)
        db_friend = Friend()
        db_friend.uid = db_user
        db_friend.list_friend = str(close_friend)
        db_friend.save()
        return HttpResponse('success')
    else:
        return HttpResponse('fail')


def search_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')
    db_user = Users.objects.get(username=request.user.username)
    information = Information.objects.get(uid=db_user.uid)
    dict_recommend = start_recommend(db_user.uid)
    rec = dict()

    p = Profiles.objects.filter().order_by('-time')[0]
    p_info = Information.objects.get(uid=p.uid)
    rec['username'] = p_info.username
    str_recommend = p.content
    for item in dict_recommend:
        str_recommend = item['1']['content']
        rec['username'] = item['1']['username']
    rec['content'] = str_recommend
    page = request.GET.get('content')
    print page
    if page:
        search_text = page
        list_friend = UserRelationship.objects.filter(user_uid_id=db_user.uid)
        list_document = []  # 存储对应查询结果来源
        list_user = []  # 存储用户
        for item in list_friend:
            if item.relationship == 'v':
                pass
            else:
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
        bm = Search(obj_index_user, search_text)
        sorted_x = bm.rank_doc()
        list_user_all = []

        for x in sorted_x:
            if search_text in bm.document[x[0]]:
                dict_user = dict()
                print 'doc num:', x[0], 'point:', x[1], 'source:', list_user[x[0]]
                print bm.document[x[0]]
                print '--------'
                dict_user['uid'] = list_user[x[0]].replace('.txt', '')
                information = Information.objects.get(uid=dict_user['uid'])
                dict_user['point'] = x[1]
                dict_user['username'] = information.username
                dict_user['content'] = bm.document[x[0]]
                if x[0] == 1:
                    dict_user['source'] = 'From：简介'
                else:
                    dict_user['source'] = 'From：博文'
                list_user_all.append(dict_user)

        count = 0
        dict_user_all = dict()
        for item in list_user_all:
            count += 1
            dict_user_all[count] = item
            print item
        return render_to_response('search.html',
                                  {'name': information.username, 'intro': information.intro,
                                   'list_user': dict_user_all, 'recommend': rec})
    return render_to_response('search.html', {'name': information.username, 'intro': information.intro,
                                              'recommend': rec, 'hint': '请输入需要查询的内容！'})
