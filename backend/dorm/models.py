from django.db import models

# Create your models here.

class DormBuilding(models.Model):
    name = models.CharField(max_length=12,default="紫荆1号楼")
    
class Dorm(models.Model):
    dormbuilding = models.ForeignKey(
        DormBuilding,
        on_delete = models.SET_NULL,
        null=True,
        related_name='Dorm_Building'
    )
    name = models.CharField(max_length=20,default="empty")
    student1 = models.CharField(max_length=20,default="empty")
    student2 = models.CharField(max_length=20,default="empty")
    student3 = models.CharField(max_length=20,default="empty")
    student4 = models.CharField(max_length=20,default="empty")