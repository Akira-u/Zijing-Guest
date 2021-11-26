from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Log
from guest.models import Guest
from .utils import LogSerializer

from rest_framework.response import Response
from rest_framework.decorators import action

from guard.wx_api import *
from guard.const import *

from django.core.cache import cache
# Create your views here.

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
        del log_object["code"]
        guest_objects = Guest.objects.filter(open_id=log_info.get("open_id"))
        guest_object=list(guest_objects)[0]
        open_id = guest_object.open_id
        log_object["guest_id"]=open_id # confusing???? 
        # if cache.has(open_id):
        #     cache.delete(open_id)
        # cache.set(open_id,log_object)
        # return Response(log_object,status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=log_object)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    """ GET """
    @action(detail=False,methods=["GET"])
    def info(self,request):
        log_info = code2Session(appId =guest_appId,appSecret=guest_appSecret,code=request.GET.get("code"))
        instance = Log.objects.filter(guest__open_id=log_info.get("open_id"))
        serializer = self.get_serializer(data=list(instance.values())[-1])
        serializer.is_valid(raise_exception=False)
        resp = serializer.validated_data
        resp["guest"] = (Guest.objects.filter(open_id=resp.get("guest_id")).values())[0].get("name")
        resp["id"]=instance.last().id
        print(resp)
        return Response(resp)


