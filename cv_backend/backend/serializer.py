from rest_framework import serializers
from .models import *


class OldPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = oldperson_info
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    oldperson_id = OldPersonSerializer(read_only=True)
    class Meta:
        model = event_info
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_info
        fields = '__all__'


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = volunteer_info
        fields = '__all__'


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = sys_user
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
