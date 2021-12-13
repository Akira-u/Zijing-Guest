from django.db.models import fields
from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Guard
from dorm.utils import DormBuildingSerializer
import requests
import re

class GuardFilter(filters.FilterSet):
    class Meta:
        model = Guard
        fields = {
            "dormbuilding__name":["exact","icontains"],
            "name":["exact","icontains"],
            "phone":["exact","icontains"],
            "open_id":["exact"]
        }
class GuardSerializer(serializers.ModelSerializer):
    dormbuilding = DormBuildingSerializer(read_only=True)
    dormbuilding_id = serializers.IntegerField(allow_null=True, required=False)
    def validate_name(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$'):
            raise serializers.ValidationError("invalid name")
        return data
    def validate_phone(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("phone must be string type")
        if not re.match(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',data):
            raise serializers.ValidationError("invalid phone number")
        return data
    # impossible to validate open_id before create.
    class Meta:
        model = Guard
        fields = '__all__'



