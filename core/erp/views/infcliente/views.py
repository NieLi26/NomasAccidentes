import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.conf import settings
from weasyprint import HTML, CSS

from core.erp.forms import AsesoriaForm, AsesoriaEspecialForm, CapacitacionForm, CasoForm, PagoForm, VisitaForm, CheckListForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Asesoria, AsesoriaEspecial, Capacitacion, Caso, Contrato, Pago, Visita, CheckList


class InfAsesoriaListView(LoginRequiredMixin, ListView):
    model = Asesoria
    template_name = 'infcliente/listase.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Asesoria.objects.filter(cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asesorias'
        # context['create_url'] = reverse_lazy('erp:asesoria_create')
        context['list_url'] = reverse_lazy('erp:infcliente_asesoria_list')
        context['entity'] = 'Asesorias'
        context['form'] = AsesoriaForm()
        return context


class InfAsesoriaEspecialListView(LoginRequiredMixin, ListView):
    model = AsesoriaEspecial
    template_name = 'infcliente/listasesp.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in AsesoriaEspecial.objects.filter(cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de AsesoriaEspecial'
        # context['create_url'] = reverse_lazy('erp:asesoriaespecial_create')
        context['list_url'] = reverse_lazy(
            'erp:infcliente_asesoriaespecial_list')
        context['entity'] = 'AsesoriasEspeciales'
        context['form'] = AsesoriaEspecialForm()
        return context


class InfCapacitacionListView(LoginRequiredMixin, ListView):
    model = Capacitacion
    template_name = 'infcliente/listcap.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Capacitacion.objects.filter(cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Capacitaciones'
        # context['create_url'] = reverse_lazy('erp:capacitacion_create')
        context['list_url'] = reverse_lazy('erp:infcliente_capacitacion_list')
        context['entity'] = 'Capacitaciones'
        context['form'] = CapacitacionForm()
        return context


class InfCasoListView(LoginRequiredMixin, ListView):
    model = Caso
    template_name = 'infcliente/listcaso.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Caso.objects.filter(ase__cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Casos'
        # context['create_url'] = reverse_lazy('erp:caso_create')
        context['list_url'] = reverse_lazy('erp:infcliente_caso_list')
        context['entity'] = 'Casos'
        context['form'] = CasoForm()
        return context


class InfVisitaListView(LoginRequiredMixin, ListView):
    model = Visita
    template_name = 'infcliente/listv.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Visita.objects.filter(cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Visitas'
        # context['create_url'] = reverse_lazy('erp:visita_create')
        context['list_url'] = reverse_lazy('erp:infcliente_visita_list')
        context['entity'] = 'Visitas'
        context['form'] = VisitaForm()
        return context


class InfResultadoVisitaListView(LoginRequiredMixin, ListView):
    model = CheckList
    template_name = 'infcliente/listrv.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CheckList.objects.filter(cli__user=self.request.user):
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de CheckList'
        # context['create_url'] = reverse_lazy('erp:resultadovisita_create')
        context['list_url'] = reverse_lazy(
            'erp:infcliente_resultadovisita_list')
        context['entity'] = 'CheckList'
        context['form'] = CheckListForm()
        return context


class InfPagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'infcliente/listpago.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pago.objects.filter(cli__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pagos'
        # context['create_url'] = reverse_lazy('erp:capacitacion_create')
        context['list_url'] = reverse_lazy('erp:infcliente_pago_list')
        context['entity'] = 'Pagos'
        context['form'] = PagoForm()
        return context
    
    
class InfContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'infcliente/listcontrato.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Contrato.objects.filter(emp__user=self.request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contrato'
        # context['create_url'] = reverse_lazy('erp:capacitacion_create')
        context['list_url'] = reverse_lazy('erp:infcliente_contrato_list')
        context['entity'] = 'Contrato'
        # context['form'] = PagoForm()
        return context



# INVOICE

class InfContratoInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/contratoinvoice.html')
            context = {
                'cont': Contrato.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_contrato_list'))

class InfAsesoriaInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/aseinvoice.html')
            context = {
                'ase': Asesoria.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_asesoria_list'))


class InfAsesoriaEspecialInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/asespinvoice.html')
            context = {
                'asesp': AsesoriaEspecial.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_asesoriaespecial_list'))


class InfCapacitacionInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/capinvoice.html')
            context = {
                'cap': Capacitacion.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_capacitacion_list'))


class InfCasoInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/cainvoice.html')
            context = {
                'ca': Caso.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_caso_list'))


class InfVisitaInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/vinvoice.html')
            context = {
                'v': Visita.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_visita_list'))


class InfResultadoVisitaInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/rvinvoice.html')
            context = {
                'rv': CheckList.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_resultadovisita_list'))


class InfPagoInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('infcliente/pagoinvoice.html')
            context = {
                'pago': Pago.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:infcliente_pago_list'))

#detalle


class DetalleCapacitacionView(TemplateView):
    template_name = 'infcliente/detcapacitacion.html'

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
        context['title'] = 'Detalle'
        context['entity'] = 'Detalles'
        # context['emp'] = Empresa.objects.get(id=self.kwargs['pk'])
        # context['fecha'] = date.today().strftime(
        #     '%Y/%m/%d')
        # context['cont'] = Contrato.objects.get(emp__id=self.kwargs['pk']).fecha_termino.strftime(
        #     '%Y/%m/%d')
        # context['list_url'] = reverse_lazy('erp:empresa_list')
        # context['form'] = FacturaForm()
        return context
