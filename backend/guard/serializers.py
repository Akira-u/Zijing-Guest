from rest_framework import serializers
from guard.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            'id', # primary key
            'name',
            'custom_id',
        ]