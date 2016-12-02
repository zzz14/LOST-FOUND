from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import Lost, Found, User

'''
class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        raise NotImplementedError('You should implement UserBind.validate_user method')

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()
'''
# 点击“丢了东西”后出现的列表（被拾到东西的列表）
class FoundList(APIView):
    '''
    def get(self):
        temp = []
        for found in Found.objects.all():
            temp = {}
            temp['id'] = activity.id
            temp['name'] = activity.name
            temp['description'] = activity.description
            temp['place'] = activity.place
            temp['status'] = activity.status
            temp['startTime'] = mktime(activity.start_time.timetuple())
            temp['endTime'] = mktime(activity.end_time.timetuple())
            temp['bookStart'] = mktime(activity.book_start.timetuple())
            temp['bookEnd'] = mktime(activity.book_end.timetuple())
            temp['currentTime'] = time.time()
            items.append(temp)
        return items
'''