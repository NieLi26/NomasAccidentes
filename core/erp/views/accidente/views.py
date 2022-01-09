import smtplib
from typing import DefaultDict
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string


from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.forms import Form
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect

from core.erp.forms import AccidenteForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Accidente, Empresa, Funcionario
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from notifications.signals import notify
from config import settings
from django.contrib.auth import  get_user_model


User = get_user_model()

class AccidenteListView(LoginRequiredMixin, ListView):
    model = Accidente
    template_name = 'accidente/list.html'
    permission_required = 'view_accidente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Accidente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Accidentes'
        context['create_url'] = reverse_lazy('erp:accidente_create')
        context['list_url'] = reverse_lazy('erp:accidente_list')
        context['entity'] = 'Accidentes'
        return context


class AccidenteCreateView(LoginRequiredMixin, CreateView):
    model = Accidente
    form_class = AccidenteForm
    template_name = 'accidente/create.html'
    success_url = reverse_lazy('erp:dashboard')
    # permission_required = 'add_accidente'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_accidente(self, user):
        data = {}
        # perro = Empresa.objects.filter(user=self.request.user)
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER,
                             settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Alerta Accidente'

            content = render_to_string('accidente/send_email.html', {
                'user': user,
                'emp': Empresa.objects.get(user=user)
                # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                # 'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    # @receiver(post_save, sender=Accidente)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                accidente = Accidente.objects.create(
                    nombre=self.request.user.username, correo=self.request.user.email)
                data = accidente.save()
                # request_finished.connect(self.print_finish)
                # print("se genero alerta de accidente")
                user = self.request.user
                data = self.send_email_accidente(user)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def my_notify(sender, instance, created, **kwargs):
        if created:
            # lo = user.objects.all()
            # for i in Funcionario.objects.all():
            users = User.objects.filter(groups__name__in=['Administrador', 'Funcionario'])
            notify.send(instance, recipient=users,
                        verb='Alerta de accidente', description='Se genero una alerta de accidente', soft_delete=True)


    post_save.connect(my_notify, sender=Accidente)


    # def ready(self):
    #     request_finished.connect(self.print_finish)
    

    # def print_finish(self, sender, **kwargs):
    #     print('Se ha generado una alerta de accidente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Alertar un Accidente'
        context['entity'] = 'Accidentes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AccidenteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Accidente
    form_class = AccidenteForm
    template_name = 'accidente/create.html'
    success_url = reverse_lazy('erp:accidente_list')
    permission_required = 'change_accidente'
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
        context['title'] = 'Edición de un Accidente'
        context['entity'] = 'Accidentes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class AccidenteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Accidente
    template_name = 'accidente/delete.html'
    success_url = reverse_lazy('erp:accidente_list')
    permission_required = 'delete_accidente'
    url_redirect = success_url

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
        context['title'] = 'Eliminación de un Accidente'
        context['entity'] = 'Accidentes'
        context['list_url'] = self.success_url
        return context
