from django.db.models import fields
from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Guard
from dorm.utils import DormBuildingSerializer
import requests


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
    class Meta:
        model = Guard
        fields = '__all__'



