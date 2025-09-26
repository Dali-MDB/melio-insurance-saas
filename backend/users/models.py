from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from tenants_manager.models import InsuranceCompany
from django.utils.translation import gettext_lazy as _
# Create your models here.

import uuid
class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)  # Explicitly define username
    phone_number = models.CharField(max_length=15, unique=True)
    is_admin = models.BooleanField(default=False)
    ROLE_CHOICES = [
        ('call_center', 'Call Center Agent'),
        ('adjuster', 'Claims Adjuster'),
        ('senior_adjuster', 'Senior Adjuster'),
        ('manager', 'Claims Manager'),
        ('admin', 'Tenant Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    tenant = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE,null=True,blank=True)
   
    SCOPE_CHOICES = [
        ("global", "Global"),
        ("tenant", "Tenant"),
    ]
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default="tenant")  #specify general users for managing the app

    objects = UserManager()
    USERNAME_FIELD = "email"  # Authenticate using email
    REQUIRED_FIELDS = ["username", "phone_number"]  # Only these are required when creating a user

    def __str__(self):
        return f'{self.username}-{self.email}'
