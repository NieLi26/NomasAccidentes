from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import VisitaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Visita


class VisitaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Visita
    template_name = 'visita/list.html'
    permission_required = 'view_visita', 'change_visita', 'delete_visita', 'add_visita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Visita.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Visitas'
        context['create_url'] = reverse_lazy('erp:visita_create')
        context['list_url'] = reverse_lazy('erp:visita_list')
        context['entity'] = 'Visitas'
        context['form'] = VisitaForm()
        return context


class VisitaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Visita
    form_class = VisitaForm
    template_name = 'visita/create.html'
    success_url = reverse_lazy('erp:visita_list')
    permission_required = 'add_visita'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Visita'
        context['entity'] = 'Visitas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class VisitaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Visita
    form_class = VisitaForm
    template_name = 'visita/create.html'
    success_url = reverse_lazy('erp:visita_list')
    permission_required = 'change_visita'
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
        context['title'] = 'Edición de una Visita'
        context['entity'] = 'Visitas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class VisitaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Visita
    template_name = 'visita/delete.html'
    success_url = reverse_lazy('erp:visita_list')
    permission_required = 'delete_visita'
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
        context['title'] = 'Eliminación de una Visita'
        context['entity'] = 'Visitas'
        context['list_url'] = self.success_url
        return context
