from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import serializers, viewsets, status
from django_filters import rest_framework as filters
from rest_framework.utils import serializer_helpers
from guard.models import Guard
from guard.utils import GuardSerializer
from log.utils import LogSerializer
from rest_framework.filters import OrderingFilter  # 导入排序

from dorm.models import Dorm, DormBuilding
from dorm.utils import DormBuildingSerializer,DormSerializer,DormFilter
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class DormBuildingViewSet(viewsets.ModelViewSet):
    queryset = DormBuilding.objects.all()
    serializer_class = DormBuildingSerializer
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter)


class DormViewSet(viewsets.ModelViewSet):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter)
    filter_class = DormFilter
    # 批量创建/更新(excel导入)
    @action(detail=False,methods=["POST"])
    def bulk_create(self,request,*args,**kwargs):
        dorm_list = [i for i in request.data.get("list")]
        for dorm in dorm_list:
            dorm.update(dormbuilding_id=request.data.get("dormbuilding_id"))
            Dorm.objects.update_or_create(defaults=dorm,**{"name":dorm.get("name"),"dormbuilding_id":dorm.get("dormbuilding_id")})
        return Response(status=status.HTTP_201_CREATED)
    # 统计信息
    @action(detail=False,methods=["GET"])
    def static(self,request,*args,**kwargs):
        query = DormBuilding.objects.all()
        resp={
            "dorms":{},
            "total_count":query.count()
        }
        return Response(resp,status=status.HTTP_200_OK)
