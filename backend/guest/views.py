from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guest
from .utils import GuestSerializer, GuestFilter
from log.utils import LogSerializer
from rest_framework.filters import OrderingFilter  # 导入排序
from rest_framework.response import Response
from rest_framework.decorators import action
from Crypto.Cipher import AES
import base64

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guard.wx_api import *
from guard.const import *
from guard.cipher import *
from guard.models import Guard
from django.core.cache import cache
from django.core.paginator import Paginator

# Create your views here.
class GuestViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter)
    filter_class = GuestFilter
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
        if not open_id:
            if not log_info.get("errmsg"):
                return Response({"code":"无效二维码"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"code":log_info["errmsg"]},status=status.HTTP_400_BAD_REQUEST)
        try:
            token=request.data.get("token")
            if not token:
                guest_object = {
                    "name":request.data.get("name"),
                    "phone":request.data.get("phone"),
                    "is_student":False,
                    "open_id":open_id,
                }
                serializer = self.get_serializer(data=guest_object)
                try:
                    serializer.is_valid(raise_exception=True)
                except:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                self.perform_create(serializer)
                resp = serializer.data
                resp["open_id"]= encrypt(open_id)
                return Response(resp, status=status.HTTP_201_CREATED)
            else:
                data = {
                    "token":token
                }
                r = requests.post("https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token",data=data)
                packet = eval(r.text).get("user")
                guest_object = {
                    "name":packet.get("name"),
                    "student_id":packet.get("card"),
                    "department":packet.get("department"),
                    "is_student":True,
                    "open_id":open_id
                }
                serializer = self.get_serializer(data=guest_object)
                try:
                    serializer.is_valid(raise_exception=True)
                except:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                self.perform_create(serializer)
                resp = serializer.data
                resp["open_id"]= encrypt(open_id)
                return Response(resp, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
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
        open_id = log_info.get("open_id")
        if not open_id:
            if not log_info.get("errmsg"):
                return Response({"code":"无效二维码"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"code":log_info["errmsg"]},status=status.HTTP_400_BAD_REQUEST)
        query = Guest.objects.filter(open_id=open_id)
        if query:
            serializer = GuestSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            guest_object=serializer.data[0]
            guest_object["open_id"]=encrypt(guest_object["open_id"])
            return Response(guest_object,status=status.HTTP_200_OK)
        else:
            return Response({"code":"Account Not Found"},status=status.HTTP_200_OK)

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
        try:
            open_id = decrypt(request.GET.get("my_open_id"))
        except:
            return Response({"my_open_id":"Invalid open_id"},status=status.HTTP_400_BAD_REQUEST)
        log_exist=cache.get(open_id)
        if log_exist:
            cache.persist(open_id)
            return Response(log_exist,status=status.HTTP_200_OK)
        else:
            return Response({"approval":"reject"},status=status.HTTP_200_OK)
    @swagger_auto_schema(
    operation_summary='返回当前Guest的访问状态',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guest code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('返回当前Guest的访问状态',openapi.Schema("status",type=openapi.TYPE_STRING,enum=["still in","out","guard","no account"]))}
    )
    @action(detail=False,methods=['GET'])
    def status(self,request):
        if request.GET.get("code"):
            log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.GET.get("code"))
            open_id = log_info.get("open_id")
            if not open_id:
                if not log_info.get("errmsg"):
                    return Response({"code":"无效二维码"},status=status.HTTP_400_BAD_REQUEST)
                return Response({"code":log_info["errmsg"]},status=status.HTTP_200_OK)
        else:
            try:
                open_id = decrypt(request.GET.get("my_open_id"))
            except:
                return Response({"my_open_id":["please check your open_id in storage, it is invalid"]},status=status.HTTP_200_OK)    
        guard_object = Guard.objects.filter(open_id=open_id)
        guest_object = Guest.objects.filter(open_id=open_id)
        if (not guard_object) and (not guest_object):
            return Response({"status":"no account"},status=status.HTTP_200_OK)
        if guard_object:
            return Response({"status":"guard"},status=status.HTTP_200_OK)
        last_log=cache.get(open_id)
        try:
            cache.persist(open_id)
            if last_log["approval"]=="permit" and last_log["out_time"]==None:
                return Response({"status":"still in"},status=status.HTTP_200_OK)
            else:
                return Response({"status":"out"},status=status.HTTP_200_OK)    
        except:
            return Response({"status":"out"},status=status.HTTP_200_OK)  
    @swagger_auto_schema(
    operation_summary='返回当前Guest的访问历史',
    manual_parameters=[
        openapi.Parameter(
            name='open_id',
            in_=openapi.IN_QUERY,
            description='Guest open_id',
            type=openapi.TYPE_STRING
        ),],
    )
    @action(detail=False,methods=['GET'])
    def history(self,request):
        try:
            open_id = decrypt(request.GET.get("my_open_id"))
            guest_object=Guest.objects.get(open_id=open_id)
        except:
            return Response({"my_open_id":"please check your open_id in storage, it is invalid"},status=status.HTTP_400_BAD_REQUEST)
        log_history=guest_object.guest_log.all()
        p = Paginator(log_history,10)
        try:
            page = int(request.GET.get("page"))
        except:
            page=1
        if page>p.num_pages:page=p.num_pages
        elif page<1:page=1
        serializer = LogSerializer(p.page(page).object_list,many=True)
        result = serializer.data
        return Response({"data": result,"total":p.count},status=status.HTTP_200_OK)
    

    @action(detail=False,methods=["POST"])
    def to_black(self,request,*args, **kwargs):
        try:
            query=[Guest.objects.get(open_id=guest["open_id"]) for guest in request.data]
            for guest in query:
                guest.credit=False
            Guest.objects.bulk_update(query,fields=["credit",])
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                
    @action(detail=False,methods=["POST"])
    def to_white(self,request,*args, **kwargs):
        try:
            query=[Guest.objects.get(open_id=guest["open_id"]) for guest in request.data]
            for guest in query:
                guest.credit=True
            Guest.objects.bulk_update(query,fields=["credit",])
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False,methods=["GET"])
    def static(self,request,*args,**kwargs):
        query = Guest.objects.all()
        resp={
            "guards":{},
            "total_count":query.count()
        }
        return Response(resp,status=status.HTTP_200_OK)