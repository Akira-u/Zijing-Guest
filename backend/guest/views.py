from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Guest
from .utils import GuestSerializer
from log.utils import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from guard.wx_api import *
from guard.const import *

# Create your views here.
class GuestViewSet(viewsets.ModelViewSet):
    """ 人员信息 viewset """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    """ POST """
    """ register """
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
