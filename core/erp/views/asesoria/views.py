from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import AsesoriaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Asesoria


class AsesoriaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Asesoria
    template_name = 'asesoria/list.html'
    permission_required = 'view_asesoria', 'change_asesoria', 'delete_asesoria', 'add_asesoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Asesoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asesorias'
        context['create_url'] = reverse_lazy('erp:asesoria_create')
        context['list_url'] = reverse_lazy('erp:asesoria_list')
        context['entity'] = 'Asesorias'
        context['form'] = AsesoriaForm()
        return context


class AsesoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Asesoria
    form_class = AsesoriaForm
    template_name = 'asesoria/create.html'
    success_url = reverse_lazy('erp:asesoria_list')
    permission_required = 'add_asesoria'
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
        context['title'] = 'Creación de una Asesoria'
        context['entity'] = 'Asesorias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AsesoriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Asesoria
    form_class = AsesoriaForm
    template_name = 'asesoria/create.html'
    success_url = reverse_lazy('erp:asesoria_list')
    permission_required = 'change_asesoria'
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
        context['title'] = 'Edición de una Asesoria'
        context['entity'] = 'Asesorias'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class AsesoriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Asesoria
    template_name = 'asesoria/delete.html'
    success_url = reverse_lazy('erp:asesoria_list')
    permission_required = 'delete_asesoria'
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
        context['title'] = 'Eliminación de una Asesoria'
        context['entity'] = 'Asesorias'
        context['list_url'] = self.success_url
        return context
