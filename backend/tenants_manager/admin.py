from django.contrib import admin
from .models import InsuranceCompany,Admin,RegistrationRequest

# Register your models here.
admin.site.register(InsuranceCompany)
admin.site.register(Admin)
admin.site.register(RegistrationRequest)