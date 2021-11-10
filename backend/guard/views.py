from django.shortcuts import render
from rest_framework import viewsets
from .serializers import LogSerializer
# Create your views here.

from guard.models import Log
class LogViewSet(viewsets.ModelViewSet):
    """ 来访日志 viewset """
    queryset = Log.objects.all()
    serializer_class = LogSerializer