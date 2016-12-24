from codex.baseerror import *
from codex.baseview import APIView
from django.contrib import auth
import os
import time
from time import mktime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from wechat.models import AdminLost
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
        self.check_input('type', 'picUrl0','picUrl1','picUrl2','picUrl3')
        adminLost = AdminLost(type=self.input['type'],
                              picUrl0=self.input['picUrl0'],
                              picUrl1=self.input['picUrl1'],
                              picUrl2=self.input['picUrl2'],
                              picUrl3=self.input['picUrl3'],
                              publishTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                              status=self.input['status'])

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
        for lost in AdminLost.objects.all():
            print(lost.id)

            temp = {}
            temp['id'] = lost.id
            temp['status'] = lost.status
            temp['type'] = lost.type
            temp['publishTime'] = mktime(lost.publishTime.timetuple())
            temp['picUrl0'] = lost.picUrl0
            temp['picUrl1'] = lost.picUrl1
            temp['picUrl2'] = lost.picUrl2
            temp['picUrl3'] = lost.picUrl3
            items.append(temp)
        return items

# 需传回要删除的失物id
class deleteActivity(APIView):
    def post(self):
        AdminLost.objects.filter(id=self.input['id']).update(status = 1);