from django.db.models import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OtherReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherReports
        fields = ['user','pulse_rate','saturation_ratio', 'oxygen_level', 'temperature']

    def validate(self, attrs):
        print(attrs)

    def create(self, validated_data):
        pass

