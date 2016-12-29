from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from LostAndFound.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, SITE_DOMAIN


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        LostHandler, FoundHandler, AdminLostHandler, MineHandler
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    menu = {
        'button': [
            {
                "type": "click",
                "name": "丢了东西",
                "key": "SOMETHING_LOST",
            },
            {
                "type": "click",
                "name": "捡了东西",
                "key": "SOMETHING_FOUND",
            },
            {
                "name": "其他",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "失物招领处",
                        "key": "ADMIN_LOST",
                    },
                    {
                        "type": "click",
                        "name": "我的",
                        "key": "MINE",
                    }
                ]
            }
        ]
    }


    @classmethod
    def update_menu(cls):
        cls.lib.set_wechat_menu(cls.menu)