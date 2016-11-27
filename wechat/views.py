from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Lost, Found
from LostAndFound.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


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
        'found_by_key':'FOUND_BY_KEY',
        'found_by_place':'FOUND_BY_PLACE',
        'release_found':'RELEASE_FOUND',
        'lost_by_key': 'LOST_BY_KEY',
        'lost_by_place': 'LOST_BY_PLACE',
        'release_lost': 'RELEASE_LOST',
    }

    menu = {
        'button': [
            {
                "name": "失物招领",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "关键字查询",
                        "key": event_keys['found_by_key'],
                    },
                    {
                        "type": "click",
                        "name": "地点查询",
                        "key": event_keys['found_by_place'],
                    },
                    {
                        "type": "click",
                        "name": "发布失物招领",
                        "key": event_keys['release_found'],
                    }
                ]
            },
            {
                "name": "寻物启事",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "关键字查询",
                        "key": event_keys['lost_by_key'],
                    },
                    {
                        "type": "click",
                        "name": "地点查询",
                        "key": event_keys['lost_by_place'],
                    },
                    {
                        "type": "click",
                        "name": "发布寻物启事",
                        "key": event_keys['release_lost'],
                    }
                ]
            },
            {
                "name": "其他",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "校内失物招领处",
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