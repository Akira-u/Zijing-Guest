from rest_framework import serializers
from django_filters import rest_framework as filters
from guest.models import Guest


class GuestFilter(filters.FilterSet):
    class Meta:
        model = Guest
        fields = {
            "student_id":["exact","icontains"],
            "name":["exact","icontains"],
            "is_student":["exact"],
            "credit":["exact"],
        }


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'
        extra_kwargs = {
            "phone":{"required": False},
            "student_id":{"required": False},
            "department":{"required": False}
        }
