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


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'



class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = '__all__'
class LogSerializer(serializers.ModelSerializer):
    # guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all())
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {"out_time":{"required": False}}


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