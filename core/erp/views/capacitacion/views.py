from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import datetime, timedelta, date


from core.erp.forms import CapacitacionForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Capacitacion

from django.db.models.signals import post_save
from django.core.signals import request_finished, request_started
from notifications.signals import notify
from config import settings
from django.contrib.auth import get_user_model
from core.erp.tasks import *


User = get_user_model()

class CapacitacionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Capacitacion
    template_name = 'capacitacion/list.html'
    permission_required = 'view_capacitacion', 'change_capacitacion', 'delete_capacitacion', 'add_capacitacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Capacitacion.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Capacitaciones'
        context['create_url'] = reverse_lazy('erp:capacitacion_create')
        context['list_url'] = reverse_lazy('erp:capacitacion_list')
        context['entity'] = 'Capacitaciones'
        context['form'] = CapacitacionForm()
        return context


class CapacitacionCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Capacitacion
    form_class = CapacitacionForm
    template_name = 'capacitacion/create.html'
    success_url = reverse_lazy('erp:capacitacion_list')
    permission_required = 'add_capacitacion'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    
        
    ########## TEST ################
    # def my_capacitacion_job():
    #     data = []
    #     try:
    #         for i in Capacitacion.objects.all():
    #             d = i.fecha_realizacion - timedelta(days=15)
    #             if d == datetime.now():
    #                 data.append(d)
    #     except:
    #         pass
    #     return print(data)

    # def my_notify_capacitacion(sender, instance, created, raw, **kwargs):
    #     if created:
    #         for i in Capacitacion.objects.all():
    #             po = i.fecha_realizacion
    #             po = po - timedelta(15)
    #             if po == date.today():
    #                 users = User.objects.filter(id=i.cli.user.id)
    #                 # users = User.objects.all()
    #                 print(users)
    #                 notify.send(instance, recipient=users,
    #                         verb='Alerta Capacitacion', description='Se genero una alerta de capacitacion', soft_delete=True)

    # post_save.connect(my_notify_capacitacion, sender=Capacitacion)
    
    ########## TEST #################

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Capacitacion'
        context['entity'] = 'Capacitaciones'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CapacitacionUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Capacitacion
    form_class = CapacitacionForm
    template_name = 'capacitacion/create.html'
    success_url = reverse_lazy('erp:capacitacion_list')
    permission_required = 'change_capacitacion'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Capacitacion'
        context['entity'] = 'Capacitaciones'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CapacitacionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Capacitacion
    template_name = 'capacitacion/delete.html'
    success_url = reverse_lazy('erp:capacitacion_list')
    permission_required = 'delete_capacitacion'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Capacitacion'
        context['entity'] = 'Capacitaciones'
        context['list_url'] = self.success_url
        return context
    
    


    
