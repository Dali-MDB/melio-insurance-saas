from rest_framework import serializers
from .models import Policy
from .utils import generate_policy_number

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id','policy_number','policyholder_name','policyholder_email','policy_type','coverage_amount','premium','start_date','end_date','is_active','tenant']
        read_only_fields = ['policy_number', 'tenant']

    
    def create(self, validated_data):
        number = generate_policy_number()
        #ensure uniqueness
        while Policy.objects.filter(policy_number=number).exists():   
            number = generate_policy_number()

        validated_data['policy_number'] = number
        return Policy.objects.create(**validated_data)