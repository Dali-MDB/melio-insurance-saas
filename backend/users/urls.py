from django.urls import path
from . import views
from . import views_auth
urlpatterns = [
    path('',view=views_auth.test),
    path('add-user/',view=views_auth.add_user),
    path('login/',view=views_auth.login),

    path('<str:user_id>/claims/',view=views.get_user_assigned_claims),
    
]