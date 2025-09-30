from django.db import models
from tenants_manager.models import InsuranceCompany
from users.models import User

# Create your models here.
class Report(models.Model):
    tenant = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=50, choices=[
        ('claims_overview', 'Claims Overview'),
        ('financial_summary', 'Financial Summary'),
        ('adjuster_performance', 'Adjuster Performance'),
        ('policy_type_analysis', 'Policy Type Analysis'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Store filter criteria used to generate the report
    filters = models.JSONField(default=dict)
    
    # Store the generated report data
    report_data = models.JSONField(default=dict)