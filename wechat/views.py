from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Lost, Found
from LostAndFound.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        HelpOrSubscribeHandler, UnbindOrUnsubscribeHandler, BindAccountHandler,
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
            },
        ]
    }

'''
    @classmethod
    def get_book_btn(cls):
        return cls.menu['button'][-1]

    @classmethod
    def update_book_button(cls, activities):
        book_btn = cls.get_book_btn()
        if len(activities) == 0:
            book_btn['type'] = 'click'
            book_btn['key'] = cls.event_keys['book_empty']
        else:
            book_btn.pop('type', None)
            book_btn.pop('key', None)
        book_btn['sub_button'] = list()
        for act in activities:
            book_btn['sub_button'].append({
                'type': 'click',
                'name': act['name'],
                'key': cls.event_keys['book_header'] + str(act['id']),
            })

    @classmethod
    def update_menu(cls, activities=None):
        """
        :param activities: list of Activity
        :return: None
        """
        if activities is not None:
            if len(activities) > 5:
                cls.logger.warn('Custom menu with %d activities, keep only 5', len(activities))
            cls.update_book_button([{'id': act.id, 'name': act.name} for act in activities[:5]])
        else:
            current_menu = cls.lib.get_wechat_menu()
            existed_buttons = list()
            for btn in current_menu:
                if btn['name'] == '抢票':
                    existed_buttons += btn.get('sub_button', list())
            activity_ids = list()
            for btn in existed_buttons:
                if 'key' in btn:
                    activity_id = btn['key']
                    if activity_id.startswith(cls.event_keys['book_header']):
                        activity_id = activity_id[len(cls.event_keys['book_header']):]
                    if activity_id and activity_id.isdigit():
                        activity_ids.append(int(activity_id))
            return cls.update_menu(Activity.objects.filter(
                id__in=activity_ids, status=Activity.STATUS_PUBLISHED, book_end__gt=timezone.now()
            ).order_by('book_end')[: 5])
        cls.lib.set_wechat_menu(cls.menu)'''
