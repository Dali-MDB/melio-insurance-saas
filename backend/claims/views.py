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
from .utils import generate_claim_number, is_valid_uuid4, is_valid_status_transition
from rest_framework.request import Request
from .permissions import ClaimCreationPermission, ClaimPermissions, AssignClaimPermission, CreateClaimNotePermission, CreateClaimDocumentPermission, ClaimNotePermissions, ClaimDocumentPermissions, UpdateClaimStatusPermission
# Create your views here.



class ListCreateClaim(ListCreateAPIView):
    """
    List and create claims for a specific policy
    
    Goal: Get all claims for a policy or create a new claim
    Path: GET/POST /policy/{policy_id}/claims/
    Authentication: JWT required, ClaimCreationPermission
    
    Request Body (POST):
    {
        "title": "Claim title",
        "description": "Detailed claim description",
        "claim_amount": 5000.00,
        "incident_date": "2024-01-15"
    }
    
    Response:
    - GET 200: [ClaimSerializer objects]
    - POST 201: ClaimSerializer object with auto-generated claim_number
    - POST 400: {"field_name": ["error message"]}
    """
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated, ClaimCreationPermission]

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
    """
    Retrieve, update or delete a specific claim
    
    Goal: Get claim details, update claim info, or delete claim
    Path: GET/PUT/PATCH/DELETE /policy/{policy_id}/claims/{claim_id}/
    Authentication: JWT required, ClaimPermissions
    
    Request Body (PUT/PATCH):
    {
        "title": "Updated claim title",
        "description": "Updated description",
        "claim_amount": 7500.00,
        "approved_amount": 6000.00
    }
    
    Response:
    - GET 200: ClaimSerializer object
    - PUT/PATCH 200: Updated ClaimSerializer object
    - DELETE 204: No content
    - 404: Claim not found
    """
    serializer_class = ClaimSerializer
    queryset = Claim.objects.all()
    permission_classes = [IsAuthenticated, ClaimPermissions]
    lookup_field = 'claim_id'

    def get_object(self):
        claim_id = self.kwargs.get('claim_id',None)
        return get_object_or_404(Claim,pk=claim_id)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated, AssignClaimPermission])
def assign_claim(request:Request,claim_id:int):
    """
    Assign a claim to a specific user
    
    Goal: Assign claim to adjuster, senior adjuster, or manager
    Path: POST /claims/{claim_id}/assign/?user_id={uuid}
    Authentication: JWT required, AssignClaimPermission
    
    Query Parameters:
    - user_id: UUID4 of the user to assign claim to
    
    Response:
    - 200: Updated ClaimSerializer object with assigned_to field
    - 400: {"error": "no user was provided"} or {"error": "please provide a valid uuid4 user_id"}
    - 404: Claim or User not found
    """
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
@permission_classes([IsAuthenticated, CreateClaimNotePermission])
def add_note(request:Request,claim_id:int):
    """
    Add a note to a claim
    
    Goal: Add internal or external note to existing claim
    Path: POST /claims/{claim_id}/add-note/
    Authentication: JWT required, CreateClaimNotePermission
    
    Request Body:
    {
        "note": "Note content",
        "is_internal": true
    }
    
    Response:
    - 201: Created ClaimNoteSerializer object
    - 400: Validation errors
    - 404: Claim not found
    """
    claim = get_object_or_404(Claim,pk=claim_id)
    note_ser = ClaimNoteSerializer(data=request.data)
    if note_ser.is_valid():
        note = note_ser.save(author=request.user, claim=claim)
        return Response(ClaimNoteSerializer(note).data,201)
    return Response(note_ser.errors,400)


class NoteDetails(APIView):
    """
    Retrieve, update or delete a specific claim note
    
    Goal: Get note details, update note content, or delete note
    Path: GET/PUT/DELETE /notes/{note_id}/
    Authentication: JWT required, ClaimNotePermissions
    
    Request Body (PUT):
    {
        "note": "Updated note content",
        "is_internal": false
    }
    
    Response:
    - GET 200: ClaimNoteSerializer object
    - PUT 201: Updated ClaimNoteSerializer object
    - DELETE 200: {"detail": "the note has been deleted successfully"}
    - 404: Note not found
    """
    permission_classes = [IsAuthenticated, ClaimNotePermissions]

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
    


