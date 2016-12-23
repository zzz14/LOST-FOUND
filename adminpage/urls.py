# -*- coding: utf-8 -*-
#
from adminpage.views import *
from django.conf.urls import url

__author__ = "Epsirom"


urlpatterns = [
    url(r'^login/?$', userLogin.as_view()),
]
