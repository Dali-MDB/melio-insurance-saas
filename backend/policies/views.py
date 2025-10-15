from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Policy
from users.models import User
from .serializers import PolicySerializer
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from datetime import datetime
from rest_framework.response import Response
from django.db.models import Q
from .permissions import PolicyPermission
# Create your views here.



class ListCreatePolicy(ListCreateAPIView):
    """
    List and create insurance policies
    
    Goal: Get all policies or create new insurance policy
    Path: GET/POST /policies/
    Authentication: JWT required, PolicyPermission
    
    Request Body (POST):
    {
        "policy_number": "POL-2024-001",
        "policyholder_name": "John Doe",
        "policyholder_email": "john@example.com",
        "policy_type": "auto|home|life|health|business|travel|other",
        "coverage_amount": 50000.00,
        "premium": 1200.00,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    
    Response:
    - GET 200: [PolicySerializer objects]
    - POST 201: PolicySerializer object
    - POST 400: Validation errors
    """
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated,PolicyPermission]
    queryset = Policy.objects.all()
    

    def perform_create(self, serializer):
        #return super().perform_create(serializer)
        return serializer.save(tenant=self.request.tenant)
    

class GetEditDeletePolicy(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific policy
    
    Goal: Get policy details, update policy info, or delete policy
    Path: GET/PUT/PATCH/DELETE /policies/{policy_id}/
    Authentication: JWT required, PolicyPermission
    
    Request Body (PUT/PATCH):
    {
        "policyholder_name": "Updated Name",
        "policyholder_email": "updated@example.com",
        "coverage_amount": 75000.00,
        "premium": 1500.00,
        "is_active": true
    }
    
    Response:
    - GET 200: PolicySerializer object
    - PUT/PATCH 200: Updated PolicySerializer object
    - DELETE 204: No content
    - 404: Policy not found
    """
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated,PolicyPermission]
    queryset = Policy.objects.all()
    lookup_field = 'policy_id'

    def get_object(self):
        policy_id = self.kwargs.get('policy_id',None)
        return get_object_or_404(Policy,pk=policy_id)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def renew_policy(request: Request, policy_id: int):
    """
    Renew policy by updating start and end dates
    
    Goal: Extend policy coverage period with new dates
    Path: PUT/PATCH /policies/{policy_id}/renew/
    Authentication: JWT required
    
    Request Body:
    {
        "new_start_date": "2025-01-01",
        "new_end_date": "2025-12-31"
    }
    
    Response:
    - 200: {"detail": "the policy has been renewed successfully", "policy": PolicySerializer object}
    - 400: {"error": "please provide both start and end dates"}, {"error": "dates must be in YYYY-MM-DD format"}, or {"error": "start date must be earlier than end date"}
    - 404: Policy not found
    """
    policy = get_object_or_404(Policy, pk=policy_id)
    new_start_date_str = request.data.get('new_start_date')
    new_end_date_str = request.data.get('new_end_date')

    # Validate presence
    if not new_start_date_str or not new_end_date_str:
        return Response({'error': 'please provide both start and end dates'}, status=400)

    try:
        new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d").date()
        new_end_date = datetime.strptime(new_end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'dates must be in YYYY-MM-DD format'}, status=400)

    # Validate logical order
    if new_start_date >= new_end_date:
        return Response({'error': 'start date must be earlier than end date'}, status=400)

    # Update policy
    policy.start_date = new_start_date
    policy.end_date = new_end_date
    policy.save()

    return Response(
        {
            'detail': 'the policy has been renewed successfully',
            'policy': PolicySerializer(policy).data
        },
        status=200
    )


@api_view(['GET'])
def search_policy(request:Request):
    """
    Search policies by keyword
    
    Goal: Find policies matching search criteria
    Path: GET /policies/search/?key_word={keyword}
    Authentication: Not required
    
    Query Parameters:
    - key_word: Search term to match against policy_number, policyholder_name, or policyholder_email (optional)
    
    Response:
    - 200: [PolicySerializer objects] - List of matching policies
    - If no key_word provided: Returns all policies
    """
    key_word = request.GET.get('key_word',None)
    if not key_word:
        policies = Policy.objects.all()
    else:
        policies = Policy.objects.filter(
            Q(policy_number__icontains=key_word) |
            Q(policyholder_name__icontains=key_word) |
            Q(policyholder_email__icontains=key_word)
        )
    return Response(PolicySerializer(policies,many=True).data,200)


