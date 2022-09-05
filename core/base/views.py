from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def page_not_found404(request, exception):
    return render(request, '404.html')

# def server_errord500(request, exception):
#     return render(request, '404.html')


# class Error505View(TemplateView):
#     template_name = "500.html"

#     @classmethod
#     def as_error_view(cls):

#         v = cls.as_view()
#         def view(request):
#             r = v(request)
#             r.render()
#             return r
#         return view
