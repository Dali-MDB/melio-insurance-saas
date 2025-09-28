from django.urls import path
from . import views

urlpatterns = [
    path('policy/<int:policy_id>/claims/',view=views.ListCreateClaim.as_view()),
    path('policy/<int:policy_id>/claims/<int:claim_id>/',view=views.GetEditDeleteClaim.as_view()),

    path('claims/<int:claim_id>/assign/',view=views.assign_claim),
    path('claims/<int:claim_id>/update-status/',view=views.update_claim_status),

    path('claims/<int:claim_id>/add-note/',view=views.add_note),
    path('notes/<int:note_id>/',view=views.NoteDetails.as_view()),

    path('claims/<int:claim_id>/add-document/',view=views.add_document),
    path('documents/<int:document_id>/',view=views.documentDetails.as_view()),
]