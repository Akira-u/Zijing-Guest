from rest_framework import serializers
from django_filters import rest_framework as filters
from guest.models import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

