from django.urls import path

from .views import *

app_name = 'reports'

urlpatterns = [
    path('pago/', ReportPagoView.as_view(), name='pago_report'),
]
