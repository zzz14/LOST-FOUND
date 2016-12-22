from codex.baseerror import *
from codex.baseview import APIView
from django.contrib import auth
import os
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
        self.check_input('', 'picUrl')
        adminLost = AdminLost(name=self.input['name'],
                              key=self.input['key'],)
        adminLost.save()
        return 0

class uploadImage(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('Not logined!')
        data = self.request.FILES['image']
        path = default_storage.save(settings.STATIC_ROOT + '/img/admin/'+data.name, ContentFile(data.read()))
        os.path.join(settings.MEDIA_ROOT, path)
        return CONFIGS['SITE_DOMAIN'] + '/img/admin/' + data.name