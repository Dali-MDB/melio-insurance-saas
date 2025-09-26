from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('',view=views.ListCreatePolicy.as_view()),
    path('<int:policy_id>/',view=views.GetEditDeletePolicy.as_view()),
]