from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Log, User, Guard
import requests

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', # primary key
            'name',
            'open_id',
            'phone',
        ]
        extra_kwargs = {'open_id': {'allow_null': False}}



class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = [
            'id', # primary key
            'name',
            'open_id',
            'phone',
        ]
        extra_kwargs = {'open_id': {'required': False}}
