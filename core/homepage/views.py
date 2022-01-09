from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse, HttpResponseRedirect
from core.erp.forms import ContactoForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.models import Contacto


class IndexView(TemplateView):
    template_name = 'index.html'
    # success_url = reverse_lazy("{% url 'index' %}")
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                con = Contacto()
                con.nombre = request.POST['nombre']
                con.correo = request.POST['correo']
                con.asunto = request.POST['asunto']
                con.mensaje = request.POST['mensaje']
                con.save()
                return HttpResponseRedirect("http://127.0.0.1:8000/")
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Creación de una Visita'
        # context['entity'] = 'Visitas'
        # context['list_url'] = return HttpResponseRedirect
        context['action'] = 'add'
        context['form'] = ContactoForm()
        return context
    
