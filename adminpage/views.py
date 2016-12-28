from codex.baseerror import *
from codex.baseview import APIView
from django.contrib import auth
import os
import time
from time import mktime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from wechat.models import AdminLost, publisherIdToPlaces, adminLostType
from LostAndFound.settings import CONFIGS

class userLogin(APIView):

    def post(self):
        username = self.input['username']
        password = self.input['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(self.request, user)
            return 0
        raise LogicError("login error")

    def get(self):
        if self.request.user.is_authenticated():
            return 0
        else:
            raise LogicError("login error")

class userLogout(APIView):

    def post(self):
        auth.logout(self.request)
        if not self.request.user.is_authenticated(): #true用户登录 false用户登出
            return 0
        else:
            raise LogicError("logout error")

class newAdminLost(APIView):
    def post(self):
        self.check_input('type', 'picUrl')
        adminLost = AdminLost(type=self.input['type'],
                              picUrl=self.input['picUrl'],
                              publisherId=self.request.user.id,
                              publishTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        adminLost.save()
        return 0

class uploadImage(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('Not logined!')
        data = self.request.FILES['image']
        path = default_storage.save(settings.STATIC_ROOT + '/img/adminpage/'+data.name, ContentFile(data.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        return CONFIGS['SITE_DOMAIN'] + '/img/adminpage/' + data.name

class adminLostList(APIView):
    def get(self):
        items = []
        for lost in AdminLost.objects.filter(status=0, publisherId=self.request.user.id):
            temp = {}
            temp['id'] = lost.id
            temp['type'] = lost.type
            temp['publishTime'] = mktime(lost.publishTime.timetuple())
            temp['picUrl'] = lost.picUrl.split(";")
            temp['picUrl'].pop()
            items.append(temp)
        info = {}
        info['adminName'] = publisherIdToPlaces[self.request.user.id]
        info['list'] = items
        return info

# 需传回要删除的失物id
class deleteAdminLost(APIView):
    def post(self):
        AdminLost.objects.filter(id=self.input['id']).update(status = 1);

class adminLostDetail(APIView):
    def get(self):
        return publisherIdToPlaces[self.request.user.id]