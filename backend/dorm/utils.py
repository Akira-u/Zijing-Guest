from django.db.models import fields
from dorm.models import DormBuilding, Dorm
from rest_framework import serializers
from django_filters import rest_framework as filters
from rest_framework import validators
import re
class DormBuildingSerializer(serializers.ModelSerializer):
    def validate_name(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("Name must be string type")
        if data[:2]!="紫荆" or data[-2:]!="号楼" or (not re.match(r'$[1-9][0-9]{0,1}$',data[2:-2])):
            raise serializers.ValidationError("format error, example:紫荆x号楼, x=1,2,11...")
        return data
    class Meta:
        model = DormBuilding
        fields = '__all__'

class DormFilter(filters.FilterSet):
    class Meta:
        model = Dorm
        fields = {
            "dormbuilding_id":["exact"],
            "id":["exact"]
        }
class DormSerializer(serializers.ModelSerializer):
    def validate_student1(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("Name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$'):
            raise serializers.ValidationError("invalid name")
        return data
    def validate_student2(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("Name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$'):
            raise serializers.ValidationError("invalid name")
        return data
    def validate_student3(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("Name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$'):
            raise serializers.ValidationError("invalid name")
        return data
    def validate_student4(self,data):
        if not isinstance(data,str):
            raise serializers.ValidationError("Name must be string type")
        if not re.match(r'^[\u4E00-\u9FA5A-Za-z]{2,10}$'):
            raise serializers.ValidationError("invalid name")
        return data
    class Meta:
        model = Dorm
        fields = '__all__'
        extra_kwargs = {
            "student1":{"required": False},
            "student2":{"required": False},
            "student3":{"required": False},
            "student4":{"required": False},
        }