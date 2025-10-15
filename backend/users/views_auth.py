from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer
from rest_framework.exceptions import APIException
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CredResetCode
from .utils import generate_code
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def test(request:Request):
    """
    Development test endpoint
    
    Goal: Test tenant context and development environment
    Path: GET /users/
    Authentication: Not required
    
    Response:
    - 200: Test response with tenant information
    """
    print(request.tenant.id)
    print(request.tenant)
    return Response('gg')


@api_view(['POST'])
def add_user(request:Request):
    """
    Register new user in tenant system
    
    Goal: Create new user account within current tenant
    Path: POST /users/add-user/
    Authentication: Not required
    
    Request Body:
    {
        "email": "user@example.com",
        "username": "username",
        "phone_number": "+1234567890",
        "role": "call_center|adjuster|senior_adjuster|manager|admin",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepassword"
    }
    
    Response:
    - 200: {"success": true, "message": "the user has been added successfully", "user": UserSerializer object}
    - 400: Validation errors
    """
    #get the req body
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user = user_ser.save(tenant=request.tenant)
        return Response({
            'success':True,
            'message':'the user has been added successfully',
            'user':user_ser.data,
        },status=200)
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def login(request:Request):
    """
    User authentication and token generation
    
    Goal: Authenticate user credentials and generate JWT tokens
    Path: POST /users/login/
    Authentication: Not required
    
    Request Body:
    {
        "email": "user@example.com",
        "password": "userpassword"
    }
    
    Response:
    - 200: {"refresh": "jwt_refresh_token", "access": "jwt_access_token"}
    - 400: {"error": "email and password fields are required"}
    - 401: {"error": "Invalid credentials"}
    """
    email = request.data.get('email',None)
    password = request.data.get('password',None)

    if not email or not password:
        return  Response({'error':'email and password fields are required'},status=status.HTTP_400_BAD_REQUEST)
    
    #authenticate the user
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    #at this level the user is valid, so we generate tokens for him
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    tokens = {
            'refresh' : str(refresh_token),
            'access' : str(access_token)
        }
    return Response(tokens, status=status.HTTP_200_OK)

@api_view(['GET'])
def generate_reset_token(request:Request):
    """
    Generate password reset code
    
    Goal: Create 6-digit reset code for password recovery
    Path: GET /users/generate-reset-token/
    Authentication: Optional (uses authenticated user or email from body)
    
    Request Body (if not authenticated):
    {
        "email": "user@example.com"
    }
    
    Response:
    - 200: {"detail": "the reset code has been sent to you successfully"}
    - 400: {"error": "no email was provided"} or {"error": "no account with this email is registered into our system"}
    """
    if request.user.is_authenticated:
        user = request.user
        email = request.user.email
    else:
        email = request.data.get('email',None)
        if not email:
            return Response({'error':'no email was provided'},status=status.HTTP_400_BAD_REQUEST)
        #fetch the user
        user =  User.objects.filter(email=email).first()
        if not user:
            return Response({'error':'no account with this email is registered into our system'},status=status.HTTP_400_BAD_REQUEST)       
        
    
    code = CredResetCode.objects.filter(user=user).first()
    if code:   #delete it
        code.delete()
    #generate a new code
    code = CredResetCode.objects.create(user=user,code=generate_code(6))
    return Response({
        'detail':'the reset code has been sent to you successfully'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_email(request:Request):
    """
    Update user email address
    
    Goal: Change authenticated user's email address
    Path: POST /users/update-email/
    Authentication: JWT required
    
    Request Body:
    {
        "new_email": "newemail@example.com"
    }
    
    Response:
    - 200: {"detail": "the email has been updated successfully", "user": UserSerializer object}
    - 400: {"error": "new email is required"}, {"error": "new email is the same as the old email"}, or {"error": "new email is already in use"}
    """
    old_email = request.user.email
    new_email = request.data.get('new_email',None)
    if not new_email:
        return Response({'error':'new email is required'},status=status.HTTP_400_BAD_REQUEST)
    if new_email == old_email:
        return Response({'error':'new email is the same as the old email'},status=status.HTTP_400_BAD_REQUEST)
    #check if the new email is already in use
    if User.objects.filter(email=new_email).exists():
        return Response({'error':'new email is already in use'},status=status.HTTP_400_BAD_REQUEST)
    #update the email
    request.user.email = new_email
    request.user.save()
    return Response({'detail':'the email has been updated successfully','user':UserSerializer(request.user).data},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request:Request):
    """
    Update user password with validation
    
    Goal: Change authenticated user's password with old password verification
    Path: POST /users/update-password/
    Authentication: JWT required
    
    Request Body:
    {
        "old_password": "currentpassword",
        "new_password": "newpassword",
        "new_password_confirm": "newpassword"
    }
    
    Response:
    - 200: {"detail": "the password has been updated successfully", "user": UserSerializer object}
    - 400: {"error": "old password and new password are required"}, {"error": "old password is incorrect"}, or {"error": "new password and new password confirm do not match"}
    """
    old_password = request.data.get('old_password',None)
    new_password = request.data.get('new_password',None)
    new_password_confirm = request.data.get('new_password_confirm',None)
    if not old_password or not new_password or not new_password_confirm:
        return Response({'error':'old password and new password are required'},status=status.HTTP_400_BAD_REQUEST)
    #check if the old password is correct
    if not request.user.check_password(old_password):
        return Response({'error':'old password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
    if new_password != new_password_confirm:
        return Response({'error':'new password and new password confirm do not match'},status=status.HTTP_400_BAD_REQUEST)
    #update the password
    request.user.set_password(new_password)
    request.user.save()
    return Response({'detail':'the password has been updated successfully','user':UserSerializer(request.user).data},status=status.HTTP_200_OK)