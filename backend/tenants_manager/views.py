from django.shortcuts import render
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationRequestSerializer, InsuranceCompanySerializer
from users.serializers import UserSerializer
from .models import RegistrationRequest, InsuranceCompany, Domain
from users.models import User
from rest_framework import status
from django_tenants.utils import schema_context, tenant_context
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from .utils import send_email

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request:Request):
    """
    Submit insurance company registration request
    
    Goal: Submit new insurance company registration for platform approval
    Path: POST /register/
    Authentication: Not required
    
    Request Body:
    {
        "company_name": "ABC Insurance Co.",
        "business_type": "auto|health|property|life|multi_line",
        "company_phone": "+1234567890",
        "contact_email": "contact@abcinsurance.com",
        "company_address": "123 Main St, City, State",
        "company_linkedin": "https://linkedin.com/company/abc-insurance",
        "default_currency": "USD",
        "subscription_plan": "basic|pro",
        "requested_domain": "abcinsurance",
        "admin_email": "admin@abcinsurance.com",
        "admin_phone": "+1234567890",
        "admin_first_name": "John",
        "admin_last_name": "Doe",
        "admin_username": "admin",
        "admin_password": "securepassword"
    }
    
    Response:
    - 201: {"message": "Registration submitted for review", "application": RegistrationRequestSerializer object}
    - 400: {"error": "Domain already exists"} or validation errors
    """
    serializer = RegistrationRequestSerializer(data=request.data)
    if serializer.is_valid():
        request.data['requested_domain']+=".localhost"
        if Domain.objects.filter(domain=request.data['requested_domain']).exists() or RegistrationRequest.objects.filter(requested_domain=request.data['requested_domain']).exists():
            return Response({'error':'Domain already exists'}, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        instance.admin_password = make_password(instance.admin_password)
        instance.save()
        return Response({"message": "Registration submitted for review","application":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registration_requests(request:Request):
    """
    Get all registration requests (public schema)
    
    Goal: Retrieve all pending registration requests from public schema
    Path: GET /registration-requests/
    Authentication: JWT required
    
    Response:
    - 200: [RegistrationRequestSerializer objects] - List of all requests
    """
    requests = RegistrationRequest.objects.all()
    return Response(RegistrationRequestSerializer(requests).data)



