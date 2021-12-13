from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guard
from .utils import GuardSerializer,GuardFilter
from log.utils import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter  # 导入排序

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .wx_api import *
import requests
from Crypto.Cipher import AES
from .const import *
from .cipher import *
from django.core.cache import cache
from django.core.paginator import Paginator

import datetime
import json
import random

# Create your views here.


# 11.17
# 当前的处理逻辑是改某个guest对应的所有log记录中的最近一条，如果操作不规范则会出现问题
# 二轮迭代加入缓存表后可以解决
# 接口主要通过 重写父类函数(没有action的标识) 或 定义action 来完成
# url: /{application_name}/{model_name}/{action_name(if exist)}
# 例: POST /guard/log/ 调用Log的create
#     POST /guard/log/checkin 调用Log的checkin

pending_guard={}

class GuardViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter)
    filter_class = GuardFilter

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
            'password': openapi.Schema(
                 type=openapi.TYPE_STRING,
                 description='Password'
            ),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=request.data.get("code"))
        open_id = log_info.get("open_id")
        if not open_id:
            return Response({"code":log_info["errmsg"]},status=status.HTTP_400_BAD_REQUEST)
        guard_object = request.data
        if request.data.get("password") == guard_password or request.data.get("password") == pending_guard.get(request.data.get("name")).get("password"):
            del guard_object["code"]
            guard_object["open_id"]=open_id
            serializer = self.get_serializer(data=guard_object)
            try:
                serializer.is_valid(raise_exception=True)
            except:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            resp = serializer.data
            resp["open_id"] =encrypt(open_id)
            del pending_guard[request.data.get("name")]
            return Response(resp, status=status.HTTP_201_CREATED)
        else:
            return Response({"password":["password incorrect"]},status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"code":log_info["errmsg"]},status=status.HTTP_400_BAD_REQUEST)
        query = Guard.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuardSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            guard_object=serializer.data[0]
            guard_object["open_id"]=encrypt(guard_object["open_id"])
            return Response(guard_object)
        else:
            return Response({"code":["Account Not Found"]},status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
    operation_summary='管理员后台获取，获取所有仍在楼内的访问记录',
    manual_parameters=[
        openapi.Parameter(
            name='open_id',
            in_=openapi.IN_QUERY,
            description='Guard open_id',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('查询是否已注册，如果已注册则返回Guard,否则为空',GuardSerializer)}
    )
    @action(detail=False,methods=['GET'])
    def backstage(self,request):
        try:
            keys=cache.keys("*")
            logs = []
            for key in keys:
                log = cache.get(key)
                cache.persist(key)
                if log.get("in_time"):
                    logs.append(cache.get(key))
                    cache.persist(key)
            p = Paginator(logs,10)
            try:
                page = int(request.GET.get("page"))
            except:
                page=1
            if page>p.num_pages:page=p.num_pages
            elif page<1:page=1
            return Response({"data":p.page(page).object_list,"total":p.count},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
    operation_summary='发送提醒',       
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'open_id': openapi.Schema(
                 type=openapi.TYPE_STRING,
                 description='Guest open_id'
            ),
            'msg': openapi.Schema(
                 type=openapi.TYPE_OBJECT,
                 description='remind msg, special format!'
            ),
            }
        )
    )
    @action(detail=False,methods=['POST'])
    def remind(self,request):
        try:
            open_id = decrypt(request.data.get("open_id"))
        except:
            return Response({"open_id":["invalid open_id"]},status=status.HTTP_400_BAD_REQUEST)
        try:    
            access_token=getAccessToken(guard_appId,guard_appSecret)
        except:
            return Response({"errmsg":["Wechat server error"]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not access_token:
            return Response({"errmsg":["Wechat server error"]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = {
            "touser": open_id,
            "template_id":remind_template,
            "data":request.data.get("msg"),
        }
        params = {
            "access_token":access_token
        }
        r = requests.post("https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token="+access_token,data=json.dumps(data))
        packet = eval(r.text)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False,methods=["GET"])
    def static(self,request,*args,**kwargs):
        query = Guard.objects.all()
        resp={
            "guards":{},
            "total_count":query.count()
        }
        return Response(resp,status=status.HTTP_200_OK)
    @action(detail=False,methods=["POST"])
    def pre_create(self,request,*args,**kwargs):
        try:
            password=random.sample("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",10)
            pre_guard = {
                "name":request.data.get("name"),
                "password": "".join(password)
            }
            pending_guard[request.data.get("name")]=pre_guard
            return Response({"result":pre_guard},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)