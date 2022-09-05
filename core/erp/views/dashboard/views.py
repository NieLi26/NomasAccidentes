from datetime import datetime
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import Reserva, PagoReserva, Plan
from core.erp.forms import DashboardForm


class DashboardView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = "view_user"
    template_name = 'dashboard.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                terminada = Reserva.objects.filter(estado_reserva='reserva terminada')
                anulada = Reserva.objects.filter(estado_reserva='reserva anulada')
                if len(start_date) and len(end_date):
                    terminada = terminada.filter(fecha_salida__range=[
                                           start_date, end_date])
                    anulada = anulada.filter(fecha_salida__range=[
                        start_date, end_date])
                    de = []
                    de = {'name': 'Reserva Terminada', 'y': terminada.count(), 'color': 'green'}, {'name': 'reserva anulada', 'y': anulada.count(), 'color': 'black'}
                    data = {'name':'Reservas', 'data': de}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_reservas_mensual(self):
        data = []
        m = datetime.now().month
        try:
            # uno = Reserva.objects.filter(estado_reserva='alojamiento terminado').count()
            # dos = Reserva.objects.filter(estado_reserva='cancelada').count()
            # tres = Reserva.objects.filter(estado_reserva='no ingreso').count()
            # cuatro = Reserva.objects.filter(estado_reserva='confirmada').count()
            # cinco = Reserva.objects.filter(estado_reserva='sin confirmar').count()
            # data.append({'name': 'alojamiento terminado', 'y': uno, 'color': 'green'})
            # data.append({'name': 'cancelada', 'y': dos, 'color': 'dark'})
            # data.append({'name': 'no ingreso', 'y': tres, 'color': 'blue'})
            # data.append({'name': 'confirmada', 'y': cuatro, 'color': 'red'})
            # data.append({'name': 'sin confirmar', 'y': cinco, 'color': 'yellow'})
            nombres = ['reserva terminada', 'pago pendiente']
            querys = [Reserva.objects.filter(
                estado_reserva=nombre, fecha_entrada__month=m).count() for nombre in nombres]
            colores = ['green', 'yellow']
            data = [{'name': nom, 'y': num, 'color': col}
                    for nom, num, col in zip(nombres, querys, colores)]
        except:
            # except Exception as e:
            pass
        # print(data)
        return data

    def get_pagos_mensual(self):
        data = []
        m = datetime.now().month
        # cancelado = PagoReserva.objects.filter(estado_pago='cancelado', fecha_creacion__month = m).count()
        # nocancelado = PagoReserva.objects.filter(estado_pago='sin cancelar', fecha_creacion__month = m).count()
        valor1 = 0
        valor2 = 0
        cancelado = PagoReserva.objects.filter(
            estado_pago='cancelado', created_date__month=m)
        for can in cancelado:
            valor1 += can.total
        # nocancelado = PagoReserva.objects.filter(
        #     estado_pago='sin cancelar', created_date__month=m)
        # for nocan in nocancelado:
        #     valor2 += nocan.total
        # print(valor1)
        # print(valor2)
        data.append({'name': 'Cancelado', 'y': valor1, 'color': '#00CB03'})
        # data.append({'name': 'Sin cancelar', 'y': valor2, 'color': '#F00505'})
        return data
 
    def get_pago_año(self):
        data = []
     
        year = datetime.now().year
        try:
            for m in range(1, 13):
                cap = PagoReserva.objects.filter(
                    created_date__year=year, created_date__month=m, estado_pago='cancelado')
                plan = Plan.objects.filter(
                    fecha_termino__year=year, fecha_termino__month=m, estado_plan='terminado')
                total = 0
                for i in cap:
                    total += i.total
                for i in plan:
                    total += i.total
                # print(meses[m-1])
                data.append([total])
        except:
            pass
        return data

    def get_reserva_año(self):
        data = []
        ter = []
        pen = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                terminada =  Reserva.objects.filter(
                    fecha_salida__year=year, fecha_salida__month=m, estado_reserva='reserva terminada').count()
                pendiente = Reserva.objects.filter(
                    fecha_salida__year=year, fecha_salida__month=m, estado_reserva='reserva anulada').count()
                ter.append(terminada)
                pen.append(pendiente)
            data.append({'name': 'Reserva Terminada', 'data': ter,'color': 'green'})
            data.append({'name': 'Reserva Anulada', 'data': pen, 'color': 'black'})
            print(data)
        except:
            pass
        return data

    def get_plan_año(self):
        data = []
        ter = []
        ini = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                terminado =  Plan.objects.filter(
                    fecha_termino__year=year, fecha_termino__month=m, estado_plan='terminado').count()
                iniciado = Plan.objects.filter(
                    fecha_inicio__year=year, fecha_inicio__month=m, estado_plan='iniciado').count()
                ter.append(terminado)
                ini.append(iniciado)
            data.append({'name': 'Plan Terminado', 'data': ter,'color': 'green'})
            data.append({'name': 'Plan iniciado', 'data': ini, 'color': 'black'})
            print(data)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = "Panel de adminstrador"
        context['entity'] = "Dashboard"
        context['title'] = "Dashboard"
        context['icon'] = "fas fa-chart-pie"
        context['reservas'] = self.get_reservas_mensual()
        context['pagos'] = self.get_pagos_mensual()
        context['pagos_anuales'] = self.get_pago_año()
        context['reservas_anuales'] = self.get_reserva_año()
        context['planes_anuales'] = self.get_plan_año()
        context['dashboard_form'] = DashboardForm()
        return context
