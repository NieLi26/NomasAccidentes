from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.forms import EstacionamientoForm
from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import Estacionamiento


class EstacionamientoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    permission_required = "view_estacionamiento"
    model = Estacionamiento
    template_name = 'estacionamiento/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                # data = []
                # for i in Estacionamiento.objects.all():
                #     data.append(i.toJSON())
                data = [i.toJSON() for i in Estacionamiento.objects.all()]
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Estacionamientos"
        context['entity'] = "Estacionamiento"
        context['icon'] = "fas fa-map-pin"
        context['create_url'] = reverse_lazy('erp:estacionamiento_create')
        context['list_url'] = reverse_lazy('erp:estacionamiento_list')
        return context


class EstacionamientoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = "add_estacionamiento"
    model = Estacionamiento
    form_class = EstacionamientoForm
    template_name = "estacionamiento/create.html"
    success_url = reverse_lazy('erp:estacionamiento_list')

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
        context['title'] = "Creacion de un Estacionamiento"
        context['entity'] = "Estacionamiento"
        context['icon'] = "fas fa-map-pin"
        context['list_url'] = reverse_lazy('erp:estacionamiento_list')
        context['action'] = "add"
        return context


class EstacionamientoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = "change_estacionamiento"
    model = Estacionamiento
    form_class = EstacionamientoForm
    template_name = "estacionamiento/create.html"
    success_url = reverse_lazy('erp:estacionamiento_list')

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
        context['title'] = "Edicion de un Estacionamiento"
        context['entity'] = "Estacionamiento"
        context['icon'] = "fas fa-map-pin"
        context['list_url'] = reverse_lazy('erp:estacionamiento_list')
        context['action'] = "edit"
        return context


class EstacionamientoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = "delete_estacionamiento"
    model = Estacionamiento
    template_name = "estacionamiento/delete.html"
    success_url = reverse_lazy('erp:estacionamiento_list')

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
        context['title'] = "Eliminacion de un Estacionamiento"
        context['entity'] = "Estacionamiento"
        context['icon'] = "fas fa-map-pin"
        context['list_url'] = reverse_lazy('erp:estacionamiento_list')
        return context
