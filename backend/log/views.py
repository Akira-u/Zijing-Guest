from datetime import date
from logging import log
from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Log
from guest.models import Guest
from dorm.models import Dorm, DormBuilding
from .utils import LogSerializer,LogFilter
from Crypto.Cipher import AES
from rest_framework.filters import OrderingFilter  # 导入排序

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
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter)
    filter_class = LogFilter
    ordering_fields = ('id',)
    """ POST """
    def create(self, request, *args, **kwargs):
        log_object = request.data
        try:
            qopen_id = decrypt(request.data.get("my_open_id"))
        except:
            return Response({"errmsg":"Invalid open_id"})
        try:
            guest_objects = Guest.objects.filter(open_id=qopen_id)
            guest_object=list(guest_objects)[0]
            if guest_object.is_student:
                guest_object.update(phone=request.data.get("phone"))
            dorm_object = Dorm.objects.filter(name=request.data.get("target_dorm")).last()
            dormbuilding_object = DormBuilding.objects.filter(name =request.data.get("target_building")).last()
        except:
            return Response({"errmsg":"Account Not Found"})
        try:
            open_id = guest_object.open_id
            log_object["guest_id"]=open_id # confusing???? 
            log_object["dorm_id"]=dorm_object.id
            log_object["dorm_building_id"]=dormbuilding_object.id
            serializer = self.get_serializer(data=log_object)
            serializer.is_valid(raise_exception=False)
            log_object = serializer.data
            log_object["guest_id"]=encrypt(log_object["guest_id"])
            log_object["guest"] = guest_object.__dict__
            log_object["dorm"] = dorm_object.__dict__
            log_object["dormbuilding"] = dormbuilding_object.__dict__
            del log_object["guest"]["_state"]
            del log_object["dorm"]["_state"]
            del log_object["dormbuilding"]["_state"]
            if cache.set(open_id,log_object, timeout=None):
                cache.persist(open_id)
                return Response(log_object, status=status.HTTP_201_CREATED)
            else:
                return Response({"errmsg":"You have a proceeding log"})
        except:
            return Response(serializer.errors)
    
    @action(detail=False,methods=["POST"])
    def check(self,request,*args, **kwargs):
        kwargs['partial'] = True
        if 1==1:
            open_id = decrypt(request.data.get("open_id"))
            ex_log = cache.get(open_id)
            cache.persist(open_id)
            if ex_log:
                if request.data.get("in_time"):
                    ex_log["in_time"]=request.data.get("in_time")
                    ex_log["approval"]=request.data.get("approval")
                    if ex_log["approval"]=="reject":
                        ex_log["guest_id"]=open_id
                        ex_log["out_time"]=request.data.get("in_time")
                        cache.delete_pattern(open_id)
                        ex_log["dormbuilding_id"]=ex_log["dorm"]["dormbuilding_id"]
                        serializer=self.get_serializer(data=ex_log)
                        serializer.is_valid(raise_exception=False)
                        if not serializer.errors:
                            self.perform_create(serializer)
                            return Response(serializer.data,status=status.HTTP_201_CREATED)
                        else:
                            return Response({"errmsg":serializer.errors})
                    else:
                        cache.delete_pattern(open_id)
                        cache.set(open_id,ex_log,timeout=None)
                        return Response({"msg":"Permit"})
                elif request.data.get("out_time"):
                    ex_log["out_time"]=request.data.get("out_time")
                    cache.delete_pattern(open_id)
                    ex_log["guest_id"]=open_id
                    ex_log["dormbuilding_id"]=ex_log["dorm"]["dormbuilding_id"]
                    serializer=self.get_serializer(data=ex_log)
                    serializer.is_valid(raise_exception=False)
                    if not serializer.errors:
                        self.perform_create(serializer)
                        return Response(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                        return Response({"errmsg":serializer.errors})
            else:
                raise Exception
        if 1==1:
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
            cache.persist(open_id)
            if not log_object:
                raise Exception
            log_object["guest_id"]= encrypt(open_id)
            return Response(log_object)
        except:
            return Response({"errmsg":"Log Not Found"})

    @action(detail=False,methods=["GET"])
    def static(self,request,*args,**kwargs):
        from datetime import datetime,timedelta
        from django.utils import timezone

        dt_s = timezone.now().date()-timedelta(6)
        student_log=[]
        other_log=[]
        total_log=[]
        student_log_weekday=[]
        other_log_weekday=[]
        total_log_weekday=[]
        student_log_hour=[]
        other_log_hour=[]
        total_log_hour=[]
        for i in range(7):
            dt_e=dt_s+timedelta(1)
            query = Log.objects.filter(in_time__range=[dt_s,dt_e])
            total = query.count()
            total_log.append(total)
            student_total=query.filter(guest__is_student=True).count()
            student_log.append(student_total)
            other_log.append(total-student_total)
            dt_s+=timedelta(1)
        for i in range(7):
            query = Log.objects.filter(in_time__week_day=i)
            total = query.count()
            total_log_weekday.append(total)
            student_total=query.filter(guest__is_student=True).count()
            student_log_weekday.append(student_total)
            other_log_weekday.append(total-student_total)
        hour=0
        for i in range(4):
            query = Log.objects.filter(in_time__hour__range=[hour,hour+5])
            total = query.count()
            total_log_hour.append({"name":f"{hour}-{hour+5}","value":total})
            hour+=6
        total_count = Log.objects.all().count()
        resp={
            "logs":{
                "student":student_log,
                "other":other_log,
                "total":total_log,
            },
            "logs_weekday":{
                "student":student_log_weekday,
                "other":other_log_weekday,
                "total":total_log_weekday,
            },
            "logs_hour":total_log_hour,
            "total_count":total_count
        }
        return Response(resp)

        

        
        

