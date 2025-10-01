from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('admin/registration-requests/', views.get_registration_requests, name='get_registration_requests'),
    path('admin/registration-requests/<int:request_id>/approve/', views.approve_registration_request, name='approve_registration_request'),
    path('admin/registration-requests/<int:request_id>/reject/', views.reject_registration_request, name='reject_registration_request'),
]