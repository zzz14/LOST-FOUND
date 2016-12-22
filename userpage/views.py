from urllib.request import Request

from codex.baseerror import *
import os

from codex.baseview import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from wechat.models import Lost, Found, User
from LostAndFound.settings import CONFIGS
import urllib.request
from wechat.wrapper import WeChatLib

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
            temp['foundTime'] = found.foundTime
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            items.append(temp)
        items.sort(key=lambda x: x["foundTime"])
        return items


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
            temp['lostTime'] = lost.lostTime
            temp['lostPlace'] = lost.lostPlace
            temp['picUrl'] = lost.picUrl
            temp['reward'] = lost.reward
            items.append(temp)
        items.sort(key=lambda x: x["lostTime"])
        return items


# 学校失物招领处失物列表
# 内容还没写
class SchoolOfficeLostList(APIView):
    def post(self):
        return


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
            temp['lostTime'] = lost.lostTime
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
            temp['foundTime'] = found.foundTime
            temp['foundPlace'] = found.foundPlace
            temp['picUrl'] = found.picUrl
            items.append(temp)
        items.sort(key=lambda x: x["foundTime"])
        return items


# 删除我发布的失物信息
# 需提供信息的id
class DeleteMineLost(APIView):
    def get(self):
        Lost.objects.filter(id=self.input['id']).update(status=1);


# 删除我发布的失物信息
# 需提供信息的id
class DeleteMineFound(APIView):
    def get(self):
        Found.objects.filter(id=self.input['id']).update(status=1);


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
        temp['lostTime'] = found.foundTime
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
        temp['lostTime'] = lost.lostTime
        temp['lostPlace'] = lost.lostPlace
        temp['picUrl'] = lost.picUrl
        temp['reward'] = lost.reward
        return temp


# 新建失物信息的界面
class NewLost(APIView):
    def post(self):
        self.check_input('name', 'contacts', 'contactType', 'contactNumber',\
                         'description', 'lostTime', 'lostPlace', 'reward','user')
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
            url = "https://api.weixin.qq.com/cgi-bin/media"
            getData = {}
            getData['access_token'] = CONFIGS['WECHAT_TOKEN']
            getData['media_id'] = self.input['media_id']
            req = Request(url=url, data=getData)
            f = urllib.request.urlopen(req, timeout=120)
            picUrl = '/img/lostAndFound/' + str(
            len(os.listdir(settings.STATIC_ROOT + '/img/lostAndFound/'))) + '_' + data.name
            path = default_storage.save(settings.STATIC_ROOT + picUrl, ContentFile(data.read()))
            os.path.join(settings.MEDIA_ROOT, path)
            return CONFIGS['SITE_DOMAIN'] + picUrl
        lost.save()


# 新建拾物信息的界面
class NewFound(APIView):
    def post(self):
        found = Found(name=self.input['name'],
                      key=self.input['key'],
                      description=self.input['description'],
                      contact=self.input['contact'],
                      foundTime=self.input['foundTime'],
                      foundPlace=self.input['foundPlace'],
                      longitude=self.input['lng'],
                      latitude=self.input['lat'],
                      user=self.input['user'],
                      picUrl=self.input['picUrl'],
                      status=0)
        found.save()

# 图片上传
class uploadImage(APIView):
    def post(self):
        data = self.input['image_id']
        picUrl = '/img/lostAndFound/' + str(len(os.listdir(settings.STATIC_ROOT+'/img/lostAndFound/'))) + '_' + data.name
        path = default_storage.save(settings.STATIC_ROOT + picUrl, ContentFile(data.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        return CONFIGS['SITE_DOMAIN'] + picUrl

class WxConfig(APIView):
    def get(self):
        config = WeChatLib.get_wechat_wx_config(self.input['url'])
        return config