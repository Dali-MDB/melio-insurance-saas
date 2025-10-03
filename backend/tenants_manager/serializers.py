from rest_framework import serializers
from .models import RegistrationRequest, InsuranceCompany


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'
        read_only_fields = ['id','admin_password']



class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'