import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.conf import settings
from django.views.generic.base import TemplateView
from weasyprint import HTML, CSS

from core.erp.forms import CheckListForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import CheckList


class CheckListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CheckList
    template_name = 'checklist/list.html'
    permission_required = 'view_checklist'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # position = 1
                for i in CheckList.objects.all():
                    # item = i.toJSON()
                    # item['position'] = position
                    data.append(i.toJSON())
                    # position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de CheckList'
        context['create_url'] = reverse_lazy('erp:checklist_create')
        context['list_url'] = reverse_lazy('erp:checklist_list')
        context['entity'] = 'CheckLists'
        context['form'] = CheckListForm()
        return context


class CheckListCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = CheckList
    form_class = CheckListForm
    template_name = 'checklist/create.html'
    success_url = reverse_lazy('erp:checklist_list')
    permission_required = 'add_checklist'
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
        context['title'] = 'Creación de un CheckList'
        context['entity'] = 'CheckList'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CheckListUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = CheckList
    form_class = CheckListForm
    template_name = 'checklist/create.html'
    success_url = reverse_lazy('erp:checklist_list')
    permission_required = 'change_checklist'
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
        context['title'] = 'Edición un CheckList'
        context['entity'] = 'CheckLists'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CheckListDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CheckList
    template_name = 'checklist/delete.html'
    success_url = reverse_lazy('erp:checklist_list')
    permission_required = 'delete_checklist'
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
        context['title'] = 'Eliminación de un CheckList'
        context['entity'] = 'CheckLists'
        context['list_url'] = self.success_url
        return context


class CheckListInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('checklist/invoice.html')
            context = {
                'ch': CheckList.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:checklist_list'))


class TodoListView(TemplateView):
    template_name = 'checklist/todolist.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'search_report':
    #             data = []
    #             start_date = request.POST.get('start_date', '')
    #             end_date = request.POST.get('end_date', '')
    #             cont = Contrato.objects.filter(
    #                 emp__id=self.kwargs['pk'])
    #             search = Pago.objects.filter(
    #                 cli__id=self.kwargs['pk'])
    #             if len(start_date) and len(end_date):
    #                 search = search.filter(fecha_creacion__range=[
    #                                        start_date, end_date])
    #             for s in search:
    #                 data.append([
    #                     s.id,
    #                     s.asunto,
    #                     s.fecha_creacion.strftime('%Y-%m-%d'),
    #                     format(s.valor, '.2f'),
    #                     # format(s.iva, '.2f'),
    #                     # format(s.total, '.2f'),
    #                 ])

    #             # pago = Pago.objects.filter(
    #             #     cli__id=self.kwargs['pk'])
    #             # subtotal = search.aggregate(
    #             #     r=Coalesce(Sum('valor'), 0)).get('r')
    #             # iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
    #             total = search.aggregate(r=Coalesce(
    #                 Sum('valor') + 100000, 0)).get('r')

    #             if total == 0:
    #                 for c in cont:
    #                     data.append([
    #                         '---',
    #                         'Precio Base',
    #                         c.fecha_creacion.strftime('%Y-%m-%d'),
    #                         # format(subtotal, '.2f'),
    #                         # format(iva, '.2f'),
    #                         '100000'
    #                     ])
    #             else:
    #                 for c in cont:
    #                     data.append([
    #                         '---',
    #                         'Precio Base',
    #                         c.fecha_creacion.strftime('%Y-%m-%d'),
    #                         # format(subtotal, '.2f'),
    #                         # format(iva, '.2f'),
    #                         '100000'
    #                     ])

    #                 data.append([
    #                     '---',
    #                     '---',
    #                     '---',
    #                     # format(subtotal, '.2f'),
    #                     # format(iva, '.2f'),
    #                     format(total, '.2f'),
    #                 ])
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura'
        context['entity'] = 'Facturas'
        # context['emp'] = Empresa.objects.get(id=self.kwargs['pk'])
        # context['fecha'] = date.today().strftime(
        #     '%Y/%m/%d')
        # context['cont'] = Contrato.objects.get(emp__id=self.kwargs['pk']).fecha_termino.strftime(
        #     '%Y/%m/%d')
        context['list_url'] = reverse_lazy('erp:checklist_list')
        context['form'] = CheckListForm()
        return context
