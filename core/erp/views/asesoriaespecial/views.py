from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import AsesoriaEspecialForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import AsesoriaEspecial


class AsesoriaEspecialListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = AsesoriaEspecial
    template_name = 'asesoriaespecial/list.html'
    permission_required = 'view_asesoriaespecial', 'change_asesoriaespecial', 'delete_asesoriaespecial', 'add_asesoriaespecial'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in AsesoriaEspecial.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de AsesoriaEspecial'
        context['create_url'] = reverse_lazy('erp:asesoriaespecial_create')
        context['list_url'] = reverse_lazy('erp:asesoriaespecial_list')
        context['entity'] = 'AsesoriasEspeciales'
        context['form'] = AsesoriaEspecialForm()
        return context


class AsesoriaEspecialCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = AsesoriaEspecial
    form_class = AsesoriaEspecialForm
    template_name = 'asesoriaespecial/create.html'
    success_url = reverse_lazy('erp:asesoriaespecial_list')
    permission_required = 'add_asesoriaespecial'
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
        context['title'] = 'Creación de una AsesoriaEspecial'
        context['entity'] = 'AsesoriasEspeciales'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AsesoriaEspecialUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = AsesoriaEspecial
    form_class = AsesoriaEspecialForm
    template_name = 'asesoriaespecial/create.html'
    success_url = reverse_lazy('erp:asesoriaespecial_list')
    permission_required = 'change_asesoriaespecial'
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
        context['title'] = 'Edición de una AsesoriaEspecial'
        context['entity'] = 'AsesoriasEspeciales'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class AsesoriaEspecialDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = AsesoriaEspecial
    template_name = 'asesoriaespecial/delete.html'
    success_url = reverse_lazy('erp:asesoriaespecial_list')
    permission_required = 'delete_asesoriaespecial'
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
        context['title'] = 'Eliminación de una AsesoriaEspecial'
        context['entity'] = 'AsesoriasEspeciales'
        context['list_url'] = self.success_url
        return context
