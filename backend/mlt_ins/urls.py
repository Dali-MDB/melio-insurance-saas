from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('policies/',include('policies.urls')),
    path('',include('claims.urls')),
    path('reports/',include('reports.urls')),
    path('administration/',include('administration.urls')),

    #public schema urls
    #path('api/',include('tenants_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
