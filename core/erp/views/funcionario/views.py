from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from core.erp.forms import FuncionarioForm, FacturaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Empresa, Funcionario, Asesoria, AsesoriaEspecial, Visita, Capacitacion, Accidente

# import locale
# locale.setlocale(locale.LC_ALL, 'es-ES')

class FuncionarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Funcionario
    template_name = 'funcionario/list.html'
    permission_required = 'view_funcionario'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Funcionario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Funcionarios'
        context['create_url'] = reverse_lazy('erp:funcionario_create')
        context['list_url'] = reverse_lazy('erp:funcionario_list')
        context['entity'] = 'Funcionarios'
        return context


class FuncionarioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/create.html'
    success_url = reverse_lazy('erp:funcionario_list')
    permission_required = 'add_funcionario'
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
        context['title'] = 'Creación un Funcionario'
        context['entity'] = 'Funcionarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class FuncionarioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/create.html'
    success_url = reverse_lazy('erp:funcionario_list')
    permission_required = 'change_funcionario'
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
        context['title'] = 'Edición un Funcionario'
        context['entity'] = 'Funcionarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class FuncionarioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario/delete.html'
    success_url = reverse_lazy('erp:funcionario_list')
    permission_required = 'delete_funcionario'
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
        context['title'] = 'Eliminación de un Funcionario'
        context['entity'] = 'Funcionarios'
        context['list_url'] = self.success_url
        return context


class FuncionarioDashboardView(LoginRequiredMixin, TemplateView):
    model = Funcionario
    template_name = 'funcionario/dashboard.html'

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
                func__id=self.kwargs['pk'], fecha_realizacion__month=m,completado=True).count()
            data.append(cap)
        except:
            pass
        return data

    def get_general_v_mes(self):
        data = []
        m = datetime.now().month
        try:
            v = Visita.objects.filter(
                func__id=self.kwargs['pk'], fecha_realizacion__month=m,completado=True).count()
            data.append(v)
        except:
            pass
        return data

    def get_general_ase_mes(self):
        data = []
        m = datetime.now().month
        try:
            ase = Asesoria.objects.filter(
                func__id=self.kwargs['pk'], fecha_realizacion__month=m, completado=True).count()
            data.append(ase)
        except:
            pass
        return data

    def get_general_asesp_mes(self):
        data = []
        m = datetime.now().month
        try:
            asesp = AsesoriaEspecial.objects.filter(
                func__id=self.kwargs['pk'], fecha_realizacion__month=m, completado=True).count()
            data.append(asesp)
        except:
            pass
        return data

        # Grafico por empresa

    # GRAFICO AREA

    def get_cap_año(self):
        data = []
        year = datetime.now().year
        try:
            for m in range(1, 13):
                cap = Capacitacion.objects.filter(func__id=self.kwargs['pk'],
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
                vis = Visita.objects.filter(func__id=self.kwargs['pk'],
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
                ase = Asesoria.objects.filter(func__id=self.kwargs['pk'],
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
                asesp = AsesoriaEspecial.objects.filter(func__id=self.kwargs['pk'],
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
                func = Empresa.objects.get(
                    func__id=self.kwargs['pk'])
                acc = Accidente.objects.filter(nombre=func.user.username,
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
        context['title'] = 'Panel de Rendimiento funcionario'
        context['entity'] = 'Reports'
        # cuadro superior
        context['cant_cap'] = Capacitacion.objects.filter(func__id=self.kwargs['pk'], completado=True).count()
        context['cant_vis'] = Visita.objects.filter(func__id=self.kwargs['pk'], completado=True).count()
        context['cant_ase'] = Asesoria.objects.filter(func__id=self.kwargs['pk'], completado=True).count()
        context['cant_asesp'] = AsesoriaEspecial.objects.filter(func__id=self.kwargs['pk'], completado=True).count()
        # HOME PIE CHART
        context['mes_actual'] = datetime.now().strftime('%B del año %Y')
        context['general_cap_mes'] = self. get_general_cap_mes()
        context['general_v_mes'] = self. get_general_v_mes()
        context['general_ase_mes'] = self. get_general_ase_mes()
        context['general_asesp_mes'] = self. get_general_asesp_mes()
        context['list_url'] = reverse_lazy('erp:funcionario_list')
        context['form'] = FacturaForm()
        return context
