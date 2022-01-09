import os

from django.forms.widgets import NumberInput

from core.erp.forms import EmpresaForm, FacturaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import (Asesoria, AsesoriaEspecial, Capacitacion, Contrato, Empresa,
                             Pago, Visita, Accidente)
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView, View)
from weasyprint import CSS, HTML

from django.db.models.functions import Coalesce
from django.db.models import Sum
from datetime import date, datetime, timedelta



# Idioma "es-ES" (código para el español de España)
# import locale
# locale.setlocale(locale.LC_ALL, 'es-ES')



class EmpresaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresa/list.html'
    permission_required = 'view_empresa'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Empresa.objects.all():
                    data.append(i.toJSON())
            elif action == 'searchdata_details':
                data = []
                for i in Pago.objects.filter(cli__id=request.POST['id']):
                    print(i)
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empresas'
        context['create_url'] = reverse_lazy('erp:empresa_create')
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['entity'] = 'Empresas'
        return context


class EmpresaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('erp:empresa_list')
    permission_required = 'add_empresa'
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
        context['title'] = 'Creación una Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class EmpresaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('erp:empresa_list')
    permission_required = 'change_empresa'
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
        context['title'] = 'Edición una Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class EmpresaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Empresa
    template_name = 'empresa/delete.html'
    success_url = reverse_lazy('erp:empresa_list')
    permission_required = 'delete_empresa'
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
        context['title'] = 'Eliminación de una Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = self.success_url
        return context


class EmpresaInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('empresa/invoice.html')
            context = {
                'p': Empresa.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:empresa_list'))


class EmpresaDashboardView(LoginRequiredMixin, TemplateView):
    model = Empresa
    template_name = 'empresa/dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

   # GRAFICO ACTIVIDADES POR MES

    def get_general_cap_mes(self):
        data = []
        m = datetime.now().month
        try:
            cap = Capacitacion.objects.filter(
                cli__id=self.kwargs['pk'], fecha_realizacion__month=m, completado=True).count()
            data = cap
        except:
            pass
        return data

    def get_general_v_mes(self):
        data = []
        m = datetime.now().month
        try:
            v = Visita.objects.filter(
                cli__id=self.kwargs['pk'], fecha_realizacion__month=m, completado=True).count()
            data=v
        except:
            pass
        return data

    def get_general_ase_mes(self):
        data = []
        m = datetime.now().month
        try:
            ase = Asesoria.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m,completado=True).count()
            data = ase
        except:
            pass
        return data

    def get_general_asesp_mes(self):
        data = []
        m = datetime.now().month
        try:
            asesp = AsesoriaEspecial.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m,completado=True).count()
            data = asesp
        except:
            pass
        return data

        # Grafico por empresa

    def get_general_acc_mes(self):
        data = []
        m = datetime.now().month
        try:
            emp = Empresa.objects.get(
                id=self.kwargs['pk'])
            asesp = Accidente.objects.filter(
                nombre=emp.user.username, fecha_creacion__month=m).count()
            data = asesp
        except:
            pass
        return data

    # GRAFICO AREA

    def get_cap_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                cap = Capacitacion.objects.filter(cli__id=self.kwargs['pk'],
                                                  fecha_realizacion__year=year, fecha_realizacion__month=m, completado=True).count()

                data.append(cap)

        except:
            pass
        return data

    def get_vis_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                vis = Visita.objects.filter(cli__id=self.kwargs['pk'],
                                            fecha_realizacion__year=year, fecha_realizacion__month=m, completado=True).count()

                data.append(vis)

        except:
            pass
        return data

    def get_ase_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                ase = Asesoria.objects.filter(cli__id=self.kwargs['pk'],
                                              fecha_realizacion__year=year, fecha_realizacion__month=m, completado=True).count()

                data.append(ase)

        except:
            pass
        return data

    def get_asesp_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                asesp = AsesoriaEspecial.objects.filter(cli__id=self.kwargs['pk'],
                                                        fecha_realizacion__year=year, fecha_realizacion__month=m, completado=True).count()

                data.append(asesp)

        except:
            pass
        return data

    def get_acc_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                emp = Empresa.objects.get(
                    id=self.kwargs['pk'])
                acc = Accidente.objects.filter(nombre=emp.user.username,
                                               fecha_creacion__year=year, fecha_creacion__month=m).count()

                data.append(acc)

        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = AsesoriaEspecial.objects.filter(completado=True)
                search2 = Asesoria.objects.filter(completado=True)
                search3 = Visita.objects.filter(completado=True)
                search4 = Capacitacion.objects.filter(completado=True)
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_realizacion__range=[
                                           start_date, end_date])
                    search2 = search2.filter(fecha_realizacion__range=[
                        start_date, end_date])
                    search3 = search3.filter(fecha_realizacion__range=[
                        start_date, end_date])
                    search4 = search4.filter(fecha_realizacion__range=[
                        start_date, end_date])

                    data = {
                        'type': 'column',
                        'colorByPoint': True,
                        'showInLegend': False,
                        'data': [search4.count(),
                                 search3.count(),
                                 search2.count(),
                                 search.count()
                                 ]
                    }
            elif action == 'search_report2':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                emp = Empresa.objects.get(
                    id=self.kwargs['pk'])
                search = Accidente.objects.filter(nombre=emp.user.username)
                search2 = Capacitacion.objects.filter(
                    cli__id=self.kwargs['pk'], completado=True)
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_creacion__range=[
                                           start_date, end_date])
                    search2 = search2.filter(fecha_realizacion__range=[
                        start_date, end_date])

                    nom = 'accidente'
                    nom2 = 'capacitacion'

                    data = {
                        'name': 'Rendimiento',
                        'colorByPoint': True,
                        'data': [
                            {
                                'name': nom,
                                'y': search.count(),
                            },
                            {
                                'name': nom2,
                                'y': search2.count(),
                            }
                        ]
                    }
            elif action == 'get_column':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_cap_año()})
                data.append({'name': 'Visita',
                            'data': self.get_vis_año()})
                data.append({'name': 'Asesoria',
                            'data': self.get_ase_año()})
                data.append({'name': 'Asesoria Especial',
                            'data': self.get_asesp_año()})            
            elif action == 'get_stacked':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_cap_año()})
                data.append({'name': 'Accidente',
                            'data': self.get_acc_año()})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de Rendimiento cliente'
        context['entity'] = 'Reports'
        # cuadro superior
        context['cant_cap'] = Capacitacion.objects.filter(cli__id=self.kwargs['pk'],completado=True).count()
        context['cant_vis'] = Visita.objects.filter(cli__id=self.kwargs['pk'],completado=True).count()
        context['cant_ase'] = Asesoria.objects.filter(cli__id=self.kwargs['pk'],completado=True).count()
        context['cant_asesp'] = AsesoriaEspecial.objects.filter(cli__id=self.kwargs['pk'],completado=True).count()
        context['cant_act_mes'] = self.get_general_cap_mes() + self.get_general_v_mes() + self.get_general_ase_mes() + self.get_general_asesp_mes()
        # emp = Empresa.objects.get(id=self.kwargs['pk'])
        context['cant_acc'] = Accidente.objects.filter(nombre=Empresa.objects.get(id=self.kwargs['pk']).user.username).count()
        # HOME PIE CHART
        context['mes_actual'] = datetime.now().strftime('%B del año %Y')
        context['general_cap_mes'] = self.get_general_cap_mes()
        context['general_v_mes'] = self.get_general_v_mes()
        context['general_ase_mes'] = self.get_general_ase_mes()
        context['general_asesp_mes'] = self.get_general_asesp_mes()
        context['general_acc_mes'] = self.get_general_acc_mes()
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['form'] = FacturaForm()
        return context

