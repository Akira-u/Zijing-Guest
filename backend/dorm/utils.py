from django.db.models import fields
from dorm.models import DormBuilding, Dorm
from rest_framework import serializers
from django_filters import rest_framework as filters

class DormBuildingSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Dorm
        fields = '__all__'
        extra_kwargs = {
            "student1":{"required": False},
            "student2":{"required": False},
            "student3":{"required": False},
            "student4":{"required": False},
        }