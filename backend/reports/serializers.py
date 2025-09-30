from .models import Report
from rest_framework import serializers
from users.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Report
        fields = ['id','tenant','name','created_at','created_by','filters','report_data']


    def update(self, instance, validated_data):
        excluded_data = ['created_at','created_by']
        for v in excluded_data:                
            validated_data.pop(v,None)
        
        for key, val in validated_data.items():
            setattr(instance,key,val)
        
        instance.save()
        return instance
