from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Policy
from users.models import User
from .serializers import PolicySerializer
from django.shortcuts import get_object_or_404
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


