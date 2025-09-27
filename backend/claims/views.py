from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from .models import Claim, ClaimDocument, ClaimNote
from users.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ClaimSerializer, ClaimNoteSerializer, ClaimDocumentSerializer
from rest_framework.permissions import IsAuthenticated
from policies.models import Policy
from django.shortcuts import get_object_or_404
from .utils import generate_claim_number, is_valid_uuid4
from rest_framework.request import Request
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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_claim(request:Request,claim_id:int):
    claim = get_object_or_404(Claim,pk=claim_id)
    user_id = request.GET.get('user_id',None)
    if not user_id:
        return Response({'error':'no user was provided'},status=400)
    if not is_valid_uuid4(user_id):
        return Response({'error':'please provide a valid uuid4 user_id'},status=400)
    user = get_object_or_404(User,pk=user_id)
    claim.assigned_to = user
    claim.save()
    return Response(ClaimSerializer(claim).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_note(request:Request,claim_id:int):
    claim = get_object_or_404(Claim,pk=claim_id)
    note_ser = ClaimNoteSerializer(data=request.data)
    if note_ser.is_valid():
        note = note_ser.save(author=request.user, claim=claim)
        return Response(ClaimNoteSerializer(note).data,201)
    return Response(note_ser.errors,400)

class NoteDetails(APIView):
    permission_classes = [IsAuthenticated]

    def fetch_note(self,note_id:int):
        return get_object_or_404(ClaimNote,pk=note_id)
    
    def get(self,request,note_id:int):
        note = self.fetch_note(note_id)
        return Response(ClaimNoteSerializer(note).data,200)

    def put(self,request,note_id:int):
        note = self.fetch_note(note_id)
        note_ser = ClaimNoteSerializer(note, data=request.data, partial = True)
        if note_ser.is_valid():
            note = note_ser.save()
            return Response(ClaimNoteSerializer(note).data,201)
        return Response(note_ser.errors,400)
    
    def delete(self,request,note_id:int):
        note = self.fetch_note(note_id)
        note.delete()
        return Response({'detail':'the hote has been deleted successfully'},200)
    



