from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guard
from .utils import GuardSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .wx_api import *
import requests
from Crypto.Cipher import AES
from .const import *
import datetime
# Create your views here.


# 11.17
# 当前的处理逻辑是改某个guest对应的所有log记录中的最近一条，如果操作不规范则会出现问题
# 二轮迭代加入缓存表后可以解决
# 接口主要通过 重写父类函数(没有action的标识) 或 定义action 来完成
# url: /{application_name}/{model_name}/{action_name(if exist)}
# 例: POST /guard/log/ 调用Log的create
#     POST /guard/log/checkin 调用Log的checkin








class GuardViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer
    """ POST """
    """ register """
    def create(self, request, *args, **kwargs):
        log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=request.data.get("code"))
        open_id = log_info.get("open_id")
        session_key = log_info.get("session_key")
        guard_object = request.data
        del guard_object["code"]
        guard_object["open_id"]=open_id
        serializer = self.get_serializer(data=guard_object)
        serializer.is_valid()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['GET'])
    def login(self,request):
        code = request.GET.get("code")
        log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=code)
        query = Guard.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuardSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            return Response(serializer.data[0])
        else:
            return Response({})

