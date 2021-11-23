
from rest_framework import serializers
from api.models import APIInfo

class APIInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIInfo
        fields = "__all__"

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = APIInfo
        fields = "__all__"