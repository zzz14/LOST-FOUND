from codex.baseerror import *
from codex.baseview import APIView
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from wechat.models import Lost, Found, User
from LostAndFound.settings import CONFIGS
from wechat.wrapper import WeChatLib


# 点击“丢了东西”后出现的列表（被拾到东西的列表）
# 按界面设计，这里似乎应该删去key，contact，reward这些值
class FoundList(APIView):
    def get(self):
        items = []
        for found in Found.objects.filter(status=0):
            temp = {}
            temp['id'] = found.id
            temp['name'] = found.name
            temp['key'] = found.key
            temp['contact'] = found.contact
            temp['description'] = found.description
            temp['foundTime'] = found.foundTime
            temp['foundPlace'] = found.foundPlace
            temp['lng'] = found.longitude
            temp['lat'] = found.latitude
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
            temp['id'] = lost.id
            temp['name'] = lost.name
            temp['key'] = lost.key
            temp['contact'] = lost.contact
            temp['description'] = lost.description
            temp['lostTime'] = lost.lostTime
            temp['lostPlace'] = lost.lostPlace
            temp['lng'] = lost.longitude
            temp['lat'] = lost.latitude
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
            temp['id'] = lost.id
            temp['name'] = lost.name
            temp['key'] = lost.key
            temp['contact'] = lost.contact
            temp['description'] = lost.description
            temp['lostTime'] = lost.lostTime
            temp['lostPlace'] = lost.lostPlace
            temp['lng'] = lost.longitude
            temp['lat'] = lost.latitude
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
        for found in Found.objects.filter(user=self.input['user'], status=0):
            temp = {}
            temp['id'] = found.id
            temp['name'] = found.name
            temp['key'] = found.key
            temp['contact'] = found.contact
            temp['description'] = found.description
            temp['foundTime'] = found.foundTime
            temp['foundPlace'] = found.foundPlace
            temp['lng'] = found.longitude
            temp['lat'] = found.latitude
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
        temp['key'] = found.key
        temp['contact'] = found.contact
        temp['description'] = found.description
        temp['lostTime'] = found.foundTime
        temp['lostPlace'] = found.foundPlace
        temp['lng'] = found.longitude
        temp['lat'] = found.latitude
        temp['picUrl'] = found.picUrl
        return temp


# 失物详情页
# 需提供失物的id
class LostDetail(APIView):
    def get(self):
        lost = Lost.objects.get(id=self.input('id'))
        temp = {}
        temp['name'] = lost.name
        temp['key'] = lost.key
        temp['contact'] = lost.contact
        temp['description'] = lost.description
        temp['lostTime'] = lost.lostTime
        temp['lostPlace'] = lost.lostPlace
        temp['lng'] = lost.longitude
        temp['lat'] = lost.latitude
        temp['reward'] = lost.reward
        temp['picUrl'] = lost.picUrl
        return temp


# 新建失物信息的界面
class NewLost(APIView):
    def post(self):
        lost = Lost(name=self.input['name'],
                    key=self.input['key'],
                    description=self.input['description'],
                    contact=self.input['contact'],
                    lostTime=self.input['lostTime'],
                    lostPlace=self.input['lostPlace'],
                    longitude=self.input['lng'],
                    latitude=self.input['lat'],
                    reward=self.input['reward'],
                    user=self.input['user'],
                    picUrl=self.input['picUrl'],
                    status=0)
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
        data = self.request.FILES['image']
        picUrl = '/img/lostAndFound/' + str(
            len(os.listdir(settings.STATIC_ROOT + '/img/lostAndFound/'))) + '_' + data.name
        path = default_storage.save(settings.STATIC_ROOT + picUrl, ContentFile(data.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        return CONFIGS['SITE_DOMAIN'] + picUrl


class WxConfig(APIView):
    def get(self):
        config = WeChatLib.get_wechat_wx_config(self.input['url'])
        return config

