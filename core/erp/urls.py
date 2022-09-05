from django.urls import path

from core.erp.views.dashboard.views import DashboardView
from core.erp.views.index.views import IndexView

from core.erp.views.estacionamiento.views import *
from core.erp.views.tarifa.views import *
from core.erp.views.cliente.views import *
from core.erp.views.recepcion.views import *
from core.erp.views.pago.views import *
from core.erp.views.plan.views import *

app_name = "erp"

urlpatterns = [
    # home
    path('', IndexView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    ########################## MANTENIMIENTO ##############################
    # estacionamiento
    path('estacionamiento/list/', EstacionamientoListView.as_view(), name='estacionamiento_list'),
    path('estacionamiento/add/', EstacionamientoCreateView.as_view(), name='estacionamiento_create'),
    path('estacionamiento/update/<int:pk>/', EstacionamientoUpdateView.as_view(), name='estacionamiento_update'),
    path('estacionamiento/delete/<int:pk>/', EstacionamientoDeleteView.as_view(), name='estacionamiento_delete'),
    # tarifa
    path('tarifa/list/', TarifaListView.as_view(), name='tarifa_list'),
    path('tarifa/add/', TarifaCreateView.as_view(), name='tarifa_create'),
    path('tarifa/update/<int:pk>/', TarifaUpdateView.as_view(), name='tarifa_update'),
    path('tarifa/delete/<int:pk>/', TarifaDeleteView.as_view(), name='tarifa_delete'),
    # tarifa
    path('cliente/list/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/update/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/delete/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),
    # plan
    path('tarifa_plan/list/', TarifaPlanListView.as_view(), name='tarifa_plan_list'),
    path('tarifa_plan/add/', TarifaPlanCreateView.as_view(), name='tarifa_plan_create'),
    path('tarifa_plan/update/<int:pk>/', TarifaPlanUpdateView.as_view(), name='tarifa_plan_update'),
    path('tarifa_plan/delete/<int:pk>/', TarifaPlanDeleteView.as_view(), name='tarifa_plan_delete'),
    ########################## RESERVAS ##############################
    # reception y salida
    path('recepcion/', RecepcionView.as_view(), name='recepcion'),
    path('salida/', SalidaView.as_view(), name='salida'),
    # path('reserva/add/<int:pk>/', ReservaCreateView.as_view(), name='reserva_create'),
    path('reserva/list/', ReservaListView.as_view(), name='reserva_list'), # lsitado diario
    path('reserva/invoice_ingreso/pdf/<int:pk>/', IngresoInvoicePdfView.as_view(), name='ingreso_invoice_pdf'),
    path('reserva/invoice_salida/pdf/<int:pk>/', SalidaInvoicePdfView.as_view(), name='salida_invoice_pdf'),

    ########################## PAGO RESERVA ##############################
    # plan reserva
    path('plan/reserva/add/<int:pk>/', PlanReservaCreateView.as_view(), name='plan_reserva_create'),
    path('plan/reserva/list/', PlanReservaListView.as_view(), name='plan_reserva_list'),
    path('plan/invoice_iniciado/pdf/<int:pk>/', PlanIniciadoInvoicePdfView.as_view(), name='plan_iniciado_invoice_pdf'),
    path('plan/invoice_terminado/pdf/<int:pk>/', PlanTerminadoInvoicePdfView.as_view(), name='plan_terminado_invoice_pdf'),
    ########################## PAGO RESERVA ##############################
    # pago reserva
    path('reserva/pago/list/', PagoReservaListView.as_view(), name='pago_reserva_list'),
    # path('guest/add/', GuestCreateView.as_view(), name='guest_create'),
    # path('reserva/pago/update/<int:pk>/', PagoReservaUpdateView.as_view(), name='pago_reserva_update'),
    # path('reserva/pago/delete/<int:pk>/', PagoReservaDeleteView.as_view(), name='pago_reserva_delete'),

    # pensando...........
    # path('reserva/list/', ReservaNoseListView.as_view(), name='reserva_list'),
    # path('reserva/retrieve/<int:pk>/', InfoReservaView.as_view(), name='reserva_retrieve'),
    # path('reserva/add/<int:pk>/', ReservaCreateView.as_view(), name='reserva_create'),
    # path('reserva/update/<int:pk>/', ReservaUpdateView.as_view(), name='reserva_update'),
    # path('reserva/delete/<int:pk>/', ReservaDeleteView.as_view(), name='reserva_delete'),


]
