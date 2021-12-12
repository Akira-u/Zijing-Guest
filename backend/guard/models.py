from django.db import models

# Create your models here.
from dorm.models import DormBuilding



class Guard(models.Model):
    """ 管理员信息 """
    name = models.CharField(max_length=20)
    open_id = models.CharField(max_length=128,primary_key=True) 
    phone = models.CharField(max_length=15)
    dormbuilding = models.ForeignKey(
        DormBuilding,
        on_delete = models.SET_NULL,
        null=True,
        related_name='Guard_Dorm_Building'
    )
    
