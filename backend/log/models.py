from django.db import models
from guest.models import Guest
# Create your models here.
class Log(models.Model):
    """ 来访记录 """
    guest = models.ForeignKey(
        Guest,
        on_delete = models.SET_NULL,
        null=True,
        related_name='guest_log'
    )
    purpose = models.CharField(max_length=100,default="empty")
    target_dorm = models.CharField(max_length=100,default="empty")
    host_student = models.CharField(max_length=100,default="empty")
    in_time = models.DateTimeField(null=True, default=None)
    out_time = models.DateTimeField(null=True, default=None)
    approval = models.CharField(max_length=20,default="pending")
    target_building = models.CharField(max_length=20,default="紫荆一号楼")
    # def __str__(self):
    #     return self.name