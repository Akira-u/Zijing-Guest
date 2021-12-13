from rest_framework import serializers
from django_filters import rest_framework as filters
from guest.models import Guest
import re

class GuestFilter(filters.FilterSet):
    class Meta:
        model = Guest
        fields = {
            "student_id":["exact","icontains"],
            "name":["exact","icontains"],
            "is_student":["exact"],
            "credit":["exact"],
        }

class GuestSerializer(serializers.ModelSerializer):
    def validate_name(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$',data):
            raise serializers.ValidationError("invalid name")
        return data
    def validate_phone(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("phone must be string type")
        if not re.match(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',data):
            raise serializers.ValidationError("invalid phone number")
        return data
        
    class Meta:
        model = Guest
        fields = '__all__'
        extra_kwargs = {
            "phone":{"required": False},
            "student_id":{"required": False},
            "department":{"required": False}
        }
