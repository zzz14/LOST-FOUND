# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from LostAndFound.settings import SITE_DOMAIN


__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event_click('HELP')

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })

class LostHandler(WeChatHandler):

    def check(self):
        return self.is_event_click('SOMETHING_LOST')

    def handle(self):
        return self.reply_single_news({
            'Title': '丢了东西？',
            'Description': '丢了东西请看这儿~',
            'Url': self.url_lost_list(),
        })

class FoundHandler(WeChatHandler):

    def check(self):
        return self.is_event_click('SOMETHING_FOUND')

    def handle(self):
        return self.reply_single_news({
            'Title': '捡了东西？',
            'Description': '捡了东西请看这儿~',
            'Url': self.url_found_list(),
        })

class AdminLostHandler(WeChatHandler):

    def check(self):
        return self.is_event_click('ADMIN_LOST')

    def handle(self):
        return self.reply_single_news({
            'Title': '失物招领处',
            'Description': '或许这里有你想找的东西~',
            'Url': SITE_DOMAIN + '/u/school_office/list',
        })

class MineHandler(WeChatHandler):

    def check(self):
        return self.is_event_click('MINE')

    def handle(self):
        return self.reply_single_news({
            'Title': '我的失物',
            'Description': '看看你丢了多少东西',
            'Url': self.url_mine(),
        })
