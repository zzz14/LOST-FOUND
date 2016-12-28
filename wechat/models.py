from django.db import models
from codex.baseerror import LogicError

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

class Lost(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    contacts = models.CharField(max_length=128, default=None)
    contactType = models.CharField(max_length=128, default=None)
    contactNumber = models.CharField(max_length=128, default=None)
    description = models.TextField()
    lostTime = models.DateTimeField(db_index=True)
    lostPlace = models.CharField(max_length=128, default=None)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    reward = models.CharField(max_length=128, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    picUrl = models.CharField(max_length=256, default=None)
    status = models.IntegerField(default=0)

class Found(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    contacts = models.CharField(max_length=128, default=None)
    contactType = models.CharField(max_length=128, default=None)
    contactNumber = models.CharField(max_length=128, default=None)
    description = models.TextField()
    foundTime = models.DateTimeField(db_index=True)
    foundPlace = models.CharField(max_length=128, default=None)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    picUrl = models.CharField(max_length=256, default=None)
    status = models.IntegerField(default=0)

# 失物招领处的失物
class AdminLost(models.Model):
    type = models.CharField(max_length=64, db_index=True)
    publisherId = models.IntegerField(default=0)
    picUrl = models.CharField(max_length=4096, default=None)
    publishTime = models.DateTimeField(db_index=True)
    status = models.IntegerField(default=0)

publisherIdToPlaces = {
    1 : "文科图书馆",
    2 : "北馆",
    3 : "逸夫馆",
    4 : "老馆",
    5 : "一教",
    6 : "二教",
    7 : "三教",
    8 : "四教",
    9 : "五教",
    10 : "六教",
    11 : "紫荆园",
    12 : "桃李园",
    13 : "丁香园",
    14 : "观畴园",
    15 : "听涛园",
    16 : "清芬园"
}

adminLostType = ["学生卡", "钥匙", "U盘", "钱包", "电子产品", "文具书本", "衣物配件", "生活用品", "体育用品", "其他"]

'''
class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1


class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, db_index=True, unique=True)
    activity = models.ForeignKey(Activity)
    status = models.IntegerField()

    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2
'''