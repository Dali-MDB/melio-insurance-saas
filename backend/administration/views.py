from django.shortcuts import render
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from tenants_manager.serializers import RegistrationRequestSerializer, InsuranceCompanySerializer
from users.serializers import UserSerializer
from tenants_manager.models import RegistrationRequest, InsuranceCompany, Domain
from users.models import User
from rest_framework import status
from django_tenants.utils import schema_context, tenant_context
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from tenants_manager.utils import send_email
from .utils import generate_valid_schema_name

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registration_requests(request:Request):
    with schema_context('public'):
        requests = RegistrationRequest.objects.all()
    return Response(RegistrationRequestSerializer(requests,many=True).data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_registration_request(request:Request,request_id:int):
    with schema_context('public'):
        reg_req = get_object_or_404(RegistrationRequest,pk=request_id)

    with schema_context('public'):
        schema_name = generate_valid_schema_name(reg_req.company_name)
        insurance_company = InsuranceCompany.objects.create(
            schema_name=schema_name,
            name=reg_req.company_name,
            code=3534335,
            logo=None,
            business_type=reg_req.business_type,
            contact_email=reg_req.contact_email,
            contact_phone=reg_req.company_phone,
            linkedin=reg_req.company_linkedin,
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
  #  send_email(reg_req.admin_email, "Registration Approved", "Your registration has been approved\n\nYour login credentials are:\nEmail: {reg_req.admin_email}\nPassword: {reg_req.admin_password} \n\nPlease login to the platform via the following link: {domain.domain}")

    #delete the registration request
    with schema_context('public'):
        reg_req.delete()
    return Response({
        "message": "Registration approved",
        "insurance_company":InsuranceCompanySerializer(insurance_company).data,
        "domain":domain.domain,
        },status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_registration_request(request:Request,request_id:int):
    with schema_context('public'):
        reg_req = get_object_or_404(RegistrationRequest,pk=request_id)
        reg_req.delete()
    return Response({"message": "Registration rejected"}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_global_admin(request:Request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user = user_ser.save(scope='global',is_admin=True)
        return Response({"message": "Global admin added","user":UserSerializer(user).data}, status=status.HTTP_200_OK)
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    