from dataclasses import field, fields
from datetime import datetime, date, time
from webbrowser import get
from django.forms import Field, fields_for_model
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, View
from django.shortcuts import render

from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML, CSS
from config import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.db import transaction
from django.db.models import Q

from core.erp.mixin import ValidatePermissionRequiredMixin

from core.erp.models import PagoReserva, Estacionamiento, Cliente, Reserva, Tarifa, Plan, TarifaPlan
from core.erp.forms import ReservaForm, ClienteForm, PagoReservaForm, PlanForm

###############################   RESERVA ##################################


class RecepcionView(LoginRequiredMixin, TemplateView):
    template_name = 'recepcion/reserva/recepcion.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == 'estacionamiento_libre':
                id = request.POST['id']
                estacionamiento = Estacionamiento.objects.get(id=id)
                estacionamiento.estado_estacionamiento = "disponible"
                estacionamiento.save()
                plan = Plan.objects.get(
                    estacionamiento_id=id, estado_plan='iniciado')
                plan.estado_plan = 'terminado'
                plan.save()
            if action == 'create_reserva':
                frmReserva = ReservaForm(request.POST)
                data = frmReserva.save()
                print(data)
            elif action == 'actualizar':
                estacionamiento = [i.toJSON() for i in Estacionamiento.objects.all().order_by(
                    "numero_estacionamiento")]
                reserva = [i.toJSON() for i in Reserva.objects.filter(
                    Q(estado_reserva='entrada') | Q(estado_reserva='pago pendiente'))]
                plan = [i.toJSON()
                        for i in Plan.objects.filter(estado_plan='iniciado')]
                data = {'estacionamiento': estacionamiento,
                        'reserva': reserva, 'plan': plan}
            elif action == 'search_reserva':
                id = request.POST['id']
                reserva = Reserva.objects.get(Q(estacionamiento_id=id, estado_reserva='entrada') | Q(
                    estacionamiento_id=id, estado_reserva='pago pendiente'))
                data = {'reserva': reserva.estado_reserva}
            elif action == 'search_reserva_plan':
                id = request.POST['id']
                plan = Plan.objects.get(
                    estacionamiento_id=id, estado_plan='iniciado')
                data = plan.toJSON()
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Panel de Entrada"
        context['entity'] = "Entrada"
        context['icon'] = "fas fa-sign-in-alt"
        context['frmReservaDiaria'] = ReservaForm()
        context['costo_tarifas'] = Tarifa.objects.all()
        return context


class SalidaView(LoginRequiredMixin, TemplateView):
    template_name = 'recepcion/reserva/salida.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == 'create_pago':
                id = request.POST['id']
                print(id)
                reserva = Reserva.objects.filter(id=id)
                reserva.update(fecha_salida=date.today())
                reserva.update(hora_salida=datetime.now())
                reserva = reserva.first()
                data = reserva.toJSON()
            elif action == 'guardar_pago':
                pago = PagoReservaForm(request.POST)
                data = pago.save()
            elif action == 'actualizar':
                # context = {
                #     'reservas': [i.toJSON() for i in  Reserva.objects.all().order_by("estacionamiento")]
                # }
                # return render(request, 'recepcion/reserva/salida_htmx.html', context)
                # data = [i.toJSON()
                #         for i in Reserva.objects.all().order_by("estacionamiento")]
                data = [i.toJSON()
                        for i in Reserva.objects.filter(estacionamiento__estado_estacionamiento="ocupado", estado_reserva="entrada").order_by("estacionamiento")]
            elif action == 'anular_salida':
                id = request.POST['reserva']
                reserva = Reserva.objects.filter(id=id)
                reserva.update(estado_reserva='pago pendiente')
                pago = PagoReservaForm(request.POST)
                data = pago.save()
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Panel de Salida"
        context['entity'] = "Salida"
        context['icon'] = "fas fa-sign-out-alt"
        # context['reservas'] = [i.toJSON() for i in  Reserva.objects.all().order_by("estacionamiento")]
        context['frmSalida'] = PagoReservaForm()
        context['action'] = 'actualizar'
        return context


