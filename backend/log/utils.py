from rest_framework import serializers
from django_filters import rest_framework as filters
from log.models import Log
from guest.utils import GuestSerializer
from dorm.utils import DormSerializer,DormBuildingSerializer
from dorm.models import Dorm,DormBuilding

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
            "guest__open_id":["exact"]
        }


class LogSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.CharField(allow_null=True, required=False)
    dorm = DormSerializer(read_only=True)
    dorm_id = serializers.IntegerField(allow_null=True, required=False)
    dormbuilding = DormBuildingSerializer(read_only=True)
    dormbuilding_id = serializers.IntegerField(allow_null=True, required=False)
    def validate(self, data):
        # print(data)
        if not data.get("in_time") or not data.get("out_time"):
            return data
        if data['in_time'] > data['out_time']:
            raise serializers.ValidationError("in time should earlier than out time")
        # if DormBuilding.objects.get(id=data.get("dormbuilding").get("id")) == :
        return data
    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            "out_time":{"required": False},
            "approval":{"required": False}
        }