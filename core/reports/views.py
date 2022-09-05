from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import ReportForm 
from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import PagoReserva, Plan

from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.db.models import Q

class ReportPagoView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name= 'pago/reserva/report.html'
    permission_required = "view_user"
    
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_report":
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = PagoReserva.objects.all()
                search2 = Plan.objects.all()
                if len(start_date) and len(end_date): # si tengo valores se siguen con el if
                    search = search.filter(created_date__range=[start_date, end_date], estado_pago='cancelado')
                    search2 = search2.filter(fecha_termino__range=[start_date, end_date], estado_plan='terminado')
                for p in search:
                    data.append([
                        # p.id,
                        p.reserva.patente,
                        p.fecha_entrada.strftime('%Y-%m-%d'),
                        # p.hora_entrada.strftime('%H:%M %p'),
                        p.fecha_salida.strftime('%Y-%m-%d'),
                        # p.hora_salida.strftime('%H:%M %p'),
                        p.total,
                    ])

                for p in search2:
                    data.append([
                        # p.id,
                        p.patente,
                        p.fecha_inicio.strftime('%Y-%m-%d'),
                        # 'sin horario',
                        p.fecha_termino.strftime('%Y-%m-%d'),
                        # 'sin horario',
                        p.total,
                    ])

                # subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                # iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                total2 = search2.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                totalFinal = total + total2

                data.append([
                    # '---',
                    '---',
                    '---',
                    # '---',
                    '---',
                    # '---',
                    totalFinal,
                ])
            else:
                data["error"] = "Ha ocurrido un error"  
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Reporte de los Pagos'
        context['entity'] = 'Reportes'
        context['icon'] = "fas fa-chart-bar"
        context['list_url'] = reverse_lazy('reports:pago_report')
        context['form'] = ReportForm()
        return context