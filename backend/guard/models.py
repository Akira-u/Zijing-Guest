from django.db import models

# Create your models here.
class Log(models.Model):
    """ 来访记录 """
    name = models.CharField(max_length=20)
    custom_id = models.IntegerField()

    def __str__(self):
        return self.name

class User(models.Model):
    """ 人员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128) # wechat
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name