# class ReservaCreateView(LoginRequiredMixin, CreateView):
#     model = Reserva
#     form_class = ReservaForm
#     template_name = "recepcion/reserva/create.html"
#     success_url = reverse_lazy('erp:recepcion')

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST["action"]
#             if action == 'add':
#                 form = self.get_form()
#                 data = form.save()
#             elif action == "search_cliente":
#                 data = []
#                 term = request.POST['term']
#                 clientes = Cliente.objects.filter(Q(nombre__icontains=term) | Q(
#                     apellido__icontains=term) | Q(rut__icontains=term))[0:10]
#                 for i in clientes:
#                     item = i.toJSON()
#                     item['text'] = i.get_full_name()
#                     data.append(item)
#             elif action == "create_cliente":
#                 with transaction.atomic():
#                     frmCliente = ClienteForm(request.POST)
#                     data = frmCliente.save()
#             elif action == 'complete':
#                 data = Estacionamiento.objects.get(
#                     id=self.kwargs['pk']).toJSON()
#             else:
#                 data["error"] = "No ha ingresado a ninguna opcion"
#         except Exception as e:
#             data["error"] = str(e)
#         return JsonResponse(data, safe=False)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Registro de Reserva"
#         context['entity'] = "Reservas"
#         context['icon'] = "fas fa-book"
#         context['list_url'] = reverse_lazy('erp:recepcion')
#         context['action'] = "add"
#         context['estacionamiento'] = Estacionamiento.objects.get(
#             id=self.kwargs['pk'])
#         context['frmCliente'] = ClienteForm()
#         return context


class IngresoInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('recepcion/reserva/invoice_ingreso.html')
            context = {
                'reserva': Reserva.objects.get(pk=self.kwargs['pk']),
                # 'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                # 'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-5.1.3-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:recepcion'))


class SalidaInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('recepcion/reserva/invoice_salida.html')
            context = {
                'pago': PagoReserva.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-5.1.3-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:salida'))


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "recepcion/reserva/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'reserva_delete':
                id = request.POST["id"]
                reserva = Reserva.objects.get(id=id)
                reserva.state = False
                reserva.save()
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Reservas"
        context['entity'] = "Reservas"
        context['icon'] = "fas fa-book"
        context['list_url'] = reverse_lazy('erp:reserva_list')
        context['form'] = ReservaForm()
        return context


class PlanReservaCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = "recepcion/reserva/create_plan.html"
    success_url = reverse_lazy('erp:plan_reserva_list')

    # def get_form(self):
    #     data = {
    #         'estacionamiento': Estacionamiento.objects.get(id=self.kwargs['pk']),
    #     }
    #     form = self.form_class(initial=data)
    #     return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == 'add':
                print('estoy aqui')
                form = self.get_form()
                data = form.save()
                print(data)
            elif action == "search_cliente":
                data = []
                term = request.POST['term']
                clientes = Cliente.objects.filter(Q(nombre__icontains=term) | Q(
                    apellido__icontains=term) | Q(rut__icontains=term))[0:10]
                for i in clientes:
                    item = i.toJSON()
                    item['text'] = i.get_full_name
                    data.append(item)
            elif action == "create_cliente":
                with transaction.atomic():
                    print(request.POST)
                    frmCliente = ClienteForm(request.POST)
                    data = frmCliente.save()
                    print(data)
            elif action == 'calcular_total':
                print(request.POST)
                id = request.POST['id']
                data = TarifaPlan.objects.get(id=id).toJSON()
            else:
                data["error"] = "No ha ingresado a ninguna opcion"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion Plan de Reserva"
        context['entity'] = "Plan de Reserva"
        context['icon'] = "fas fa-book"
        context['list_url'] = self.success_url
        context['action'] = "add"
        # print(context['form_class'])
        context['form'].fields['estacionamiento'].initial = Estacionamiento.objects.get(
            id=self.kwargs['pk'])
        context['frmCliente'] = ClienteForm()
        return context


class PlanReservaListView(LoginRequiredMixin, ListView):
    model = Plan
    template_name = "recepcion/reserva/list_plan.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'reserva_delete':
                id = request.POST["id"]
                reserva = Reserva.objects.get(id=id)
                reserva.state = False
                reserva.save()
            elif action == 'terminar_plan':
                id = request.POST['id']
                plan = Plan.objects.get(id=id)
                plan.estado_plan = 'terminado'
                plan.save()
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado Planes de Reservas"
        context['entity'] = "planes"
        context['icon'] = "fas fa-book"
        context['list_url'] = reverse_lazy('erp:plan_reserva_list')
        context['formPlan'] = ClienteForm()
        return context


class PlanIniciadoInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(
                'recepcion/reserva/invoice_plan_iniciado.html')
            context = {
                'plan': Plan.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-5.1.3-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:salida'))


class PlanTerminadoInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(
                'recepcion/reserva/invoice_plan_terminado.html')
            context = {
                'plan': Plan.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-5.1.3-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:salida'))
