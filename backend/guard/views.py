from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import User, Guard
from .utils import LogSerializer,LogFilter,UserSerializer, GuardSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .wx_api import *
import requests
from Crypto.Cipher import AES
from .const import *

# Create your views here.
from guard.models import Log


class LogViewSet(viewsets.ModelViewSet):
    """ 来访日志 viewset """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = LogFilter
    def create(self, request, *args, **kwargs):
        print(request.data) # string type
        raw = request.data.get("code")
        splited = raw.split("==")
        print(splited)
        qrcode = splited[0]+"=="
        code = splited[1]

        access_token = getAccessToken(appId=guest_appId, appSecret=guest_appSecret)
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=code )
        key_info = getUserEncryptKey(access_token, log_info.get("open_id"), log_info.get("session_key"))
        cipher = AES.new(key_info.get("encrypt_key").encode(), AES.MODE_CBC,key_info.get("iv").encode())
        plaintext = cipher.decrypt(base64.b64decode(qrcode))
        print(plaintext)
        log_object = eval(str("\'")+str(plaintext.decode())+str("\'"))
        serializer = self.get_serializer(data=log_object)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # TODO





class UserViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data["code"]
        resp = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        print(resp)
        open_id = resp.get("open_id")
        session_key = packet.get("session_key")
        user_object = serializer.data
        user_object["open_id"]=open_id
        print(user_object)
        User.objects.create(**user_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False,methods=['GET'])
    def login(self,request):
        print(request.data)
        code = request.GET.get("code")
        resp = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        print(resp)
        query = User.objects.filter(open_id=resp.get("open_id"))
        serializer = self.get_serializer(data=query.all())
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # TODO

class GuardViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data["code"]
        resp = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=code)
        print(resp)
        open_id = resp.get("open_id")
        session_key = packet.get("session_key")
        Guard_object = serializer.data
        Guard_object["open_id"]=open_id
        print(Guard_object)
        Guard.objects.create(**Guard_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False,methods=['GET'])
    def login(self,request):
        code = request.GET.get("code")
        resp = code2Session(appId=guard_appId, appSecret=guard_appSecret,code=code)
        print(resp)
        query = Guard.objects.filter(open_id=resp.get("open_id"))
        # print(list(query.all())[0].open_id)
        serializer = self.get_serializer(data=list(query.all()),many=True)
        serializer.is_valid(raise_exception=False)
        print(serializer.data)
        return Response(serializer.data[0], status=status.HTTP_201_CREATED)