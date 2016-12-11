# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^lost/list/?$', FoundList.as_view()),
    url(r'^lost/new/?$', NewLost.as_view()),
    url(r'^lost/detail/?$', FoundDetail.as_view()),
    url(r'^found/list/?$', LostList.as_view()),
    url(r'^found/new/?$', NewFound.as_view()),
    url(r'^found/detail/?$', LostDetail.as_view()),
    url(r'^school_office/list/?$', SchoolOfficeLostList.as_view()),
    url(r'^mine/lost/?$', MineLost.as_view()),
    url(r'^mine/found/?$', MineFound.as_view()),
    url(r'^mine/lost/delete/?$', DeleteMineLost.as_view()),
    url(r'^mine/found/delete/?$', DeleteMineFound.as_view()),
    url(r'^wx/config/?$',WxConfig.as_view())
]
