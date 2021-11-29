from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guard
from .utils import GuardSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .wx_api import *
import requests
from Crypto.Cipher import AES
from .const import *
from .cipher import *

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
    @swagger_auto_schema(
    operation_summary='注册账号',       
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                 type=openapi.TYPE_STRING,
                 description='User Name'
            ),
            'phone': openapi.Schema(
                 type=openapi.TYPE_STRING,
                 description='User Phone'
            ),
            'code': openapi.Schema(
                 type=openapi.TYPE_STRING,
                 description='User Code'
            ),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        try:
            log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=request.data.get("code"))
            open_id = log_info.get("open_id")
            session_key = log_info.get("session_key")
            guard_object = request.data
            del guard_object["code"]
            guard_object["open_id"]=open_id
            serializer = self.get_serializer(data=guard_object)
            serializer.is_valid()
            self.perform_create(serializer)
            resp = serializer.data
            resp["open_id"] =encrypt(open_id)
            return Response(resp, status=status.HTTP_201_CREATED)
        except :
            return Response({"errmsg":serializer.errors})
    @swagger_auto_schema(
    operation_summary='判断当前Guard是否已注册',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guard code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('查询是否已注册，如果已注册则返回Guard,否则为空',GuardSerializer)}
    )
    @action(detail=False,methods=['GET'])
    def login(self,request):
        try:
            code = request.GET.get("code")
            log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=code)
        except:
            return Response({"errmsg":log_info["errmsg"]})
        query = Guard.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuardSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            guard_object=serializer.data[0]
            guard_object["open_id"]=encrypt(guard_object["open_id"])
            return Response(guard_object)
        else:
            return Response({"errmsg":"Account Not Found"})

