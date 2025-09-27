from django.urls import path
from . import views

urlpatterns = [
    path('policy/<int:policy_id>/claims/',view=views.ListCreateClaim.as_view()),
    path('policy/<int:policy_id>/claims/<int:claim_id>/',view=views.GetEditDeleteClaim.as_view()),
]