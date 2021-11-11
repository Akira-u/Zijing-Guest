from django.shortcuts import render
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .utils import LogSerializer,LogFilter
# Create your views here.

from guard.models import Log
class LogViewSet(viewsets.ModelViewSet):
    """ 来访日志 viewset """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = LogFilter