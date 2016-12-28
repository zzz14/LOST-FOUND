import os
import time
from time import mktime
from codex.baseview import APIView
from django.conf import settings
from wechat.models import Lost, Found, AdminLost, publisherIdToPlaces, adminLostType, User
from LostAndFound.settings import CONFIGS, STATIC_ROOT, get_url
import urllib.request
from wechat.wrapper import WeChatLib
#分词
#import sys
#sys.path.append('jieba/')
from jieba.jieba.analyse.textrank import TextRank
from jieba import jieba

#import jieba
#import jieba.analyse
#jieba.enable_parallel(15) # 开启并行分词模式，参数为并行进程数
jieba.set_dictionary('jieba/extra_dict/dict.txt.small')
jieba.load_userdict("jieba/userdict.txt") # file_name 为文件类对象或自定义词典的路径


# 点击“丢了东西”后出现的列表（被拾到东西的列表）
# 按界面设计，这里似乎应该删去key，contact，reward这些值
class FoundList(APIView):
    def get(self):
        items = []
        for found in Found.objects.filter(status=0):
            temp = {}
            temp['id'] = found.id
            temp['name'] = found.name
            temp['contacts'] = found.contacts
            temp['contactNumber'] = found.contactNumber
            temp['contactType'] = found.contactType
            temp['description'] = found.description
            temp['foundTime'] = mktime(found.foundTime.timetuple())
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            items.append(temp)
        items.sort(key=lambda x: x["foundTime"])
        return items

#失物招领列表的搜索
class FoundListSearch(APIView):
    def divKey(self, contact1):
        count = 0
        inputKeyWord = list(jieba.analyse.extract_tags(self.input['Content'], topK=25))
        contactKeyWord = list(jieba.analyse.extract_tags(contact1, topK=25))
        for item1 in contactKeyWord:
            for item2 in inputKeyWord:
                if item1 == item2:
                    count += 1
                    print(item1)
        return count


    def get(self):
        self.check_input('Content')

        items = []
        guanjianzi = list(jieba.analyse.extract_tags("黑色的钱包", topK=25))
        print(guanjianzi)
        keys = list(jieba.analyse.extract_tags(self.input['Content'], topK=25))
        print(keys)
        result = {}
        for found in Found.objects.filter(status=0):
            temp = {}
            temp['id'] = found.id
            temp['name'] = found.name
            temp['contacts'] = found.contacts
            temp['contactNumber'] = found.contactNumber
            temp['contactType'] = found.contactType
            temp['description'] = found.description
            temp['foundTime'] = mktime(found.foundTime.timetuple())
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            if self.divKey(found.contacts) > 0:
                items.append(temp)
                result['keys'] = keys
                result['items'] = items
        items.sort(key=lambda x: x["foundTime"])
        return result


# 点击“捡了东西”后出现的列表（丢失物品的列表）
class LostList(APIView):
    def get(self):
        items = []
        for lost in Lost.objects.filter(status=0):
            temp = {}
            temp['id'] = lost.id
            temp['name'] = lost.name
            temp['description'] = lost.description
            temp['lostTime'] = mktime(lost.lostTime.timetuple())
            temp['lostPlace'] = lost.lostPlace
            temp['picUrl'] = lost.picUrl
            if lost.latitude != 0:
                temp['lat'] = lost.latitude
            if lost.longitude != 0:
                temp['lng'] = lost.longitude
            items.append(temp)
        items.sort(key=lambda x: x["lostTime"])
        return items


