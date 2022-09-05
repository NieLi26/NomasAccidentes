from datetime import datetime, date, time
from django.utils import timezone
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse

from django.db.models.signals import post_save

from core.base.models import BaseModel


#---------------------- Estacionamiento-------------------------#

class Estacionamiento(BaseModel):
    """Model definition for Estacionamiento."""
    estado_choices = {
        ('ocupado', 'Ocupado'),
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('mantenimiento', 'Mantenimiento'),
    }

    tipo_choices = {
        ('normal', 'Normal'),
        ('discapacitado', 'Discapacitado')
    }

    numero_estacionamiento = models.PositiveBigIntegerField(
        verbose_name='Numero Estacionamiento')
    estado_estacionamiento = models.CharField(
        'Estado', max_length=50, choices=estado_choices, default='disponible')
    tipo_estacionamiento = models.CharField(
        'Tipo', max_length=50, choices=tipo_choices, default='normal')

    class Meta:
        """Meta definition for Estacionamiento."""

        verbose_name = 'Estacionamiento'
        verbose_name_plural = 'Estacionamientos'
        ordering = ['numero_estacionamiento']
        db_table = 'estacionamiento'

    def __str__(self):
        """Unicode representation of Estacionamiento."""
        return str(self.numero_estacionamiento)

    def toJSON(self):
        item = model_to_dict(self)
        return item


#---------------------- Tarifa-------------------------#

class Tarifa(BaseModel):
    """Model definition for Tarifa."""

    nombre = models.CharField('Nombre', max_length=150)
    precio = models.PositiveIntegerField('Precio', default=0)

    class Meta:
        """Meta definition for Tarifa."""

        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        ordering = ['id']
        db_table = 'tarifa'

    def __str__(self):
        return self.nombre

    @property
    def get_update_url(self):
        return reverse('erp:tarifa_update', kwargs={'pk': self.pk})

    @property
    def get_delete_url(self):
        return reverse('erp:tarifa_delete', kwargs={'pk': self.pk})

    def toJSON(self):
        item = model_to_dict(self)
        item['update_url'] = self.get_update_url
        item['delete_url'] = self.get_delete_url
        return item

#---------------------- Reserva-------------------------#


class Reserva(BaseModel):

    estado_reserva_choices = (
        # ('sin confirmar', 'Sin Confirmar'),
        # ('reservado', 'Reservado'),
        ('entrada', 'Entrada'),
        ('reserva terminada', 'Reserva Terminada'),
        ('pago pendiente', 'Pago Pendiente'),
        ('reserva anulada', 'Reserva Anulada'),
    )

    # cliente = models.ForeignKey(
    #     Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True)
    estacionamiento = models.ForeignKey(
        Estacionamiento, on_delete=models.CASCADE, verbose_name="Estacionamiento")
    estado_reserva = models.CharField(
        max_length=25, choices=estado_reserva_choices, default="entrada", verbose_name="Estado de Reserva")
    tarifa = models.ForeignKey(
        Tarifa, on_delete=models.CASCADE, verbose_name='Tarifa', default='normal')
    patente = models.CharField('Patente', max_length=15)
    abono = models.PositiveIntegerField(
        default=0, verbose_name="Abono", blank=True, null=True)
    total = models.PositiveIntegerField(
        default=0, verbose_name="Total a pagar", null=True, blank=True)
    fecha_entrada = models.DateField(
        default=date.today, verbose_name="Fecha de Entrada")
    hora_entrada = models.TimeField(
        default=datetime.now, verbose_name="Hora de Entrada")
    fecha_salida = models.DateField(
        verbose_name="Fecha de Salida", null=True, blank=True)
    hora_salida = models.TimeField(
        verbose_name="Hora de Salida", null=True, blank=True)

    def __str__(self):
        return f'{self.patente}'

    def toJSON(self):
        item = model_to_dict(self)
        # if item['cliente']:
        #     item['cliente'] = self.cliente.toJSON()
        item['estacionamiento'] = self.estacionamiento.toJSON()
        item['tarifa'] = self.tarifa.toJSON()
        item['fecha_entrada'] = self.fecha_entrada.strftime('%Y-%m-%d')
        if item['fecha_salida']:
            item['fecha_salida'] = self.fecha_salida.strftime('%Y-%m-%d')
        item['hora_entrada'] = self.hora_entrada.strftime('%H:%M %p')
        if item['hora_salida']:
            item['hora_salida'] = self.hora_salida.strftime('%H:%M %p')

        return item

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["id"]
        db_table = 'reserva'


def reserva_save(sender, instance, **kwargs):
    estacionamiento = Estacionamiento.objects.filter(
        id=instance.estacionamiento_id)
    pago = PagoReserva.objects.filter(reserva=instance)
    if instance.estado_reserva == "entrada":
        estacionamiento.update(estado_estacionamiento="ocupado")
    if instance.estado_reserva == "reserva anulada":
        estacionamiento.update(estado_estacionamiento="disponible")
        pago.update(estado_pago='revisado')
    if instance.estado_reserva == "reserva terminada":
        estacionamiento.update(estado_estacionamiento="disponible")


post_save.connect(reserva_save, sender=Reserva)


