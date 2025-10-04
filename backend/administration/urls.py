from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('registration-requests/', views.get_registration_requests, name='get_registration_requests'),
    path('registration-requests/<int:request_id>/approve/', views.approve_registration_request, name='approve_registration_request'),
    path('registration-requests/<int:request_id>/reject/', views.reject_registration_request, name='reject_registration_request'),


    path('add-global-admin/', views.add_global_admin, name='add_global_admin'),
]