# 学校失物招领处失物列表
class SchoolOfficeLostList(APIView):
    def get(self):
        items = []
        losts = AdminLost.objects.filter(publishTime__gte=self.input['startDate'])
        print(self.input['startDate'])
        print(self.input['endDate'])
        losts = losts.exclude(publishTime__gte=self.input['endDate'])
        if 'type' in self.input and\
            self.input['type'] != "" and\
            'publisherId' in self.input and\
            self.input['publisherId'] != '0':
            for lost in losts.filter(status=0,type=self.input['type'],publisherId=self.input['publisherId']):
                picUrl = lost.picUrl.split(';')
                picUrl.pop()
                for url in picUrl:
                    temp = {}
                    temp['id'] = lost.id
                    temp['place'] = publisherIdToPlaces[lost.publisherId]
                    temp['type'] = lost.type
                    temp['publishTime'] = time.strftime("%Y-%m-%d", lost.publishTime.timetuple())
                    temp['picUrl'] = url
                    items.append(temp)
        elif 'type' in self.input and\
            self.input['type'] != "":
            print(2)
            for lost in losts.filter(status=0,type=self.input['type']):
                picUrl = lost.picUrl.split(';')
                picUrl.pop()
                for url in picUrl:
                    temp = {}
                    temp['id'] = lost.id
                    temp['place'] = publisherIdToPlaces[lost.publisherId]
                    temp['type'] = lost.type
                    temp['publishTime'] = time.strftime("%Y-%m-%d", lost.publishTime.timetuple())
                    temp['picUrl'] = url
                    items.append(temp)
        elif 'publisherId' in self.input and\
            self.input['publisherId'] != '0':
            print(self.input['publisherId'])
            for lost in losts.filter(status=0,publisherId=self.input['publisherId']):
                picUrl = lost.picUrl.split(';')
                picUrl.pop()
                for url in picUrl:
                    temp = {}
                    temp['id'] = lost.id
                    temp['place'] = publisherIdToPlaces[lost.publisherId]
                    temp['type'] = lost.type
                    temp['publishTime'] = time.strftime("%Y-%m-%d", lost.publishTime.timetuple())
                    temp['picUrl'] = url
                    items.append(temp)
        else:
            print(4)
            for lost in losts.filter(status=0):
                picUrl = lost.picUrl.split(';')
                picUrl.pop()
                for url in picUrl:
                    temp = {}
                    temp['id'] = lost.id
                    temp['place'] = publisherIdToPlaces[lost.publisherId]
                    temp['type'] = lost.type
                    temp['publishTime'] = time.strftime("%Y-%m-%d", time.localtime(lost.publishTime))
                    temp['picUrl'] = url
                    items.append(temp)
        items.sort(key=lambda x: x["place"])
        info = {}
        info['typeList'] = adminLostType
        info['placeList'] = list(publisherIdToPlaces.values())
        info['items'] = items
        return info


# “我的失物”界面，列表中系显示我发出且未删除的失物信息
# 前端须返回输入user
class MineLost(APIView):
    def get(self):
        items = []
        for lost in Lost.objects.filter(user=self.input['user'], status=0):
            temp = {}
            temp['name'] = lost.name
            temp['contacts'] = lost.contacts
            temp['contactNumber'] = lost.contactNumber
            temp['contactType'] = lost.contactType
            temp['description'] = lost.description
            temp['lostTime'] = mktime(lost.lostTime.timetuple())
            temp['lostPlace'] = lost.lostPlace
            temp['picUrl'] = lost.picUrl
            temp['reward'] = lost.reward
            items.append(temp)
        items.sort(key=lambda x: x["lostTime"])
        return items


# “我的拾物”界面，列表中系显示我发出且未删除的拾物信息
# 前端须返回输入user
class MineFound(APIView):
    def get(self):
        items = []
        for found in Found.objects.filter(status=0):
            temp = {}
            temp['name'] = found.name
            temp['contacts'] = found.contacts
            temp['contactNumber'] = found.contactNumber
            temp['contactType'] = found.contactType
            temp['description'] = found.description
            temp['foundTime'] = mktime(found.foundTime.timetuple())
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            items.append(temp)
        items.sort(key=lambda x: x["foundTime"])
        return items


# 删除我发布的失物信息
# 需提供信息的id
class DeleteMineLost(APIView):
    def get(self):
        Lost.objects.filter(id=self.input['id']).update(status=1)


# 删除我发布的失物信息
# 需提供信息的id
class DeleteMineFound(APIView):
    def get(self):
        Found.objects.filter(id=self.input['id']).update(status=1)


# 拾物详情页
# 需提供拾物的id
class FoundDetail(APIView):
    def get(self):
        found = Found.objects.get(id=self.input('id'))
        temp = {}
        temp['name'] = found.name
        temp['contact'] = found.contact
        temp['contactType'] = found.contactType
        temp['contactNumber'] = found.contactNumber
        temp['description'] = found.description
        temp['lostTime'] = mktime(found.foundTime.timetuple())
        temp['lostPlace'] = found.foundPlace
        temp['picUrl'] = found.picUrl
        return temp

