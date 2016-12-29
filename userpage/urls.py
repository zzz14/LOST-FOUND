# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^found/list/?$', FoundList.as_view()),
    url(r'^lost/new/?$', NewLost.as_view()),
    url(r'^found/detail/?$', FoundDetail.as_view()),
    url(r'^lost/list/?$', LostList.as_view()),
    url(r'^found/list_search/?$', FoundListSearch.as_view()),
    url(r'^lost/list_search/?$', LostListSearch.as_view()),
    url(r'^found/new/?$', NewFound.as_view()),
    url(r'^lost/detail/?$', LostDetail.as_view()),
    url(r'^school_office/list/?$', SchoolOfficeLostList.as_view()),
    url(r'^mine/lost/?$', MineLost.as_view()),
    url(r'^mine/found/?$', MineFound.as_view()),
    url(r'^mine/lost/delete/?$', DeleteMineLost.as_view()),
    url(r'^mine/found/delete/?$', DeleteMineFound.as_view()),
    url(r'^lost/modify/?$', ModifyLost.as_view()),
    url(r'^found/modify/?$', ModifyFound.as_view()),
    url(r'^wx/config/?$',WxConfig.as_view())
]
