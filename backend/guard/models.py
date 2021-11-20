from django.db import models

# Create your models here.
class Log(models.Model):
    """ 来访记录 """
    guest = models.ForeignKey(
        "Guest",
        on_delete = models.SET_NULL,
        null=True,
    )
    purpose = models.CharField(max_length=100,default="empty")
    target_dorm = models.CharField(max_length=100,default="empty")
    host_student = models.CharField(max_length=100,default="empty")
    in_time = models.DateTimeField(null=True, default=None)
    out_time = models.DateTimeField(null=True, default=None)
    # def __str__(self):
    #     return self.name


class Guest(models.Model):
    """ 人员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128,primary_key=True) 
    phone = models.CharField(max_length=15)

    # def __str__(self):
    #     return self.name

class Guard(models.Model):
    """ 管理员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128,primary_key=True) 
    phone = models.CharField(max_length=15)
    
    # def __str__(self):
    #     return self.name

class Test1(models.Model):
    open_id = models.CharField(max_length=128,primary_key=True)

class Test2(models.Model):
    test1 = models.ForeignKey(
        "Test1",
        on_delete = models.SET_NULL,
        null=True,
    )
