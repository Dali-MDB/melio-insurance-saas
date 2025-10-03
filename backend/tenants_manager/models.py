from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .admin_manager import AdminManager


# Create your models here.
class InsuranceCompany(TenantMixin):
    # Basic Identification
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True) 
    logo = models.ImageField(upload_to='logos',null=True,blank=True)
    
    # Company Details
    business_type = models.CharField(max_length=50, choices=[
        ('auto', 'Auto Insurance'),
        ('health', 'Health Insurance'), 
        ('property', 'Property Insurance'),
        ('life', 'Life Insurance'),
        ('multi_line', 'Multi-Line Insurance')
    ])
    
    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    linkedin = models.CharField(max_length=150,null=True,blank=True)
    address = models.TextField(blank=True)
    
    # Operational Settings (Configurable per tenant)
    # auto_assign_claims = models.BooleanField(default=False)
    # max_claim_amount = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00)
    default_currency = models.CharField(max_length=3, default='USD')
    
    # Metadata
    created_on = models.DateField(auto_now_add=True)
    subscription_plan = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('pro','Pro')
    ], default='basic')
    
   
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass




class RegistrationRequest(models.Model):
    # === COMPANY INFORMATION (from InsuranceCompany) ===
    company_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=InsuranceCompany._meta.get_field('business_type').choices)
    company_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    company_address = models.TextField()
    company_linkedin = models.CharField(max_length=150, blank=True, null=True)
    default_currency = models.CharField(max_length=3, default='USD')
    subscription_plan = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('pro', 'Pro')
    ], default='basic')
    requested_domain = models.CharField(max_length=100)
    
    # === ADMIN USER INFORMATION (from User) ===
    admin_email = models.EmailField()  # Will become username & email
    admin_phone = models.CharField(max_length=15)
    admin_first_name = models.CharField(max_length=30)
    admin_last_name = models.CharField(max_length=30)
    admin_username = models.CharField(max_length=30)  # Explicit username
    admin_password = models.CharField(max_length=128)


    def __str__(self):
        return f"request:{self.company_name}"
    



class Admin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # so they can log into admin site

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="platform_admins", 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="platform_admins_permissions",  
        blank=True,
    )

    def __str__(self):
        return self.email