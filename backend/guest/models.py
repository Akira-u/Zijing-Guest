from django.db import models

# Create your models here.


class Guest(models.Model):
    """ 人员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128,primary_key=True) 
    phone = models.CharField(max_length=15, null=True,default=None)
    department = models.CharField(max_length=20, null=True,default=None)
    student_id = models.CharField(max_length=12, null=True,default=None)
    is_student = models.BooleanField(default=True)
    credit = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.name