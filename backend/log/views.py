from datetime import date
from logging import log
from os import stat_result
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
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
            qopen_id = request.data.get("my_open_id")
        except:
            return Response({"my_open_id":["please check your open_id in storage, it is invalid"]},status=status.HTTP_400_BAD_REQUEST)
        guest_object = Guest.objects.get(open_id=qopen_id)
        if not guest_object:
            return Response({"my_open_id":["no corrsponding guest account with your open_id"]},status=status.HTTP_400_BAD_REQUEST)
        if guest_object.is_student:
            guest_object.phone=request.data.get("phone")
            guest_object.save()
        try:
            dorm_object = Dorm.objects.get(id = request.data.get("target_dorm"))
        except:
            return Response({"dorm_object":["no corrsponding dorm with your target_dorm"]},status=status.HTTP_400_BAD_REQUEST)
        try:
            dormbuilding_object = DormBuilding.objects.get(id = request.data.get("target_dormbuilding"))
        except:
            return Response({"dormbuilding_object":["no corrsponding dormbuilding with your target_dormbuilding"]},status=status.HTTP_400_BAD_REQUEST)
        if dorm_object.dormbuilding != dormbuilding_object:
            return Response({"dorm and building":["no target dorm in your target building"]},status=status.HTTP_400_BAD_REQUEST)
        try:
            open_id = guest_object.open_id
            log_object["guest_id"]=open_id # confusing???? 
            log_object["dorm_id"]=dorm_object.id
            log_object["dorm_building_id"]=dormbuilding_object.id
            serializer = self.get_serializer(data=log_object)
            serializer.is_valid(raise_exception=True)
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        finally:
            log_object = serializer.data
            log_object["guest_id"]=encrypt(log_object["guest_id"])
            log_object["guest"] = guest_object.__dict__
            log_object["dorm"] = dorm_object.__dict__
            log_object["dormbuilding"] = dormbuilding_object.__dict__
            for i in range(1,5):
                if log_object["host_student"]==log_object["dorm"][f"student{i}"]:
                    break
                if i==4:
                    return Response({"host_student":["no corresponding student in your target dorm"]},status=status.HTTP_400_BAD_REQUEST)
            del log_object["guest"]["_state"]
            del log_object["dorm"]["_state"]
            del log_object["dormbuilding"]["_state"]
            if cache.set(open_id,log_object, timeout=None):
                cache.persist(open_id)
                return Response(log_object, status=status.HTTP_201_CREATED)
            else:
                return Response({"system cache":"cache error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False,methods=["POST"])
    def check(self,request,*args, **kwargs):
        kwargs['partial'] = True
        try:
            open_id = decrypt(request.data.get("open_id"))
        except:
            return Response({"open_id":["invalid open_id"]},status=status.HTTP_400_BAD_REQUEST)
        ex_log = cache.get(open_id)
        if not ex_log:
            return Response({"log":["no pending log, maybe timeout"]},status=status.HTTP_400_BAD_REQUEST)
        cache.persist(open_id)
        if request.data.get("in_time"):
            if ex_log.get("out_time"):
                return Response({"in_time":["already have a out_time"]},status=status.HTTP_400_BAD_REQUEST)
            ex_log["in_time"]=request.data.get("in_time")
            ex_log["approval"]=request.data.get("approval")
            if ex_log["approval"]=="reject":
                ex_log["guest_id"]=open_id
                ex_log["out_time"]=request.data.get("in_time")
                cache.delete_pattern(open_id)
                ex_log["dormbuilding_id"]=ex_log["dorm"]["dormbuilding_id"]
                serializer=self.get_serializer(data=ex_log)
                try:
                    serializer.is_valid(raise_exception=True)
                except:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                self.perform_create(serializer)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            elif ex_log["approval"]=="permit":
                cache.delete_pattern(open_id)
                cache.set(open_id,ex_log,timeout=None)
                return Response(ex_log,status=status.HTTP_200_OK)
        elif request.data.get("out_time"):
            ex_log["out_time"]=request.data.get("out_time")
            cache.delete_pattern(open_id)
            ex_log["guest_id"]=open_id
            ex_log["dormbuilding_id"]=ex_log["dorm"]["dormbuilding_id"]
            serializer=self.get_serializer(data=ex_log)
            try:
                serializer.is_valid(raise_exception=True)
            except:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
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
        code = request.GET.get("code")
        log_info = code2Session(appId=guest_appId, appSecret=guest_appSecret,code=code)
        open_id = log_info.get("open_id")
        if not open_id:
            return Response({"code":log_info["errmsg"]},status=status.HTTP_400_BAD_REQUEST)
        try:
            log_object = cache.get(open_id)
            cache.persist(open_id)
            if not log_object:
                raise Exception
            log_object["guest_id"]= encrypt(open_id)
            return Response(log_object,status=status.HTTP_200_OK)
        except:
            return Response({"log":["no log info for this guest,please fill in the form again"]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(resp,status=status.HTTP_200_OK)

        

        
        

