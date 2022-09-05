from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from core.base.views import page_not_found404

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('login/', LoginFormView.as_view()),
    path('', include('core.login.urls')),
    path('admin/', admin.site.urls),
    path('erp/', include('core.erp.urls')),
    path('reports/', include('core.reports.urls')),
    path('user/', include('core.user.urls')),
]   

handler404 = page_not_found404
# handler404 = Error505View.as_error_view()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
