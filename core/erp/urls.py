
from django.urls import path
from core.erp.views.contacto.views import ContactoDeleteView, ContactoListView

# cliente
from core.erp.views.pago.views import *
from core.erp.views.infcliente.views import *
# admin
from core.erp.views.empresa.views import *
from core.erp.views.funcionario.views import *
from core.erp.views.contrato.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.accidente.views import *
# funcionario
from core.erp.views.capacitacion.views import *
from core.erp.views.visita.views import *
from core.erp.views.caso.views import *
from core.erp.views.asesoria.views import *
from core.erp.views.asesoriaespecial.views import *
from core.erp.views.checklist.views import *
# from core.erp.views.resultadovisita.views import *

app_name = 'erp'

urlpatterns = [
    ######################################## NEW APP ##################################
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Empresa
    path('empresa/list/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/add/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/update/<int:pk>/',
         EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/delete/<int:pk>/',
         EmpresaDeleteView.as_view(), name='empresa_delete'),
    path('empresa/invoice/pdf/<int:pk>/', EmpresaInvoicePdfView.as_view(),
         name='empresa_invoice_pdf'),
    path('empresa/dashboard/<int:pk>/',
         EmpresaDashboardView.as_view(), name='empresa_dashboard'),
     path('empresa/dashboard/<int:pk>/grafico_invoice.html', EmpresaDashboardPrintView.as_view(),
         name='empresa_dashboard_print'),
    path('empresa/grafico/invoice/pdf/<int:pk>/', GraficoInvoicePdfView.as_view(),
         name='empresa_grafico_invoice_pdf'),
    path('empresa/factura/<int:pk>/', FacturaView.as_view(),
         name='empresa_factura'),
    #     path('empresa/factura/<int:pk>/factura-print.html', EmpresaFacturaPrintView.as_view(),
    #          name='empresa_factura_print'),

    # Pago
    path('pago/list/', PagoListView.as_view(), name='pago_list'),
    path('pago/add/', PagoCreateView.as_view(), name='pago_create'),
    path('pago/update/<int:pk>/',
         PagoUpdateView.as_view(), name='pago_update'),
    path('pago/delete/<int:pk>/',
         PagoDeleteView.as_view(), name='pago_delete'),

    # Funcionario
    path('funcionario/list/', FuncionarioListView.as_view(),
         name='funcionario_list'),
    path('funcionario/add/', FuncionarioCreateView.as_view(),
         name='funcionario_create'),
    path('funcionario/update/<int:pk>/',
         FuncionarioUpdateView.as_view(), name='funcionario_update'),
    path('funcionario/delete/<int:pk>/',
         FuncionarioDeleteView.as_view(), name='funcionario_delete'),
    path('funcionario/dashboard/<int:pk>/',
         FuncionarioDashboardView.as_view(), name='funcionario_dashboard'),

    # Contrato
    path('contrato/list/', ContratoListView.as_view(), name='contrato_list'),
    path('contrato/add/', ContratoCreateView.as_view(), name='contrato_create'),
    path('contrato/update/<int:pk>/',
         ContratoUpdateView.as_view(), name='contrato_update'),
    path('contrato/delete/<int:pk>/',
         ContratoDeleteView.as_view(), name='contrato_delete'),
    path('contrato/invoice/pdf/<int:pk>/',
         ContratoInvoicePdfView.as_view(), name='contrato_invoice_pdf'),

    # CheckList
    path('checklist/list/', CheckListView.as_view(), name='checklist_list'),
    path('checklist/add/', CheckListCreateView.as_view(), name='checklist_create'),
    path('checklist/update/<int:pk>/',
         CheckListUpdateView.as_view(), name='checklist_update'),
    path('checklist/delete/<int:pk>/',
         CheckListDeleteView.as_view(), name='checklist_delete'),
    path('checklist/invoice/pdf/<int:pk>/',
         CheckListInvoicePdfView.as_view(), name='checklist_invoice_pdf'),
    path('checklist/todolist/<int:pk>/',
         TodoListView.as_view(), name='checklist_todolist_pdf'),


    # Capacitacion
    path('capacitacion/list/', CapacitacionListView.as_view(),
         name='capacitacion_list'),
    path('capacitacion/add/', CapacitacionCreateView.as_view(),
         name='capacitacion_create'),
    path('capacitacion/update/<int:pk>/',
         CapacitacionUpdateView.as_view(), name='capacitacion_update'),
    path('capacitacion/delete/<int:pk>/',
         CapacitacionDeleteView.as_view(), name='capacitacion_delete'),

    # Visita
    path('visita/list/', VisitaListView.as_view(),
         name='visita_list'),
    path('visita/add/', VisitaCreateView.as_view(),
         name='visita_create'),
    path('visita/update/<int:pk>/',
         VisitaUpdateView.as_view(), name='visita_update'),
    path('visita/delete/<int:pk>/',
         VisitaDeleteView.as_view(), name='visita_delete'),

    # Asesoria
    path('asesoria/list/', AsesoriaListView.as_view(),
         name='asesoria_list'),
    path('asesoria/add/', AsesoriaCreateView.as_view(),
         name='asesoria_create'),
    path('asesoria/update/<int:pk>/',
         AsesoriaUpdateView.as_view(), name='asesoria_update'),
    path('asesoria/delete/<int:pk>/',
         AsesoriaDeleteView.as_view(), name='asesoria_delete'),

    # Asesoria Especial
    path('asesoriaespecial/list/', AsesoriaEspecialListView.as_view(),
         name='asesoriaespecial_list'),
    path('asesoriaespecial/add/', AsesoriaEspecialCreateView.as_view(),
         name='asesoriaespecial_create'),
    path('asesoriaespecial/update/<int:pk>/',
         AsesoriaEspecialUpdateView.as_view(), name='asesoriaespecial_update'),
    path('asesoriaespecial/delete/<int:pk>/',
         AsesoriaEspecialDeleteView.as_view(), name='asesoriaespecial_delete'),

    # Caso
    path('caso/list/', CasoListView.as_view(), name='caso_list'),
    path('caso/add/', CasoCreateView.as_view(), name='caso_create'),
    path('caso/update/<int:pk>/',
         CasoUpdateView.as_view(), name='caso_update'),
    path('caso/delete/<int:pk>/',
         CasoDeleteView.as_view(), name='caso_delete'),

    # ------------------------------------------------
    # Infcliente
    path('infcliente/capacitacion/list/', InfCapacitacionListView.as_view(),
         name='infcliente_capacitacion_list'),
    path('infcliente/visita/list/', InfVisitaListView.as_view(),
         name='infcliente_visita_list'),
    path('infcliente/resultadovisita/list/', InfResultadoVisitaListView.as_view(),
         name='infcliente_resultadovisita_list'),
    path('infcliente/asesoria/list/', InfAsesoriaListView.as_view(),
         name='infcliente_asesoria_list'),
    path('infcliente/asesoriaespecial/list/', InfAsesoriaEspecialListView.as_view(),
         name='infcliente_asesoriaespecial_list'),
    path('infcliente/caso/list/', InfCasoListView.as_view(),
         name='infcliente_caso_list'),
    path('infcliente/pago/list/', InfPagoListView.as_view(),
         name='infcliente_pago_list'),
    path('infcliente/contrato/list/', InfContratoListView.as_view(),
         name='infcliente_contrato_list'),
    # invoices
    path('infcapacitacion/invoice/pdf/<int:pk>/', InfCapacitacionInvoicePdfView.as_view(),
         name='infcliente_capacitacion_invoice_pdf'),
    path('infvisita/invoice/pdf/<int:pk>/', InfVisitaInvoicePdfView.as_view(),
         name='infcliente_visita_invoice_pdf'),
    path('infresultadovisita/invoice/pdf/<int:pk>/', InfResultadoVisitaInvoicePdfView.as_view(),
         name='infcliente_resultadovisita_invoice_pdf'),
    path('infasesoria/invoice/pdf/<int:pk>/', InfAsesoriaInvoicePdfView.as_view(),
         name='infcliente_asesoria_invoice_pdf'),
    path('infasesoriaespecial/invoice/pdf/<int:pk>/', InfAsesoriaEspecialInvoicePdfView.as_view(),
         name='infcliente_asesoriaespecial_invoice_pdf'),
    path('infcaso/invoice/pdf/<int:pk>/', InfCasoInvoicePdfView.as_view(),
         name='infcliente_caso_invoice_pdf'),
    path('infpago/invoice/pdf/<int:pk>/', InfPagoInvoicePdfView.as_view(),
         name='infcliente_pago_invoice_pdf'),
    path('infcontrato/invoice/pdf/<int:pk>/', InfContratoInvoicePdfView.as_view(),
         name='infcliente_contrato_invoice_pdf'),
    # detalle
    path('detalle/capacitacion/<int:pk>/', DetalleCapacitacionView.as_view(),
         name='detalle_capacitacion'),
    # -----------------------------------------------


    # accidente
    path('accidente/list/', AccidenteListView.as_view(),
         name='accidente_list'),
    path('accidente/add/', AccidenteCreateView.as_view(),
         name='accidente_create'),
    path('accidente/update/<int:pk>/',
         AccidenteUpdateView.as_view(), name='accidente_update'),
    path('accidente/delete/<int:pk>/',
         AccidenteDeleteView.as_view(), name='accidente_delete'),
    
    
    # contacto
    path('contacto/list/', ContactoListView.as_view(),
         name='contacto_list'),
    path('contacto/delete/<int:pk>/',
         ContactoDeleteView.as_view(), name='contacto_delete'),

]
