from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ReportSerializer
from .models import Report
from django.shortcuts import get_object_or_404
# Create your views here.



class ListCreateReport(ListCreateAPIView):
    """
    List and create insurance reports
    
    Goal: Get all reports or create new insurance report
    Path: GET/POST /reports/
    Authentication: JWT required
    
    Request Body (POST):
    {
        "title": "Monthly Claims Report",
        "description": "Report description",
        "report_type": "monthly|quarterly|annual|custom",
        "date_range_start": "2024-01-01",
        "date_range_end": "2024-01-31"
    }
    
    Response:
    - GET 200: [ReportSerializer objects]
    - POST 201: ReportSerializer object with created_by and tenant auto-assigned
    - POST 400: Validation errors
    """
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


    def perform_create(self, serializer):
        serializer.save(
            tenant = self.request.tenant,
            created_by = self.request.user,
        )


class GetUpdateDeleteReport(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific report
    
    Goal: Get report details, update report info, or delete report
    Path: GET/PUT/PATCH/DELETE /reports/{report_id}/
    Authentication: JWT required
    
    Request Body (PUT/PATCH):
    {
        "title": "Updated Report Title",
        "description": "Updated description",
        "report_type": "updated_type",
        "status": "draft|published|archived"
    }
    
    Response:
    - GET 200: ReportSerializer object
    - PUT/PATCH 200: Updated ReportSerializer object
    - DELETE 204: No content
    - 404: Report not found
    """
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = 'report_id'

    def get_object(self):
        report_id = self.kwargs.get('report_id',None)
        return get_object_or_404(Report,pk=report_id)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)




