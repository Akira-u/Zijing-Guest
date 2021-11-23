from django.db import models

# Create your models here.


class Guest(models.Model):
    """ 人员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128,primary_key=True) 
    phone = models.CharField(max_length=15)

    # def __str__(self):
    #     return self.name