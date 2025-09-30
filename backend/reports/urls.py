from django.urls import path
from . import views

urlpatterns = [
    path('',view=views.ListCreateReport.as_view()),    
    path('<int:report_id>',view=views.GetUpdateDeleteReport.as_view()),

]
