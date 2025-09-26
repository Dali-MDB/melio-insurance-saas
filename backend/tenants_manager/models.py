from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

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
