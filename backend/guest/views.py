from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guest
from .utils import GuestSerializer
from log.utils import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from Crypto.Cipher import AES
import base64

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guard.wx_api import *
from guard.const import *
from guard.cipher import *
from django.core.cache import cache
from django.core.paginator import Paginator

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
        try:
            print(request.data.get("code"))
            log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.data.get("code"))
            print(log_info)
            open_id = log_info.get("open_id")
            print(open_id)
            session_key = log_info.get("session_key")
        except:
            return Response({"errmsg":log_info["errmsg"]})
        try:
            token=request.data.get("token")
            if not token:
                guest_object = request.data
                del guest_object["code"]
                guest_object["open_id"]=open_id
                guest_object["is_student"]=False
                serializer = self.get_serializer(data=guest_object)
                serializer.is_valid()
                self.perform_create(serializer)
                resp = serializer.data
                resp["open_id"] =encrypt(open_id)
                return Response(resp, status=status.HTTP_201_CREATED)
            else:
                data = {
                    "token":token
                }
                r = requests.post("https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token",data=data)
                # print(eval(r.text))
                packet = eval(r.text).get("user")
                print(packet)
                guest_object = {
                    "name":packet.get("name"),
                    "student_id":packet.get("card"),
                    "department":packet.get("department"),
                    "is_student":True,
                    "open_id":open_id
                }
                print(guest_object)
                serializer = self.get_serializer(data=guest_object)
                serializer.is_valid(raise_exception=False)
                self.perform_create(serializer)
                resp = serializer.data
                resp["open_id"]= encrypt(open_id)
                print(serializer.errors)
                print(resp)
                return Response(resp, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors)

        
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
        try:
            code = request.GET.get("code")
            log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        except:
            return Response({"errmsg":log_info["errmsg"]})
        query = Guest.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuestSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            guest_object=serializer.data[0]
            guest_object["open_id"]=encrypt(guest_object["open_id"])
            return Response(guest_object)
        else:
            return Response({"errmsg":"Account Not Found"})

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
            return Response({"errmsg":"Invalid open_id"})
        try:
            log_exist=cache.get(open_id)
            if log_exist:
                return Response(log_exist)
            else:
                raise Exception
                
            # guest_object = Guest.objects.get(open_id=open_id)
            # logs=guest_object.guest_log.all()
            # serializer=LogSerializer(data=list(logs.values())[-1])
            # serializer.is_valid(raise_exception=True)
            # return Response(serializer.validated_data)
        except:
            return Response({"errmsg":"Log Not Found"})
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
        try:
            if request.GET.get("code"):
                log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.GET.get("code"))
                open_id = log_info["open_id"]
            else:
                open_id = decrypt(request.GET.get("my_open_id"))
        except KeyError:
            return Response({"errmsg":log_info["errmsg"]})
        except:
            return Response({"errmsg":"Invalid open_id"})
        try:
            guest_object=Guest.objects.get(open_id=open_id)
            last_log=guest_object.guest_log.last()
            result={}
            if last_log.approval=="permit" and last_log.out_time==None:
                result["status"] = "still in"
            else:
                result["status"] = "out"
            return Response(result)
        except:
            return Response({"errmsg":"No Log"})
    

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
            # open_id = request.GET.get("open_id")
        except:
            return Response({"errmsg":"invalid open_id"})
        guest_object=Guest.objects.get(open_id=open_id)
        print(guest_object)
        log_history=list(guest_object.guest_log.all().values())
        serializer=LogSerializer(data=log_history,many=True)
        serializer.is_valid()
        print(serializer.errors)
        log_cache=cache.get(open_id)
        result = serializer.validated_data
        if log_cache:
            result.append(log_cache)
        print(result)
        for log in result:
            del log["guest_id"]
        p = Paginator(result,10)
        try:
            page = int(request.GET.get("page"))
        except:
            page=1
        if page>p.num_pages:page=p.num_pages
        elif page<1:page=1
        return Response({"data":p.page(page).object_list,"total":p.count})
            
            
                


