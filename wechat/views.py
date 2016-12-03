from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Lost, Found
from LostAndFound.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, SITE_DOMAIN


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        HelpOrSubscribeHandler,
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    menu = {
        'button': [
            {
                "type": "view",
                "name": "丢了东西",
                "url": SITE_DOMAIN + '/lost/list',
            },
            {
                "type": "view",
                "name": "捡了东西",
                "url": SITE_DOMAIN + '/found/list',
            },
            {
                "name": "其他",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "失物招领处",
                        "url": SITE_DOMAIN + '/school_office/list',
                    },
                    {
                        "type": "view",
                        "name": "我的失物",
                        "url": SITE_DOMAIN + '/mine/lost',
                    },
                    {
                        "type": "view",
                        "name": "我的拾物",
                        "url": SITE_DOMAIN + '/mine/found',
                    },
                    {
                        "type": "view",
                        "name": "帮助",
                        "url": SITE_DOMAIN + '/help',
                    }
                ]
            }
        ]
    }


    @classmethod
    def update_menu(cls):
        cls.lib.set_wechat_menu(cls.menu)