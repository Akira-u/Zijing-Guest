from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Log

class LogFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id','custom_id'))
    class Meta:
        model = Log
        fields = {
            'id':['exact'],
            'name':['icontains','exact'],
            'custom_id':['icontains','exact'],
        }
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            'id', # primary key
            'name',
            'custom_id',
        ]