class EmpresaDashboardPrintView(LoginRequiredMixin, TemplateView):
    model = Empresa
    template_name = 'empresa/grafico_invoice.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de Dashboard'
        context['entity'] = 'Dashboard'
        # context['list_url'] = reverse_lazy('erp:empresa_list')
        return context

class GraficoInvoicePdfView(View):

   # GRAFICO ACTIVIDADES POR MES

    def get_general_cap_mes(self):
        data = []
        m = datetime.now().month
        try:
            cap = Capacitacion.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m).count()
            data = cap
        except:
            pass
        return data

    def get_general_v_mes(self):
        data = []
        m = datetime.now().month
        try:
            v = Visita.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m).count()
            data=v
        except:
            pass
        return data

    def get_general_ase_mes(self):
        data = []
        m = datetime.now().month
        try:
            ase = Asesoria.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m).count()
            data = ase
        except:
            pass
        return data

    def get_general_asesp_mes(self):
        data = []
        m = datetime.now().month
        try:
            asesp = AsesoriaEspecial.objects.filter(
                cli__id=self.kwargs['pk'], fecha_creacion__month=m).count()
            data = asesp
        except:
            pass
        return data

        # Grafico por empresa

    def get_general_acc_mes(self):
        data = []
        m = datetime.now().month
        try:
            emp = Empresa.objects.get(
                id=self.kwargs['pk'])
            asesp = Accidente.objects.filter(
                nombre=emp.user.username, fecha_creacion__month=m).count()
            data = asesp
        except:
            pass
        return data


    def get(self, request, *args, **kwargs):
        try:
            template = get_template('empresa/grafico_invoice.html')
            context = {
                'general_cap_mes': self.get_general_cap_mes(),
                'general_v_mes': self.get_general_v_mes(),
                'general_ase_mes': self.get_general_ase_mes(),
                'general_asesp_mes': self.get_general_asesp_mes(),
                'general_acc_mes': self.get_general_acc_mes(),
                'cant_act_mes': self.get_general_cap_mes() + self.get_general_v_mes() + self.get_general_ase_mes() + self.get_general_asesp_mes()
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:empresa_list'))



class FacturaView(TemplateView):
    template_name = 'empresa/factura.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                cont = Contrato.objects.filter(
                    emp__id=self.kwargs['pk'])
                search = Pago.objects.filter(
                    cli__id=self.kwargs['pk'])
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_creacion__range=[
                                           start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.asunto,
                        s.fecha_creacion.strftime('%Y-%m-%d'),
                        format(s.valor, '.2f'),
                        # format(s.iva, '.2f'),
                        # format(s.total, '.2f'),
                    ])

                # pago = Pago.objects.filter(
                #     cli__id=self.kwargs['pk'])
                # subtotal = search.aggregate(
                #     r=Coalesce(Sum('valor'), 0)).get('r')
                # iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(
                    Sum('valor') + 100000, 0)).get('r')

                if total == 0:
                    for c in cont:
                        data.append([
                            '---',
                            'Precio Base',
                            c.fecha_creacion.strftime('%Y-%m-%d'),
                            # format(subtotal, '.2f'),
                            # format(iva, '.2f'),
                            '100000'
                        ])
                else:
                    for c in cont:
                        data.append([
                            '---',
                            'Precio Base',
                            c.fecha_creacion.strftime('%Y-%m-%d'),
                            # format(subtotal, '.2f'),
                            # format(iva, '.2f'),
                            '100000'
                        ])

                    data.append([
                        '---',
                        '---',
                        '---',
                        # format(subtotal, '.2f'),
                        # format(iva, '.2f'),
                        format(total, '.2f'),
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura'
        context['entity'] = 'Facturas'
        context['emp'] = Empresa.objects.get(id=self.kwargs['pk'])
        context['fecha'] = date.today().strftime(
            '%Y/%m/%d')
        context['cont'] = Contrato.objects.get(emp__id=self.kwargs['pk']).fecha_termino.strftime(
            '%Y/%m/%d')
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['form'] = FacturaForm()
        return context
