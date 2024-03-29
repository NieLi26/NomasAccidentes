from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.forms import PagoReservaForm
from core.erp.models import Estacionamiento, PagoReserva, Reserva


class PagoReservaListView(LoginRequiredMixin, ListView):
    model = PagoReserva
    template_name = 'pago/reserva/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'revisar_pago':
                id = request.POST['id']
                pago = PagoReserva.objects.get(id=id)
                reserva = Reserva.objects.get(id=pago.reserva_id)
                reserva.estado_reserva='reserva anulada'
                reserva.save()
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Pagos"
        context['entity'] = "Pagos de Reservas"
        context['icon'] = "fas fa-hand-holding-usd"
        # context['create_url'] = reverse_lazy('erp:room_create')
        context['list_url'] = reverse_lazy('erp:pago_reserva_list')
        context['form'] = PagoReservaForm()
        return context


# class RoomCreateView(CreateView):
#     model = Room
#     form_class = RoomForm
#     template_name = "rooms/room/create.html"
#     success_url = reverse_lazy('erp:room_list')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST["action"]
#             if action == "add":
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data["error"] = "No ha ingresado a ninguna opcion"
#         except Exception as e:
#             data["error"] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Creacion de una Habitacion"
#         context['entity'] = "Habitaciones"
#         context['list_url'] = reverse_lazy('erp:room_list')
#         context['action'] = "add"
#         return context


# class PagoReservaUpdateView(UpdateView):
#     model = PagoReserva
#     form_class = PagoReservaForm
#     template_name = "recepcion/pago.html"
#     success_url = reverse_lazy('erp:pago_reserva_list')

#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST["action"]
#             if action == "edit":
#                 form = self.get_form()
#                 data = form.save()
#             elif action == 'complete':
#                 data = Reserva.objects.get(id=self.object.reserva.id).toJSON()
#             else:
#                 data["error"] = "No ha ingresado a ninguna opcion"
#         except Exception as e:
#             data["error"] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Pago de Reserva"
#         context['entity'] = "Habitaciones"
#         context['icon'] = "fas fa-hand-holding-usd"
#         context['list_url'] = self.success_url
#         context['action'] = "edit"
#         context['reserva'] = Reserva.objects.get(id=self.object.reserva.id)
#         return context


# class PagoReservaDeleteView(DeleteView):
#     model = PagoReserva
#     template_name = "pago/reserva/delete.html"
#     success_url = reverse_lazy('erp:pago_reserva_list')

#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             self.object.delete()
#         except Exception as e:
#             data["error"] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Eliminacion de pago de una reserva"
#         context['entity'] = "Pagos Reserva"
#         context['icon'] = "fas fa-hand-holding-usd"
#         context['list_url'] = self.success_url
#         return context
