from django.contrib import admin
from core.erp.models import *

# Register your models here.

######## INTERFAZ ADMIN ########
admin.site.register(Reserva)
admin.site.register(Estacionamiento)
admin.site.register(Tarifa)
admin.site.register(Cliente)
admin.site.register(PagoReserva)
admin.site.register(Plan)


