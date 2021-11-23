from django.db import models

# Create your models here.
class APIInfo(models.Model):
    api_name = models.CharField(max_length=32, verbose_name="接口名称", default="请输入接口名称")
    # 接口描述
    api_describe = models.TextField(max_length=255, verbose_name="接口描述", default="请输入接口描述")
    
    # 接口负责人
    api_manager = models.CharField(max_length=11, verbose_name="接口负责人", default="请输入接口负责人名字")
    
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    # 修改时间
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="修改时间")
   
    class Meta:
        db_table = 'api_info'
        # 设置表名，默认表名是：应用名称_模型类名
        # 带有应用名的表名太长了
        verbose_name = '接口列表'
        verbose_name_plural = "接口列表"

    def __str__(self):
        return self.api_name