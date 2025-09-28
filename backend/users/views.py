from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from .models import User
from claims.utils import is_valid_uuid4
from claims.serializers import ClaimSerializer
from claims.models import Claim
from .serializers import UserSerializer

# Create your views here.
@api_view(['GET'])
def view_user_profile(request:Request,user_id:str):
    if not is_valid_uuid4(user_id):
        return Response({'error':'please provide a valid uuid4 user_id'},status=400)
    user = get_object_or_404(User,pk=user_id)
    return Response(UserSerializer(user))



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_assigned_claims(request:Request,user_id:str):
    if not is_valid_uuid4(user_id):
        return Response({'error':'please provide a valid uuid4 user_id'},status=400)
    user = get_object_or_404(User,pk=user_id)
    assigned_claims = user.assigned_claims
    return Response(ClaimSerializer(assigned_claims,many=True).data,200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_role(request:Request):
    role = request.GET.get('role',None)
    if not role:
        return Response({'detail':'no role was provided'},400)
    
    users = User.objects.filter(role=role)
    return Response(UserSerializer(users).data)




