from django.db import models

# Create your models here.
class Log(models.Model):
    """ 来访记录 """
    name = models.CharField(max_length=20)
    custom_id = models.IntegerField()

    def __str__(self):
        return self.name
