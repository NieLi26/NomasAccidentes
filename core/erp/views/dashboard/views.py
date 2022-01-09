import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from weasyprint import HTML, CSS
from datetime import datetime

from core.erp.forms import CapacitacionForm, FacturaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Accidente, Actividad, Capacitacion, Pago, Visita, Asesoria, AsesoriaEspecial, Empresa, Funcionario


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    # Grafico por empresa general

    def get_general_empresa(self):
        data = []
        try:
            for i in Empresa.objects.all():
                data.append(i.name)
        except:
            pass
        return data

    def get_empresa_cap(self):
        data = []
        try:
            for i in Empresa.objects.all():
                cap = Capacitacion.objects.filter(cli__id=i.id, completado=True).count()
                data.append(cap)
        except:
            pass
        return data

    def get_empresa_v(self):
        data = []
        try:
            for i in Empresa.objects.all():
                v = Visita.objects.filter(cli__id=i.id, completado=True).count()
                data.append(v)
        except:
            pass
        return data

    def get_empresa_ase(self):
        data = []
        try:
            for i in Empresa.objects.all():
                ase = Asesoria.objects.filter(cli__id=i.id, completado=True).count()
                data.append(ase)
        except:
            pass
        return data

    def get_empresa_asesp(self):
        data = []
        try:
            for i in Empresa.objects.all():
                asesp = AsesoriaEspecial.objects.filter(cli__id=i.id, completado=True).count()
                data.append(asesp)
        except:
            pass
        return data

        # Grafico por empresa

    # Grafico actividades por mes

    def get_general_cap_mes(self):
        data = []
        m = datetime.now().month
        try:
                cap = Capacitacion.objects.filter(fecha_realizacion__month=m, completado=True).count()
                data.append(cap)
        except:
            pass
        return data

    def get_general_v_mes(self):
        data = []
        m = datetime.now().month
        try:
                v = Visita.objects.filter(fecha_realizacion__month=m, completado=True).count()
                data.append(v)
        except:
            pass
        return data

    def get_general_ase_mes(self):
        data = []
        m = datetime.now().month
        try:
                ase = Asesoria.objects.filter(fecha_realizacion__month=m, completado=True).count()
                data.append(ase)
        except:
            pass
        return data

    def get_general_asesp_mes(self):
        data = []
        m = datetime.now().month
        try:
                asesp = AsesoriaEspecial.objects.filter(fecha_realizacion__month=m, completado=True).count()
                data.append(asesp)
        except:
            pass
        return data

        # Grafico por empresa

    # Grafico por funcionario

    def get_general_funcionario(self):
        data = []
        try:
            for i in Funcionario.objects.all():
                data.append(i.names)
        except:
            pass
        return data

    def get_funcionario_cap(self):
        data = []
        try:
            for i in Funcionario.objects.all():
                cap = Capacitacion.objects.filter(func__id=i.id, completado=True).count()
                data.append(cap)
        except:
            pass
        return data

    def get_funcionario_v(self):
        data = []
        try:
            for i in Funcionario.objects.all():
                v = Visita.objects.filter(func__id=i.id, completado=True).count()
                data.append(v)
        except:
            pass
        return data

    def get_funcionario_ase(self):
        data = []
        try:
            for i in Funcionario.objects.all():
                ase = Asesoria.objects.filter(func__id=i.id, completado=True).count()
                data.append(ase)
        except:
            pass
        return data

    def get_funcionario_asesp(self):
        data = []
        try:
            for i in Funcionario.objects.all():
                asesp = AsesoriaEspecial.objects.filter(func__id=i.id, completado=True).count()
                data.append(asesp)
        except:
            pass
        return data

    # GRAFICO 3D

    def get_cap_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                cap = Capacitacion.objects.filter(
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
                vis = Visita.objects.filter(
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
                ase = Asesoria.objects.filter(
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
                asesp = AsesoriaEspecial.objects.filter(
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
                acc = Accidente.objects.filter(
                    fecha_creacion__year=year, fecha_creacion__month=m).count()

                data.append(acc)

        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        data = []
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
            elif action == 'get_chart':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_empresa_cap()})
                data.append({'name': 'Visita', 'data': self.get_empresa_v()})
                data.append(
                    {'name': 'Asesoria', 'data': self.get_empresa_ase()})
                data.append({'name': 'Asesoria Especial',
                            'data': self.get_empresa_asesp()})
            elif action == 'get_chart2':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_funcionario_cap()})
                data.append(
                    {'name': 'Visita', 'data': self.get_funcionario_v()})
                data.append(
                    {'name': 'Asesoria', 'data': self.get_funcionario_ase()})
                data.append({'name': 'Asesoria Especial',
                            'data': self.get_funcionario_asesp()})
                
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
            elif action == 'get_spline':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_cap_año()})
                data.append({'name': 'Accidente',
                            'data': self.get_acc_año()})
            elif action == 'get_stacked':
                data = []
                data.append({'name': 'Capacitacion',
                            'data': self.get_cap_año()})
                data.append({'name': 'Accidente',
                            'data': self.get_acc_año()})
            elif action == 'get_pagos':
                data = []
                # for i in Pago.objects.all().order_by('fecha_creacion')[:3]: ///--- los primeros regisros, fijarse en el guion(-) del filtro
                for i in Pago.objects.all().order_by('-fecha_creacion')[:3]:
                    data.append(i.toJSON())    
            elif action == 'get_accidentes':
                data = []
                # for i in Accidente.objects.all().order_by('fecha_creacion')[:3]: ///--- los primeros regisros, fijarse en el guion(-) del filtro
                for i in Accidente.objects.all().order_by('-fecha_creacion')[:3]:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['entity'] = 'Reports'
        # LISTADO FINAL
        context['list_accidentes'] = Accidente.objects.last()
        # HOME PIE CHART
        context['mes_actual'] = datetime.now().strftime('%B del año %Y')
        context['general_cap_mes'] = self. get_general_cap_mes()
        context['general_v_mes'] = self. get_general_v_mes()
        context['general_ase_mes'] = self. get_general_ase_mes()
        context['general_asesp_mes'] = self. get_general_asesp_mes()
        ###############
        context['general_empresa'] = self.get_general_empresa()
        context['general_funcionario'] = self.get_general_funcionario()
        # cuadro superior
        context['cant_cli'] = Empresa.objects.filter(user__is_active=True).count()
        context['cant_func'] = Funcionario.objects.filter(user__is_active=True).count()
        context['cant_acc'] = Accidente.objects.all().count()
        context['cant_act'] = Asesoria.objects.filter(completado=True).count() + \
            AsesoriaEspecial.objects.filter(completado=True).count() + Capacitacion.objects.filter(completado=True).count() + \
            Visita.objects.filter(completado=True).count()
        # cuadro
        context['cant_cap'] = Capacitacion.objects.filter(completado=True).count()
        context['cant_vis'] = Visita.objects.filter(completado=True).count()
        context['cant_ase'] = Asesoria.objects.filter(completado=True).count()
        context['cant_asesp'] = AsesoriaEspecial.objects.filter(completado=True).count()
        # cuadro infefior
        context['empresa_cap'] = self.get_empresa_cap()
        context['empresa_v'] = self.get_empresa_v()
        context['empresa_ase'] = self.get_empresa_ase()
        context['empresa_asesp'] = self.get_empresa_asesp()
        context['list_url'] = reverse_lazy('reports:report_dashboard_empresa')
        context['form'] = FacturaForm()
        return context
