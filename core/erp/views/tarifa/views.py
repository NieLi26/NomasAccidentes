from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TarifaForm
from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import Tarifa


class TarifaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = "view_tarifa"
    model = Tarifa
    template_name = 'tarifa/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = [i.toJSON() for i in self.model.objects.all()]
                print(data)
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Tarifas"
        context['entity'] = "Tarifa"
        context['icon'] = "fas fa-donate"
        context['create_url'] = reverse_lazy('erp:tarifa_create')
        context['list_url'] = reverse_lazy('erp:tarifa_list')
        return context


class TarifaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = "add_tarifa"
    model = TarifaForm.Meta.model
    form_class = TarifaForm
    template_name = "tarifa/create.html"
    success_url = reverse_lazy('erp:tarifa_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opcion"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion de una Tarifa"
        context['entity'] = "Tarifa"
        context['icon'] = "fas fa-donate"
        context['list_url'] = reverse_lazy('erp:tarifa_list')
        context['action'] = "add"
        return context


class TarifaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = "change_tarifa"
    model = TarifaForm.Meta.model
    form_class = TarifaForm
    template_name = "tarifa/create.html"
    success_url = reverse_lazy('erp:tarifa_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opcion"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edicion de una Tarifa"
        context['entity'] = "Tarifa"
        context['icon'] = "fas fa-donate"
        context['list_url'] = reverse_lazy('erp:tarifa_list')
        context['action'] = "edit"
        return context


class TarifaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = "delete_tarifa"
    model = Tarifa
    template_name = "tarifa/delete.html"
    success_url = reverse_lazy('erp:tarifa_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminacion de una Tarifa"
        context['entity'] = "Tarifa"
        context['icon'] = "fas fa-donate"
        context['list_url'] = reverse_lazy('erp:tarifa_list')
        return context
