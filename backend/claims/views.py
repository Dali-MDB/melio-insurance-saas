from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from .models import Claim, ClaimDocument, ClaimNote
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ClaimSerializer
from rest_framework.permissions import IsAuthenticated
from policies.models import Policy
from django.shortcuts import get_object_or_404
from .utils import generate_claim_number
# Create your views here.



class ListCreateClaim(ListCreateAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]

    def get_policy(self):
        policy_id = self.kwargs['policy_id']
        return get_object_or_404(
            Policy, 
            id=policy_id, 
            tenant=self.request.user.tenant
        )
    
    def get_queryset(self):
        policy = self.get_policy()
        return Claim.objects.filter(policy=policy)
    
    def perform_create(self, serializer):
        policy = self.get_policy()
        number = generate_claim_number()
        serializer.save(
            policy=policy,
            tenant=self.request.tenant,
            claim_number = number
        )


class GetEditDeleteClaim(RetrieveUpdateDestroyAPIView):
    serializer_class = ClaimSerializer
    queryset = Claim.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'claim_id'

    def get_object(self):
        claim_id = self.kwargs.get('claim_id',None)
        return get_object_or_404(Claim,pk=claim_id)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)