class PagoReserva(BaseModel):

    estado_pago_reserva_diaria_choices = (
        ('cancelado', 'Cancelado'),
        ('anulado', 'Anulado'),
        ('revisado', 'Revisado'),
    )

    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, verbose_name="Reserva", related_name='reservita')
    numero_boleta = models.PositiveIntegerField(verbose_name='Nro Boleta')
    fecha_entrada = models.DateField(
        verbose_name="Fecha de Entrada", blank=True, null=True)
    hora_entrada = models.TimeField(
        verbose_name="Hora de Entrada", blank=True, null=True)
    fecha_salida = models.DateField(
        verbose_name="Fecha de Salida", null=True, blank=True)
    hora_salida = models.TimeField(
        verbose_name="Hora de Salida", null=True, blank=True)
    total = models.PositiveIntegerField(default=0, verbose_name="Valor total")
    obs = models.TextField(
        max_length=200, verbose_name="Observacion", blank=True, null=True)
    estado_pago = models.CharField(
        max_length=25, choices=estado_pago_reserva_diaria_choices, default="pendiente", verbose_name="Estado de Pago")

    def __str__(self):
        return str(self.reserva)

    def toJSON(self):
        item = model_to_dict(self)
        item['reserva'] = self.reserva.toJSON()
        item['fecha_entrada'] = self.fecha_entrada.strftime('%Y-%m-%d')
        item['fecha_salida'] = self.fecha_salida.strftime('%Y-%m-%d')
        item['hora_entrada'] = self.hora_entrada.strftime('%H:%M %p')
        item['hora_salida'] = self.hora_salida.strftime('%H:%M %p')
        return item

    class Meta:
        verbose_name = "Pago Reserva"
        verbose_name_plural = "Pagos Reservas"
        ordering = ["id"]
        db_table = 'pago_reserva'


def pago_save(sender, instance, **kwargs):
    reserva = Reserva.objects.get(id=instance.reserva.id)
    pago = PagoReserva.objects.filter(id=instance.id)
    if reserva.estado_reserva == "entrada":
        pago.update(estado_pago='cancelado')
        reserva.estado_reserva = "reserva terminada"
        reserva.save()
    if reserva.estado_reserva == "pago pendiente":
        pago.update(estado_pago='anulado')


post_save.connect(pago_save, sender=PagoReserva)


############################################################### PLAN ######################################################

#---------------------- TarifaPlan-------------------------#

class TarifaPlan(BaseModel):
    """Model definition for Tarifa."""

    nombre = models.CharField('Nombre', max_length=150)
    precio = models.PositiveIntegerField('Precio', default=0)

    class Meta:
        """Meta definition for Tarifa."""

        verbose_name = 'Tarifa Plan'
        verbose_name_plural = 'Tarifas de Planes'
        ordering = ['id']
        db_table = 'tarifa_plan'

    def __str__(self):
        return self.nombre

    @property
    def get_update_url(self):
        return reverse('erp:tarifa_plan_update', kwargs={'pk': self.pk})

    @property
    def get_delete_url(self):
        return reverse('erp:tarifa_plan_delete', kwargs={'pk': self.pk})

    def toJSON(self):
        item = model_to_dict(self)
        item['update_url'] = self.get_update_url
        item['delete_url'] = self.get_delete_url
        return item

# ---------------------- CLIENTE ------------------------


class Cliente(BaseModel):

    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    apellido = models.CharField(max_length=255, verbose_name="Apellido")
    rut = models.CharField(max_length=10, verbose_name="Rut")
    razon_social = models.CharField(
        'Razón Social', max_length=50, null=True, blank=True)
    direccion = models.CharField('Dirección', max_length=150)
    telefono = models.PositiveIntegerField(verbose_name="Telefono")
    mail = models.EmailField(max_length=30, verbose_name="Correo")

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
        db_table = 'cliente'

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f'{self.nombre} {self.apellido} / {self.rut}'

    @property
    def get_update_url(self):
        return reverse('erp:cliente_update', kwargs={'pk': self.pk})

    @property
    def get_delete_url(self):
        return reverse('erp:cliente_delete', kwargs={'pk': self.pk})

    def toJSON(self):
        item = model_to_dict(self)
        item['get_full_name'] = self.get_full_name
        item['update_url'] = self.get_update_url
        item['delete_url'] = self.get_delete_url
        return item

# ---------------------- CLIENTE ------------------------


class Plan(BaseModel):

    estado_plan_choices = (
        ('iniciado', 'Iniciado'),
        ('terminado', 'Terminado'),
    )

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    estacionamiento = models.ForeignKey(
        Estacionamiento, on_delete=models.CASCADE, verbose_name="Estacionamiento")
    estado_plan = models.CharField(
        max_length=25, choices=estado_plan_choices, default="iniciado", verbose_name="Estado de Plan")
    tarifa_plan = models.ForeignKey(
        TarifaPlan, on_delete=models.CASCADE, verbose_name='Tarifa Plan', default='mensual')
    patente = models.CharField('Patente', max_length=15)
    # abono = models.PositiveIntegerField(
    #     default=0, verbose_name="Abono", blank=True, null=True)
    total = models.PositiveIntegerField(
        default=0, verbose_name="Total a pagar", null=True, blank=True)
    fecha_inicio = models.DateField(
        default=date.today, verbose_name="Fecha de Inicio")
    fecha_termino = models.DateField(
        default=date.today, verbose_name="Fecha de Termino", null=True, blank=True)

    def __str__(self):
        return f'{self.patente}'

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['estacionamiento'] = self.estacionamiento.toJSON()
        item['tarifa_plan'] = self.tarifa_plan.toJSON()
        item['fecha_inicio'] = self.fecha_inicio.strftime('%Y-%m-%d')
        item['fecha_termino'] = self.fecha_termino.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"
        ordering = ["id"]
        db_table = 'plan'


def plan_save(sender, instance, **kwargs):
    estacionamiento = Estacionamiento.objects.filter(
        id=instance.estacionamiento_id)
    if instance.estado_plan == "iniciado":
        estacionamiento.update(estado_estacionamiento="reservado")
    if instance.estado_plan == "terminado":
        estacionamiento.update(estado_estacionamiento="disponible")


post_save.connect(plan_save, sender=Plan)
