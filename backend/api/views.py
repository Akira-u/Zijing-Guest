from rest_framework import viewsets
from rest_framework import generics
from . import models
from . import serializers

class APIList(generics.ListAPIView):
    """
    查看接口列表
    """
    queryset = models.APIInfo.objects.all()
    serializer_class = serializers.APISerializer

class APIDetail(generics.RetrieveAPIView):
    """
    查看接口详细
    """
    queryset = models.APIInfo.objects.all()
    serializer_class = serializers.APISerializer


class APIDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    更新接口内容
    """
    queryset = models.APIInfo.objects.all()
    serializer_class = serializers.APISerializer


class APIInfoViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            返回一组（查）

        list:
            返回所有组（查）

        create:
            创建新组（增）

        delete:
            删除现有的一组（删）

        partial_update:
            更新现有组中的一个或多个字段（改：部分更改）

        update:
            更新一组（改：全部更改）
    """

    queryset = models.APIInfo.objects.all()
    serializer_class = serializers.APIInfoSerializer