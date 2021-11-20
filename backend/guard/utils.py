from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Log, Guest, Guard,Test1,Test2
import requests

# TODO
# class LogFilter(filters.FilterSet):
#     sort = filters.OrderingFilter(fields=("id",""))
#     class Meta:
#         model = Log
#         fields = {
#             "id":["exact"],
#             "name":["icontains","exact"],
#             "custom_id":["icontains","exact"],
#         }

class LogSerializer(serializers.ModelSerializer):
    guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all())
    class Meta:
        model = Log
        fields = [
            "guest", # foreign key
            "purpose",
            "target_dorm",
            "host_student",
            "in_time",
            "out_time",
        ]
        extra_kwargs = {"out_time":{"required": False}}

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            "open_id", # primary key
            "name",
            "phone",
        ]



class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = [
            "open_id", # primary key
            "name",
            "phone",
        ]


class Test1Serializer(serializers.ModelSerializer):
    test2 = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Test1
        fields = '__all__'

class Test2Serializer(serializers.ModelSerializer):
    test1 = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Test2
        fields = '__all__'