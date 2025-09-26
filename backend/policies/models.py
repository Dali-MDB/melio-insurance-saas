from django.db import models
from tenants_manager.models import InsuranceCompany
from django.utils import timezone

# Create your models here.
class Policy(models.Model):
    policy_number = models.CharField(max_length=50, unique=True)
    tenant = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    policyholder_name = models.CharField(max_length=100)
    policyholder_email = models.EmailField()

    POLICY_TYPE_CHOICES = [
        ('auto', 'Auto'),
        ('home', 'Home'),
        ('life', 'Life'),
        ('health', 'Health'),
        ('business', 'Business'),
        ('travel', 'Travel'),
        ('other', 'Other')
    ]
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPE_CHOICES)
    
    # Financial basics
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Dates only
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


    @property
    def is_valid(self):
        return self.start_date <= timezone.now().date() <= self.end_date and self.is_active

    def __str__(self):
        return f'policy: {self.policy_number} - {self.policyholder_email}' 