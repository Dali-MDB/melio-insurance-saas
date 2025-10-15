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
    """
    View user profile information
    
    Goal: Get public profile information for a user
    Path: GET /users/{user_id}/
    Authentication: Not required
    
    Path Parameters:
    - user_id: UUID4 format user identifier
    
    Response:
    - 200: UserSerializer object with profile data
    - 400: {"error": "please provide a valid uuid4 user_id"}
    - 404: User not found
    """
    if not is_valid_uuid4(user_id):
        return Response({'error':'please provide a valid uuid4 user_id'},status=400)
    user = get_object_or_404(User,pk=user_id)
    return Response(UserSerializer(user))



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_assigned_claims(request:Request,user_id:str):
    """
    Get all claims assigned to a specific user
    
    Goal: Retrieve all claims assigned to a user (adjuster, manager, etc.)
    Path: GET /users/{user_id}/claims/
    Authentication: JWT required
    
    Path Parameters:
    - user_id: UUID4 format user identifier
    
    Response:
    - 200: [ClaimSerializer objects] - List of assigned claims
    - 400: {"error": "please provide a valid uuid4 user_id"}
    - 404: User not found
    """
    if not is_valid_uuid4(user_id):
        return Response({'error':'please provide a valid uuid4 user_id'},status=400)
    user = get_object_or_404(User,pk=user_id)
    assigned_claims = user.assigned_claims
    return Response(ClaimSerializer(assigned_claims,many=True).data,200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_role(request:Request):
    """
    Get users filtered by role
    
    Goal: Retrieve all users with a specific role
    Path: GET /users/?role={role}
    Authentication: JWT required
    
    Query Parameters:
    - role: One of [call_center, adjuster, senior_adjuster, manager, admin]
    
    Response:
    - 200: [UserSerializer objects] - List of users with specified role
    - 400: {"detail": "no role was provided"}
    """
    role = request.GET.get('role',None)
    if not role:
        return Response({'detail':'no role was provided'},400)
    
    users = User.objects.filter(role=role)
    return Response(UserSerializer(users).data)




