from rest_framework import serializers
from django_filters import rest_framework as filters
from guard.models import Guard
import requests


class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = '__all__'



