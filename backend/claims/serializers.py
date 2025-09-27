from rest_framework import serializers
from .models import Claim, ClaimDocument, ClaimNote
from policies.serializers import PolicySerializer
from users.serializers import UserSerializer


class ClaimDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDocument
        fields = '__all__'
        read_only_fields = ['created_at','uploaded_by','claim']
        

        def update(self, instance, validated_data):
            excluded_data = ['created_at','claim','uploaded_by']
            for v in excluded_data:                
                validated_data.pop(v,None)
            
            for key, val in validated_data.items():
                setattr(instance,key,val)
            
            instance.save()
            return instance


class ClaimNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimNote
        fields = '__all__'
        read_only_fields = ['created_at','author','claim']

        def update(self, instance, validated_data):
            excluded_data = ['created_at','claim','author']
            for v in excluded_data:                
                validated_data.pop(v,None)
            
            for key, val in validated_data.items():
                setattr(instance,key,val)
            
            instance.save()
            return instance
            
            


class ClaimSerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    documents = ClaimDocumentSerializer(many=True, read_only=True)
    notes = ClaimNoteSerializer(many=True, read_only=True)
    class Meta:
        model = Claim
        fields = ['id','claim_number' ,'tenant' ,'policy','title' ,'description' ,'claim_amount' ,'approved_amount' ,'assigned_to' ,'incident_date' ,'created_at' ,'updated_at','documents', 'notes' ]
        read_only_fields = ['id','claim_number','tenant','policy','assigned_to','created_at' ,'updated_at']

    


