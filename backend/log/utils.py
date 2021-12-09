from rest_framework import serializers
from django_filters import rest_framework as filters
from log.models import Log
from guest.utils import GuestSerializer

# TODO
class LogFilter(filters.FilterSet):
    in_time = filters.DateTimeFromToRangeFilter()
    out_time = filters.DateTimeFromToRangeFilter()
    class Meta:
        model = Log
        fields = {
            "guest__student_id":["exact","icontains"],
            "guest__name":["exact","icontains"],
            "guest__is_student":["exact"],
            "approval":["exact","in"],
        }


class LogSerializer(serializers.ModelSerializer):
    # guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all())
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            "out_time":{"required": False},
            "approval":{"required": False}
        }