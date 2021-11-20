from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guest, Guard
from .utils import LogSerializer,GuestSerializer, GuardSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .wx_api import *
import requests
from Crypto.Cipher import AES
from .const import *
import datetime
from .consumers import *
# Create your views here.
from guard.models import Log


# 11.17
# 当前的处理逻辑是改某个guest对应的所有log记录中的最近一条，如果操作不规范则会出现问题
# 二轮迭代加入缓存表后可以解决
# 接口主要通过 重写父类函数(没有action的标识) 或 定义action 来完成
# url: /{application_name}/{model_name}/{action_name(if exist)}
# 例: POST /guard/log/ 调用Log的create
#     POST /guard/log/checkin 调用Log的checkin

class LogViewSet(viewsets.ModelViewSet):
    """ 来访日志 viewset """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = LogFilter
    """ POST """
    def create(self, request, *args, **kwargs):
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=request.data.get("code"))
        log_object = request.data
        print(log_object)
        del log_object["code"]
        # log_object["open_id"] = log_info.get("open_id")
        guest_objects = Guest.objects.filter(open_id=log_info.get("open_id"))
        # list(instance)[0]
        # log_object["guest"]=guest_object
        # print(log_object)
        # instance = Log.objects.create(**log_object)
        print(list(guest_objects)[0])
        guest_object=list(guest_objects)[0]
        log_object["guest_id"]=guest_object.open_id # confusing???? 
        print(log_object)
        serializer = self.get_serializer(data=log_object)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        # TODO
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    """ POST """
    @action(detail=False,methods=["POST"])
    def check_in(self, request):
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=request.data.get("code"))
        log_object = request.data
        del log_object["code"]
        instance = Log.objects.filter(guest__open_id=log_info.get("open_id"))
        serializer = self.get_serializer(list(instance)[0], data={"in_time":datetime.datetime.now()}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        notice(conn_id=log_info.get("object"),**{"permit":True})
        return Response(serializer.data)
    @action(detail=False,methods=["POST"])
    def check_out(self, request):
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=request.data.get("code"))
        log_object = request.data
        del log_object["code"]
        instance = Log.objects.filter(guest__open_id=log_info.get("open_id"))
        serializer = self.get_serializer(list(instance)[0], data={"out_time":datetime.datetime.now()}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)        
    """ GET """
    @action(detail=False,methods=["GET"])
    def info(self,request):
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=request.GET.get("code"))
        print(log_info)
        instance = Log.objects.filter(guest__open_id=log_info.get("open_id"))
        print(instance)
        serializer = self.get_serializer(data=list(instance)[0])
        serializer.is_valid(raise_exception=False)
        # print(serializer.data)
        # print(serializer.errors)
        return Response(serializer.data)

    #     access_token = getAccessToken(appId=guest_appId, appSecret=guest_appSecret)
    #     log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=code )
    #     key_info = getGuestEncryptKey(access_token, log_info.get("open_id"), log_info.get("session_key"))
    #     cipher = AES.new(key_info.get("encrypt_key").encode(), AES.MODE_CBC,key_info.get("iv").encode())
    #     plaintext = cipher.decrypt(base64.b64decode(qrcode))
    #     print(plaintext)
    #     log_object = eval(str("\'")+str(plaintext.decode())+str("\'"))
    #     serializer = self.get_serializer(data=log_object)
    #     serializer.is_valid(raise_exception=False)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED) # TODO





class GuestViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    """ POST """
    """ register """
    def create(self, request, *args, **kwargs):
        print(request.data)
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=request.data.get("code"))
        print(log_info)
        open_id = log_info.get("open_id")
        session_key = log_info.get("session_key")
        guest_object = request.data
        del guest_object["code"]
        guest_object["open_id"]=open_id
        serializer = self.get_serializer(data=guest_object)
        serializer.is_valid()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['GET'])
    def login(self,request):
        print(request.data)
        code = request.GET.get("code")
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        print(log_info)
        query = Guest.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuestSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            print(serializer.data)
            return Response(serializer.data[0])
        else:
            return Response({})
class GuardViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer
    """ POST """
    """ register """
    def create(self, request, *args, **kwargs):
        print(request.data)
        log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=request.data.get("code"))
        print(log_info)
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
        print(request.data)
        code = request.GET.get("code")
        log_info = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=code)
        print(log_info)
        query = Guard.objects.filter(open_id=log_info.get("open_id"))
        if query:
            serializer = GuardSerializer(data=list(query.values()),many=True)
            serializer.is_valid()
            print(serializer.data)
            return Response(serializer.data[0])
        else:
            return Response({})

from .utils import Test1Serializer,Test2Serializer
from .models import Test1,Test2
class Test1ViewSet(viewsets.ModelViewSet):
    queryset = Test1.objects.all()
    serializer_class = Test1Serializer
class Test2ViewSet(viewsets.ModelViewSet):
    queryset = Test2.objects.all()
    serializer_class = Test1Serializer
    def create(self,request,*args,**kwargs):
        open_id= request.data.get("open_id")
        print(Test2.objects.all())
        test1 = Test1.objects.get(open_id=open_id)
        test2 = Test2.objects.create(test1=test1,**{"name":"123123"})
        print(test2)
        return Response({})

# print(Log.objects.all().values())