# 失物详情页
# 需提供失物的id
class LostDetail(APIView):
    def get(self):
        self.check_input('id')
        lost = Lost.objects.get(id=self.input['id'])
        temp = {}
        temp['name'] = lost.name
        temp['contacts'] = lost.contacts
        temp['contactNumber'] = lost.contactNumber
        temp['contactType'] = lost.contactType
        temp['description'] = lost.description
        temp['lostTime'] = mktime(lost.lostTime.timetuple())
        temp['lostPlace'] = lost.lostPlace
        temp['picUrl'] = lost.picUrl
        temp['reward'] = lost.reward
        return temp


# 失物招领处失物详情页
# 需提供失物的id
class AdminLostDetail(APIView):
    def get(self):
        items = []
        self.check_input('id')
        for lost in AdminLost.objects.get(id = self.input['id']):
            temp = {}
            temp['id'] = lost.id
            temp['place'] = publisherIdToPlaces[lost.id]
            temp['type'] = lost.type
            temp['publishTime'] = mktime(lost.publishTime.timetuple())
            temp['picUrl'] = lost.picUrl
            items.append(temp)
        return items

# 新建失物信息的界面
class NewLost(APIView):
    def post(self):
        self.check_input('name', 'contacts', 'contactType', 'contactNumber',\
                         'description', 'lostTime', 'lostPlace', 'reward')
        user = User.get_by_openid(self.input['user'])
        lost = Lost(name=self.input['name'],
                    description=self.input['description'],
                    contacts=self.input['contacts'],
                    contactNumber = self.input['contactNumber'],
                    contactType = self.input['contactType'],
                    lostTime=self.input['lostTime'],
                    lostPlace=self.input['lostPlace'],
                    reward=self.input['reward'],
                    user=user,
                    status=0)
        if 'lng' in self.input:
            lost.longitude = self.input['lng']
        if 'lat' in self.input:
            lost.latitude = self.input['lat']
        if 'media_id' in self.input:
            getData = {}
            getData['access_token'] = WeChatLib.get_wechat_access_token()
            getData['media_id'] = self.input['media_id']
            data = urllib.parse.urlencode(getData)
            url = "https://api.weixin.qq.com/cgi-bin/media/get?" + data
            pic = urllib.request.urlopen(url)
            pic_name = self.input['media_id']+'.jpg'
            pic_path = os.path.join('img','lost',pic_name)
            pic_full_path = os.path.join(STATIC_ROOT,pic_path)
            lost.picUrl = get_url(pic_path)
            f = open(pic_full_path, 'wb')
            # TODO
            f.write(pic.read())
            f.close()
        lost.save()

# 新建拾物信息的界面
class NewFound(APIView):
    def post(self):
        self.check_input('name', 'contacts', 'contactType', 'contactNumber', 'description', 'foundTime', 'foundPlace', 'reward')
        found = Found(name=self.input['name'],
                      description=self.input['description'],
                      contacts=self.input['contacts'],
                      contactNumber=self.input['contactNumber'],
                      contactType=self.input['contactType'],
                      foundTime=self.input['foundTime'],
                      foundPlace=self.input['foundPlace'],
                      user=self.user.open_id,
                      status=0)
        if 'lng' in self.input:
            found.longitude = self.input['lng']
        if 'lat' in self.input:
            found.latitude = self.input['lat']
        if 'media_id' in self.input:
            getData = {}
            getData['access_token'] = WeChatLib.get_wechat_access_token()
            getData['media_id'] = self.input['media_id']
            data = urllib.parse.urlencode(getData)
            url = "https://api.weixin.qq.com/cgi-bin/media/get?" + data
            pic = urllib.request.urlopen(url)
            f = open(self.input['media_id'] + ".jpg", 'wb')
            f.write(pic.read())
            f.close()
            found.picUrl = settings.STATIC_ROOT + '/img/lostAndFound/found/' + str(self.input['media_id'])
        found.save()

class WxConfig(APIView):
    def get(self):
        config = WeChatLib.get_wechat_wx_config(self.input['url'])
        return config
