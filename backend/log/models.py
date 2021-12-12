from django.db import models
from guest.models import Guest
from dorm.models import Dorm, DormBuilding
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
    dorm = models.ForeignKey(
        Dorm,
        on_delete=models.SET_NULL,
        null=True,
        related_name="log_dorm"
    )
    host_student = models.CharField(max_length=100,default="empty")
    in_time = models.DateTimeField(null=True, default=None)
    out_time = models.DateTimeField(null=True, default=None)
    approval = models.CharField(max_length=20,default="pending")
    dormbuilding = models.ForeignKey(
        DormBuilding,
        on_delete=models.SET_NULL,
        null=True,
        related_name="log_dormbuilding"
    )