@api_view(['POST'])
@permission_classes([IsAuthenticated, CreateClaimDocumentPermission])
def add_document(request:Request,claim_id:int):
    """
    Upload and attach document to a claim
    
    Goal: Upload document files (photos, reports, estimates) to claim
    Path: POST /claims/{claim_id}/add-document/
    Authentication: JWT required, CreateClaimDocumentPermission
    
    Request Body (multipart/form-data):
    {
        "document_type": "photo|police_report|estimate|medical_bill|invoice|other",
        "file": "uploaded_file",
        "description": "Optional description"
    }
    
    Response:
    - 201: Created ClaimDocumentSerializer object
    - 400: Validation errors
    - 404: Claim not found
    """
    claim = get_object_or_404(Claim,pk=claim_id)
    note_ser = ClaimDocumentSerializer(data=request.data)
    if note_ser.is_valid():
        note = note_ser.save(uploaded_by=request.user, claim=claim)
        return Response(ClaimDocumentSerializer(note).data,201)
    return Response(note_ser.errors,400)


class documentDetails(APIView):
    """
    Retrieve, update or delete a specific claim document
    
    Goal: Get document details, update document metadata, or delete document
    Path: GET/PUT/DELETE /documents/{document_id}/
    Authentication: JWT required, ClaimDocumentPermissions
    
    Request Body (PUT):
    {
        "document_type": "updated_type",
        "description": "Updated description"
    }
    
    Response:
    - GET 200: ClaimDocumentSerializer object
    - PUT 201: Updated ClaimDocumentSerializer object
    - DELETE 200: {"detail": "the document has been deleted successfully"}
    - 404: Document not found
    """
    permission_classes = [IsAuthenticated, ClaimDocumentPermissions]

    def fetch_document(self,document_id:int):
        return get_object_or_404(ClaimDocument,pk=document_id)
    
    def get(self,request,document_id:int):
        document = self.fetch_document(document_id)
        return Response(ClaimDocumentSerializer(document).data,200)

    def put(self,request,document_id:int):
        document = self.fetch_document(document_id)
        document_ser = ClaimDocumentSerializer(document, data=request.data, partial = True)
        if document_ser.is_valid():
            document = document_ser.save()
            return Response(ClaimDocumentSerializer(document).data,201)
        return Response(document_ser.errors,400)
    
    def delete(self,request,document_id:int):
        document = self.fetch_document(document_id)
        document.delete()
        return Response({'detail':'the hote has been deleted successfully'},200)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, UpdateClaimStatusPermission])
def update_claim_status(request:Request,claim_id:int):
    """
    Update claim status following valid state transitions
    
    Goal: Change claim status through approved workflow states
    Path: PUT /claims/{claim_id}/update-status/?new_status={status}
    Authentication: JWT required, UpdateClaimStatusPermission
    
    Query Parameters:
    - new_status: One of [reported, assigned, under_review, investigation, 
      documents_requested, waiting_approval, approved, denied, 
      payment_processing, paid, closed]
    
    Response:
    - 200: Updated ClaimSerializer object with new status
    - 400: {"detail": "no status query parameter has been provided"} or 
      {"detail": "the transition to the new status you have provided is not approved"}
    - 404: Claim not found
    """
    claim = get_object_or_404(Claim,pk=claim_id)
    new_status = request.GET.get('new_status',None)
    if not new_status:
        return Response({'detail':'no status query parameter has been provided'},400)

    if not is_valid_status_transition(claim.status, new_status):
        return Response({'detail':'the transition to the new status you have provided is not approved'},400)
    
    #update the status
    claim.status = new_status
    claim.save()
    return Response(ClaimSerializer(claim).data,200)


