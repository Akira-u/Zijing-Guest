from rest_framework import serializers
from guard.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            'name',
            'custom_id',
        ]