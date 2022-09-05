from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ClienteForm
from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import Cliente


class ClienteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = "view_cliente"
    model = Cliente
    template_name = 'cliente/list.html'

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
        context['title'] = "Listado de Clientes"
        context['entity'] = "Cliente"
        context['icon'] = "fas fa-users"
        context['create_url'] = reverse_lazy('erp:cliente_create')
        context['list_url'] = reverse_lazy('erp:cliente_list')
        return context


class ClienteCreateView(LoginRequiredMixin, CreateView):
    # permission_required = "add_cliente"
    model = ClienteForm.Meta.model
    form_class = ClienteForm
    template_name = "cliente/create.html"
    success_url = reverse_lazy('erp:cliente_list')

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
        context['title'] = "Creacion de una Cliente"
        context['entity'] = "Cliente"
        context['icon'] = "fas fa-users"
        context['list_url'] = reverse_lazy('erp:cliente_list')
        context['action'] = "add"
        return context


class ClienteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = "change_cliente"
    model = ClienteForm.Meta.model
    form_class = ClienteForm
    template_name = "cliente/create.html"
    success_url = reverse_lazy('erp:cliente_list')

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
        context['title'] = "Edicion de una Cliente"
        context['entity'] = "Cliente"
        context['icon'] = "fas fa-users"
        context['list_url'] = reverse_lazy('erp:cliente_list')
        context['action'] = "edit"
        return context


class ClienteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = "delete_cliente"
    model = Cliente
    template_name = "cliente/delete.html"
    success_url = reverse_lazy('erp:cliente_list')

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
        context['title'] = "Eliminacion de una Cliente"
        context['entity'] = "Cliente"
        context['icon'] = "fas fa-users"
        context['list_url'] = reverse_lazy('erp:cliente_list')
        return context
