# -*- coding: utf-8 -*-
#
from adminpage.views import *
from django.conf.urls import url

__author__ = "Epsirom"


urlpatterns = [
    url(r'^login/?$', userLogin.as_view()),
    url(r'^image/upload/?$',uploadImage.as_view()),
    url(r'^adminpage/list/?$', adminLostList.as_view()),
    url(r'^adminpage/detail/?$', newAdminLost.as_view()),
    url(r'^adminpage/typeList/?$', typeList.as_view()),
    url(r'^adminpage/delete/?$', deleteAdminLost.as_view()),
    url(r'^logout/?$', userLogout.as_view()),
]
