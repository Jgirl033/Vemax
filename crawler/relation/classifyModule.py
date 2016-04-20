# coding:utf-8
from crawler.user.infoModule import UserMessage


class FriendAnalyse:
    def __init__(self):
        pass

    @staticmethod
    def get_friend_info(close_friend):
        """
        爬取亲密好友资料
        :param close_friend: 亲密好友列表,数据格式:(uid，亲密度)
        :return:亲密好友资料列表([(id,(昵称，性别，地区，生日，感情状况，简介，认证信息，教育信息，工作信息),亲密度)])
        """
        friend_list = []
        for i in close_friend:
            print i
            fr = UserMessage(i[0])
            cf_list = (i[0],  # 好友id
                       (fr.get_name(), fr.get_sex(), fr.get_address(), fr.get_birthday(),
                        fr.get_feel(), fr.get_intro(), fr.get_cer_message(),
                        fr.get_study_experience(), fr.get_work_experience()),  # 资料
                       float(i[1]) / 3)  # 亲密度
            friend_list.append(cf_list)
        return friend_list

    @staticmethod
    def get_user_info(uid):
        """
        通过登陆其他帐号，将用户作为一般好友爬取资料,跟好友的数据格式统一，亲密度为0
        :param uid: 用户uid
        :return:用户资料列表（[(id,(昵称，性别，地区，生日，感情状况，简介，认证信息，教育信息，工作信息),亲密度（0）)]）
        """
        return FriendAnalyse.get_friend_info([(uid, 0)])


class FriendClassify:
    def __init__(self):
        pass

    @staticmethod
    def relation(sextype):

        """
        根据性别分类
        :param sextype: 性别
        :return:返回分类
        """
        if sextype == '男':
            return '基友'
        elif sextype == '女':
            return '闺蜜'
        else:
            return '好友'

    @staticmethod
    def add_group(friends, result):
        """
        根据分类把好友添加到对应的组
        :param friends: 好友列表
        :param result: 分类字典
        :return:返回分类字典
        """
        for i in friends[:4]:
            fri_relation = FriendClassify.relation(i[1][1])
            sex_type = fri_relation
            if sex_type == '基友':
                result['基友'].append(i)
            elif sex_type == '闺蜜':
                result['闺蜜'].append(i)
            else:
                result['好友'].append(i)
        return result

    @staticmethod
    def result_print(result):
        """
        输出各分类好友名字
        :param result: 分类字典
        :return:
        """
        print '_____同学______'
        for i in result['同学']:
            print i[1][0]
        print '_____同事______'
        for i in result['同事']:
            print i[1][0]
        print '_____同乡______'
        for i in result['同乡']:
            print i[1][0]
        print '_____基友______'
        for i in result['基友']:
            print i[1][0]
        print '_____闺蜜______'
        for i in result['闺蜜']:
            print i[1][0]
        print '_____好友______'
        for i in result['好友']:
            print i[1][0]

    @staticmethod
    def relation_sort(user, friends):
        """
        :param user:    list  [id,(0.昵称，1.性别,2.地区,3.生日,4.感情状况,5.简介,6.认证信息,7.教育信息,8.工作信息),亲密度]
        :param friends: list  [friend0,friend1,....]
        :return result: dict  分类结果
        """
        result = {'同学': [], '同事': [], '基友': [], '闺蜜': [], '同乡': [], '好友': []}
        result = FriendClassify.add_group(friends, result)

        user_school = user[0][1][7].split('·')
        user_company = (user[0][1][8].split(';'))[0]
        user_hometown = user[0][1][2]
        for i in range(len(user_school)):
            user_school[i] = (user_school[i].split(';'))[0]
        friends_school = []
        friends_company = []
        friends_hometown = []
        friends = friends[4:]
        for friend in friends:
            friend_school = friend[1][7].split('·')
            for i in range(len(friend_school)):
                friend_school[i] = (friend_school[i].split(';'))[0]
            friends_school.append(friend_school)
            friends_company.append(friend[1][8].split(';')[0])
            friends_hometown.append(friend[1][2])

        for i in range(len(friends)):
            sth_store = friends[i]  # 设定字典的存储的元素
            if user_company == friends_company[i] and friends_company[i] != '':
                result['同事'].append(sth_store)
            else:
                for school in user_school:
                    if school in friends_school[i] and sth_store not in result['同学']:  # 若好友为同事，则不再分到同学
                        result['同学'].append(sth_store)  # 存名字
            if user_hometown == friends_hometown[i] and sth_store not in result['同事'] and sth_store not in result['同学']:
                result['同乡'].append(sth_store)
            if sth_store not in result['同事'] and sth_store not in result['同学'] and sth_store not in result['同乡']:
                result['好友'].append(sth_store)
        FriendClassify.result_print(result)
        return result
