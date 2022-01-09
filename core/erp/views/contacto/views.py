from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ContactoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Contacto


class ContactoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Contacto
    template_name = 'contacto/list.html'
    permission_required = 'view_contacto', 'change_contacto', 'delete_contacto', 'add_contacto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Contacto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contactos'
        # context['create_url'] = reverse_lazy('erp:contacto_create')
        context['list_url'] = reverse_lazy('erp:contacto_list')
        context['entity'] = 'Contactoss'
        context['form'] = ContactoForm()
        return context



class ContactoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Contacto
    template_name = 'contacto/delete.html'
    success_url = reverse_lazy('erp:contacto_list')
    permission_required = 'delete_contacto'
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
        context['title'] = 'Eliminación de un Contacto'
        context['entity'] = 'Contactoss'
        context['list_url'] = self.success_url
        return context
