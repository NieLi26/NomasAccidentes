from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.user.forms import UserForm, UserProfileForm
from notifications.models import Notification 



class NotificationListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/list.html'
    permission_required = 'view_notification'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Notification.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Notificaciones'
        context['create_url'] = reverse_lazy('user:user_notification')
        context['list_url'] = reverse_lazy('user:user_notification')
        context['entity'] = 'Notificaciones'
        return context


# class NotificationCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
#     model = User
#     form_class = UserForm
#     template_name = 'user/create.html'
#     success_url = reverse_lazy('user:user_list')
#     permission_required = 'add_user'
#     url_redirect = success_url

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Creación de un Usuario'
#         context['entity'] = 'Usuarios'
#         context['list_url'] = self.success_url
#         context['action'] = 'add'
#         return context


# class NotificationUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
#     model = User
#     form_class = UserForm
#     template_name = 'user/create.html'
#     success_url = reverse_lazy('user:user_list')
#     permission_required = 'change_user'
#     url_redirect = success_url

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edición de un Usuario'
#         context['entity'] = 'Usuarios'
#         context['list_url'] = self.success_url
#         context['action'] = 'edit'
#         return context


class NotificationDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Notification
    template_name = 'notification/delete.html'
    success_url = reverse_lazy('user:notification_list')
    permission_required = 'delete_notification'
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
        context['title'] = 'Eliminación de una Notificacion'
        context['entity'] = 'Notificaciones'
        context['list_url'] = self.success_url
        return context

