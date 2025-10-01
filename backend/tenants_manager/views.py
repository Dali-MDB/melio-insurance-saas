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
    serializer = RegistrationRequestSerializer(data=request.data)
    if serializer.is_valid():
        if Domain.objects.filter(domain=request.data['requested_domain']).exists():
            return Response({'error':'Domain already exists'}, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        instance.admin_password = make_password(instance.admin_password)
        instance.save()
        return Response({"message": "Registration submitted for review","application":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registration_requests(request:Request):
    requests = RegistrationRequest.objects.all()
    return Response(RegistrationRequestSerializer(requests).data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_registration_request(request:Request,request_id:int):
    reg_req = get_object_or_404(RegistrationRequest,pk=request_id)

    with schema_context('public'):
        insurance_company = InsuranceCompany.objects.create(
            name=reg_req.company_name,
            code=reg_req.requested_domain,
            logo=None,
            business_type=reg_req.business_type,
            contact_email=reg_req.contact_email,
            contact_phone=reg_req.company_phone,
            company_linkedin=reg_req.company_linkedin,
            default_currency=reg_req.default_currency,
            subscription_plan=reg_req.subscription_plan,
            address=reg_req.company_address,
        )
        domain = Domain.objects.create(
            domain=reg_req.requested_domain,
            tenant=insurance_company,
            is_primary=True,
        )
    with tenant_context(insurance_company):
        user = User.objects.create(
            email=reg_req.admin_email,
            username=reg_req.admin_username,
            phone_number=reg_req.admin_phone,
            role='admin',
            tenant=insurance_company,
            password=reg_req.admin_password,
        )
    #send email to admin (implement later)
    send_email(reg_req.admin_email, "Registration Approved", "Your registration has been approved\n\nYour login credentials are:\nEmail: {reg_req.admin_email}\nPassword: {reg_req.admin_password} \n\nPlease login to the platform via the following link: {domain.domain}")

    #delete the registration request
    reg_req.delete()
    return Response({"message": "Registration approved","insurance_company":InsuranceCompanySerializer(insurance_company).data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_registration_request(request:Request,request_id:int):
    reg_req = get_object_or_404(RegistrationRequest,pk=request_id)
    reg_req.delete()
    return Response({"message": "Registration rejected"}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_global_admin(request:Request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user = user_ser.save(scope='global',is_admin=True)
        return Response({"message": "Global admin added"}, status=status.HTTP_200_OK)
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    