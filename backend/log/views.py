from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import Log
from guest.models import Guest
from .utils import LogSerializer
from Crypto.Cipher import AES

from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guard.wx_api import *
from guard.const import *
from guard.cipher import *

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
        log_object = request.data
        try:
            qopen_id = decrypt(request.data.get("open_id"))
        except:
            return Response({"errmsg":"Invalid open_id"})
        try:
            guest_objects = Guest.objects.filter(open_id=qopen_id)
            guest_object=list(guest_objects)[0]
        except:
            return Response({"errmsg":"Account Not Found"})
        try:
            open_id = guest_object.open_id
            log_object["guest_id"]=open_id # confusing???? 
            print(log_object)
            serializer = self.get_serializer(data=log_object)
            serializer.is_valid(raise_exception=True)
            log_object = serializer.data
            print(log_object)
            del log_object["guest_id"]
            log_object["guest_name"]=guest_object.name
            if cache.set(open_id,log_object, nx=True):
                print(cache.get(open_id))
                return Response(log_object, status=status.HTTP_201_CREATED)
            else:
                return Response({"errmsg":"You have a proceeding log"})
        except:
            print(serializer.errors)
            return Response(serializer.errors)
    
    @action(detail=False,methods=["POST"])
    def check(self,request,*args, **kwargs):
        kwargs['partial'] = True
        print("patch")
        try:
            # lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            open_id = decrypt(request.data.get("open_id")) 
            # print(open_id)
            ex_log = cache.get(open_id)
            print(ex_log)
            print(request.data)
            if ex_log:
                if request.data.get("in_time"):
                    ex_log["in_time"]=request.data.get("in_time")
                    ex_log["approval"]=request.data.get("approval")
                    if ex_log["approval"]=="reject":
                        cache.delete_pattern(open_id)
                        return Response({"msg":"Reject"})
                    else:
                        print("1")
                        cache.delete_pattern(open_id)
                        print("2")
                        cache.set(open_id,ex_log)
                        print("3")
                        return Response({"msg":"Permit"})
                elif request.data.get("out_time"):
                    ex_log["out_time"]=request.data.get("out_time")
                    cache.delete_pattern(open_id)
                    ex_log["guest_id"]=open_id
                    serializer=self.get_serializer(data=ex_log)
                    serializer.is_valid(raise_exception=False)
                    if not serializer.errors:
                        self.perform_create(serializer)
                        return Response(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                        return Response({"errmsg":serializer.errors})
            else:
                raise Exception
        except:
            return Response({"errmsg":"proceeding log not found, maybe timeout."})
    @swagger_auto_schema(
    operation_summary='根据guset的code返回最近的一条log',
    manual_parameters=[
        openapi.Parameter(
            name='code',
            in_=openapi.IN_QUERY,
            description='Guest code',
            type=openapi.TYPE_STRING
        ),],
    responses={200:openapi.Response('response guest latest log info',LogSerializer)}
    )
    @action(detail=False,methods=["GET"])
    def info(self,request,*args, **kwargs):
        try:
            code = request.GET.get("code")
            log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        except:
            return Response({"errmsg":log_info["errmsg"]})
        try:    
            open_id = log_info.get("open_id")
            log_object = cache.get(open_id)
            # print(log_object)
            if not log_object:
                raise Exception
            
            log_object["guest_id"]= encrypt(open_id)
            return Response(log_object)
        except:
            return Response({"errmsg":"Log Not Found"})

