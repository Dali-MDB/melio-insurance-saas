from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','email','username','phone_number','is_admin','role','tenant','scope','password']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        scope = attrs.get('scope', getattr(self.instance, 'scope', None))
        tenant = attrs.get('tenant', getattr(self.instance, 'tenant', None))
        
        if scope == 'global' and tenant is not None:
            raise serializers.ValidationError({
                'tenant': 'Tenant must be null for global scope users'
            })
        elif scope == 'tenant' and tenant is None:
            raise serializers.ValidationError({
                'tenant': 'Tenant is required for tenant scope users'
            })
        
        return attrs
    
    def create(self, validated_data):
         # Extract the required positional arguments
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password', None)
        
        # Call create_user with proper arguments
        return User.objects.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            password=password,
            **validated_data  # remaining fields go as extra_fields
        )