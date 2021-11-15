from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import User
from .utils import LogSerializer,LogFilter,UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

import requests
# Create your views here.

from guard.models import Log
class LogViewSet(viewsets.ModelViewSet):
    """ 来访日志 viewset """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = LogFilter

class UserViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data["code"]
        appId = "wxd658ab1f82314e2a"
        appSecret = "815767c2cf0359f4910dee4136de0962"
        # code = "111"
        payload = { 
            "appid": appId,
            "secret": appSecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        print(payload)
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session',params=payload)
        packet = eval(r.text)
        openid=""
        session_key=""
        unionid="" # discard in iter stage 1
        print(packet)
        # if packet.get("errcode")==0:
        #     openid = packet.get("openid")
        #     session_key = packet.get("session_key")
        # else: print("code2session error")
        openid = packet.get("openid")
        session_key = packet.get("session_key")
        user_object = serializer.data
        user_object["open_id"]=openid
        print(user_object)
        User.objects.create(**user_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False,methods=['GET'])
    def login(self,request):
        print(request.data)
        appId = "wxd658ab1f82314e2a"
        appSecret = "815767c2cf0359f4910dee4136de0962"
        # code = "111"
        payload = { 
            "appid": appId,
            "secret": appSecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        print(payload)
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session',params=payload)
        packet = eval(r.text)
        openid=""
        session_key=""
        unionid="" # discard in iter stage 1
        
        query = User.objects.filter(open_id=packet.get("openid"))
        serializer = self.get_serializer(data=query.all())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       

            
        
        
