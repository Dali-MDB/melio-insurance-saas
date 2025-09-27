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
# Create your views here.



class ListCreatePolicy(ListCreateAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]
    queryset = Policy.objects.all()
    

    def perform_create(self, serializer):
        #return super().perform_create(serializer)
        return serializer.save(tenant=self.request.tenant)
    

class GetEditDeletePolicy(RetrieveUpdateDestroyAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]
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


