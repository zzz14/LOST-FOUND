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

    event_keys = {
        'mine': 'MINE',
        'help': 'HELP',
        'school_office':'SCHOOL_OFFICE',
    }

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
                "url": "http://www.baidu.com",
            },
            {
                "name": "其他",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "失物招领处",
                        "key": event_keys['school_office'],
                    },
                    {
                        "type": "click",
                        "name": "帮助",
                        "key": event_keys['help'],
                    },
                    {
                        "type": "click",
                        "name": "我的",
                        "key": event_keys['mine'],
                    }
                ]
            }
        ]
    }


    @classmethod
    def update_menu(cls):
        cls.lib.set_wechat_menu(cls.menu)