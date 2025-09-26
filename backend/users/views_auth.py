from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer
from rest_framework.exceptions import APIException
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET'])
def test(request:Request):
    print(request.tenant.id)
    print(request.tenant)
    return Response('gg')


@api_view(['POST'])
def add_user(request:Request):
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