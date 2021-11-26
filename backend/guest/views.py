from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guest
from .utils import GuestSerializer
from log.utils import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guard.wx_api import *
from guard.const import *

# Create your views here.
class GuestViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
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
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.data.get("code"))
        open_id = log_info.get("open_id")
        session_key = log_info.get("session_key")
        guest_object = request.data
        del guest_object["code"]
        guest_object["open_id"]=open_id
        serializer = self.get_serializer(data=guest_object)
        serializer.is_valid()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
    operation_summary='判断当前Guest是否已注册',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guest code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('查询是否已注册，如果已注册则返回Guest,否则为空',GuestSerializer)}
    )
    @action(detail=False,methods=['GET'])
    def login(self,request):
        code = request.GET.get("code")
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        query = Guest.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuestSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            return Response(serializer.data[0])
        else:
            return Response({})

    @swagger_auto_schema(
    operation_summary='返回当前Guest对应的Log',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guest code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('返回当前Guest的Log',LogSerializer)}
    )
    @action(detail=False,methods=['GET'])
    def approve_result(self,request):
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.GET.get("code"))
        open_id = log_info.get("open_id")
        guest_object = Guest.objects.get(open_id=open_id)
        logs=guest_object.guest_log.all()
        serializer=LogSerializer(data=list(logs.values())[-1])
        serializer.is_valid(raise_exception=False)
        return Response(serializer.validated_data)
        # return Response({})

    @swagger_auto_schema(
    operation_summary='返回当前Guest的访问状态',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guest code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('返回当前Guest的访问状态',openapi.Schema("status",type=openapi.TYPE_STRING,enum=["still in","out"]))}
    )
    @action(detail=False,methods=['GET'])
    def status(self,request):
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.GET.get("code"))
        open_id = log_info.get("open_id")
        # open_id = request.GET.get("open_id")
        guest_object = Guest.objects.get(open_id=open_id)
        last_log=guest_object.guest_log.last()
        result={}
        if last_log.approval=="permit" and last_log.out_time==None:
            result["status"] = "still in"
        else:
            result["status"] = "out"
        # serializer=LogSerializer(data=list(logs.values())[-1])
        # serializer.is_valid(raise_exception=False)
        return Response(result)
        # return Response({})
