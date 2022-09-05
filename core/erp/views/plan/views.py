from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TarifaPlanForm
from core.erp.mixin import ValidatePermissionRequiredMixin
from core.erp.models import TarifaPlan


class TarifaPlanListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = "view_tarifaplan"
    model = TarifaPlan
    template_name = 'plan/list.html'

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
        context['title'] = "Listado Tarifa de Planes"
        context['entity'] = "Tarifa Plan"
        context['icon'] = "fas fa-clipboard-list"
        context['create_url'] = reverse_lazy('erp:tarifa_plan_create')
        context['list_url'] = reverse_lazy('erp:tarifa_plan_list')
        return context


class TarifaPlanCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = "add_tarifaplan"
    model = TarifaPlanForm.Meta.model
    form_class = TarifaPlanForm
    template_name = "plan/create.html"
    success_url = reverse_lazy('erp:tarifa_plan_list')

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
        context['title'] = "Creacion de un plan"
        context['entity'] = "plan"
        context['icon'] = "fas fa-clipboard-list"
        context['list_url'] = reverse_lazy('erp:tarifa_plan_list')
        context['action'] = "add"
        return context


class TarifaPlanUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = "change_tarifaplan"
    model = TarifaPlanForm.Meta.model
    form_class = TarifaPlanForm
    template_name = "plan/create.html"
    success_url = reverse_lazy('erp:tarifa_plan_list')

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
        context['title'] = "Edicion de un plan"
        context['entity'] = "plan"
        context['icon'] = "fas fa-clipboard-list"
        context['list_url'] = reverse_lazy('erp:tarifa_plan_list')
        context['action'] = "edit"
        return context


class TarifaPlanDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = "delete_tarifaplan"
    model = TarifaPlan
    template_name = "plan/delete.html"
    success_url = reverse_lazy('erp:tarifa_plan_list')

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
        context['title'] = "Eliminacion de un plan"
        context['entity'] = "plan"
        context['icon'] = "fas fa-clipboard-list"
        context['list_url'] = reverse_lazy('erp:tarifa_plan_list')
        return context
