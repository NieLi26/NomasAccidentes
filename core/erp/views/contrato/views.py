import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.conf import settings
from weasyprint import HTML, CSS


from core.erp.forms import ContratoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Contrato


class ContratoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Contrato
    template_name = 'contrato/list.html'
    permission_required = 'view_contrato'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Contrato.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contratos'
        context['create_url'] = reverse_lazy('erp:contrato_create')
        context['list_url'] = reverse_lazy('erp:contrato_list')
        context['entity'] = 'Contratos'
        return context


class ContratoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contrato/create.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'add_contrato'
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
        context['title'] = 'Creación de un Contrato'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ContratoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contrato/create.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'change_contrato'
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
        context['title'] = 'Edición de un Contrato'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ContratoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'contrato/delete.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'delete_contrato'
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
        context['title'] = 'Eliminación de un Contrato'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        return context


class ContratoInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('contrato/invoice.html')
            context = {
                'cont': Contrato.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:contrato_list'))