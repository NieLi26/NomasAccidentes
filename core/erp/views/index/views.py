from datetime import datetime, date
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.models import Reserva, PagoReserva


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_reservas_mensual(self):
        data = []
        m = datetime.now().month
        try:
            nombres = ['reserva terminada', 'confirmada', 'pago pendiente']
            querys = [Reserva.objects.filter(
                estado_reserva=nombre, fecha_entrada__month=m).count() for nombre in nombres]
            colores = ['green', 'blue', 'yellow']
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
        valor1 = 0
        valor2 = 0
        cancelado = PagoReserva.objects.filter(
            estado_pago='cancelado', created_date__month=m)
        for can in cancelado:
            valor1 += can.total
        data.append({'name': 'Cancelado', 'y': valor1, 'color': '#00CB03'})
        return data



    def get_pago_diario(self):
        total = 0
        # forma1
        day = date.today().day
        # print(day)
        try:
            for pago  in [pago.total for pago in PagoReserva.objects.filter(created_date__day=day,estado_pago='cancelado')]:
                total +=pago
        except:
            pass
        return total

    def get_reserva_terminada_diaria(self):
        total = 0
        # forma2
        day = datetime.now().day
        try:
            total = Reserva.objects.filter(fecha_salida__day=day, estado_reserva='reserva terminada').count()
        except:
            pass
        return total

    def get_reserva_pendiente_diaria(self):
        total = 0
        # forma2
        day = datetime.now().day
        try:
            total = Reserva.objects.filter(fecha_salida__day=day, estado_reserva='pago pendiente').count()
        except:
            pass
        return total

    def get_reserva_anulada_diaria(self):
        total = 0
        # forma2
        day = datetime.now().day
        try:
            total = Reserva.objects.filter(fecha_salida__day=day, estado_reserva='reserva anulada').count()
        except:
            pass
        return total

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['entity'] = "Home"
        context['title'] = "Home"
        # context['icon'] = "fas fa-chart-line"
        context['pagos_diarios'] = self.get_pago_diario()
        context['reservas_terminadas_diarias'] = self.get_reserva_terminada_diaria()
        context['reservas_pendientes_diarias'] = self.get_reserva_pendiente_diaria()
        context['reservas_anuladas_diarias'] = self.get_reserva_anulada_diaria()
        return context
