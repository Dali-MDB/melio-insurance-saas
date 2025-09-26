from django.db import models
import uuid
from tenants_manager.models import InsuranceCompany
from users.models import User
from policies.models import Policy

# Create your models here.
class Claim(models.Model):
    claim_number = models.CharField(max_length=50, unique=True)  # Auto-generated
    tenant = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    # Realistic status flow
    status = models.CharField(max_length=20, choices=[
        ('reported', 'Reported'),
        ('assigned', 'Assigned'),
        ('investigation', 'Investigation'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('paid', 'Paid')
    ], default='reported')
    
    # Financials
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    incident_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)