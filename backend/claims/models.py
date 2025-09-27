from django.db import models
import uuid
from tenants_manager.models import InsuranceCompany
from users.models import User
from policies.models import Policy
from users.models import User
import os

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


    def __str__(self):
        return f'claim: {self.claim_number} - {self.incident_date}'




class ClaimNote(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    is_internal = models.BooleanField(default=True)  # Internal note vs customer-facing
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'claim-note: {self.claim.claim_number} - {self.created_at}'

def get_file_name(instance,filename):
    return os.path.join('claim_documents',str(instance.claim.claim_number),filename)

class ClaimDocument(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=[
        ('police_report', 'Police Report'),
        ('estimate', 'Repair Estimate'),
        ('photo', 'Photo'),
        ('medical_bill', 'Medical Bill'),
        ('invoice', 'Invoice'),
        ('other', 'Other')
    ])
    file = models.FileField(upload_to=get_file_name)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def delete(self, *args, **kwargs):
        # delete file from storage before deleting the record
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


    def __str__(self):
        return f'claim-note: {self.claim.claim_number} - {self.uploaded_at}'