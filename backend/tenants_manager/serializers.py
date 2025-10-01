from rest_framework import serializers
from .models import RegistrationRequest


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'
        read_only_fields = ['id','admin_password']