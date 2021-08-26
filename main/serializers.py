from django.db.models import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PatientTestData(serializers.Serializer):
    "this data will not be saved to any model"
    heart_rate = serializers.CharField()
    oxygen_level = serializers.CharField()
    temperature = serializers.CharField()

    