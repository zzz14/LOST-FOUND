from urllib.request import Request
from codex.baseerror import *
import os
import time
from time import mktime
from codex.baseview import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from wechat.models import Lost, Found, AdminLost, publisherIdToPlaces, User
from LostAndFound.settings import CONFIGS, STATIC_ROOT, get_url
import urllib.request
from wechat.wrapper import WeChatLib
#分词
#import sys
#sys.path.append('jieba/')
from userpage.jieba.jieba.analyse.textrank import TextRank
from userpage.jieba import jieba
#import jieba
#import jieba.analyse
#jieba.enable_parallel(15) # 开启并行分词模式，参数为并行进程数
jieba.set_dictionary('userpage/jieba/extra_dict/dict.txt.small')
jieba.load_userdict("userpage/jieba/userdict.txt") # file_name 为文件类对象或自定义词典的路径


# 点击“丢了东西”后出现的列表（被拾到东西的列表）
# 按界面设计，这里似乎应该删去key，contact，reward这些值
class FoundList(APIView):
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

#失物找领列表的搜索
class FoundListSearch(APIView):
    def divKey(self, contact1):
        count = 0
        inputKeyWord = list(TextRank.textrank(self.input['Content'], topK=25))
        contactKeyWord = list(TextRank.textrank(contact1, topK=25))
        for item1 in contactKeyWord:
            for item2 in inputKeyWord:
                if item1 == item2:
                    count += 1
                    print(item1)
        return count

    @property
    def get(self):
        items = []
        keys = list(TextRank.textrank(self.input['Content'], topK=25))
        result = {}
        for found in Found.objects.filter(status=0):
            temp = {}
            temp['name'] = found.name
            temp['key'] = found.key
            temp['contact'] = found.contact
            temp['description'] = found.description
            temp['foundTime'] = found.foundTime
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            if self.divKey(found.contact) > 0:
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


# 学校失物招领处失物列表
# 内容还没写
class SchoolOfficeLostList(APIView):
    def get(self):
        items = []
        for lost in AdminLost.objects.filter(status=0):
            temp = {}
            temp['id'] = lost.id
            temp['place'] = publisherIdToPlaces[lost.id]
            temp['type'] = lost.type
            temp['publishTime'] = mktime(lost.publishTime.timetuple())
            temp['picUrl'] = lost.picUrl
            items.append(temp)
        return items


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
        lost = Lost.objects.get(id=self.input('id'))
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
        for lost in AdminLost.objects.GET(id = self.input['id']):
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
            getData['access_token'] = CONFIGS['WECHAT_TOKEN']
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
            getData['access_token'] = CONFIGS['WECHAT_TOKEN']
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
