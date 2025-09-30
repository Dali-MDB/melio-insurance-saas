from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ReportSerializer
from .models import Report
from django.shortcuts import get_object_or_404
# Create your views here.



class ListCreateReport(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


    def perform_create(self, serializer):
        serializer.save(
            tenant = self.request.tenant,
            created_by = self.request.user,
        )


class GetUpdateDeleteReport(RetrieveUpdateDestroyAPIView):
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




