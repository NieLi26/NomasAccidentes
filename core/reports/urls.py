from django.urls import path

from core.reports.views import *

app_name = 'reports'

urlpatterns = [
    # Report
    path('report/dashboard/empresa',
         DashboardClienteView.as_view(), name='report_dashboard_empresa'),
]
