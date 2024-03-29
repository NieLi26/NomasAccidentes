# Generated by Django 4.0.1 on 2022-09-05 21:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=255, verbose_name='Apellido')),
                ('rut', models.CharField(max_length=10, verbose_name='Rut')),
                ('razon_social', models.CharField(blank=True, max_length=50, null=True, verbose_name='Razón Social')),
                ('direccion', models.CharField(max_length=150, verbose_name='Dirección')),
                ('telefono', models.PositiveIntegerField(verbose_name='Telefono')),
                ('mail', models.EmailField(max_length=30, verbose_name='Correo')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('numero_estacionamiento', models.PositiveBigIntegerField(verbose_name='Numero Estacionamiento')),
                ('estado_estacionamiento', models.CharField(choices=[('reservado', 'Reservado'), ('ocupado', 'Ocupado'), ('mantenimiento', 'Mantenimiento'), ('disponible', 'Disponible')], default='disponible', max_length=50, verbose_name='Estado')),
                ('tipo_estacionamiento', models.CharField(choices=[('normal', 'Normal'), ('discapacitado', 'Discapacitado')], default='normal', max_length=50, verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Estacionamiento',
                'verbose_name_plural': 'Estacionamientos',
                'db_table': 'estacionamiento',
                'ordering': ['numero_estacionamiento'],
            },
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('precio', models.PositiveIntegerField(default=0, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Tarifa',
                'verbose_name_plural': 'Tarifas',
                'db_table': 'tarifa',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TarifaPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('precio', models.PositiveIntegerField(default=0, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Tarifa Plan',
                'verbose_name_plural': 'Tarifas de Planes',
                'db_table': 'tarifa_plan',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('estado_reserva', models.CharField(choices=[('entrada', 'Entrada'), ('reserva terminada', 'Reserva Terminada'), ('pago pendiente', 'Pago Pendiente'), ('reserva anulada', 'Reserva Anulada')], default='entrada', max_length=25, verbose_name='Estado de Reserva')),
                ('patente', models.CharField(max_length=15, verbose_name='Patente')),
                ('abono', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Abono')),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total a pagar')),
                ('fecha_entrada', models.DateField(default=datetime.date.today, verbose_name='Fecha de Entrada')),
                ('hora_entrada', models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Entrada')),
                ('fecha_salida', models.DateField(blank=True, null=True, verbose_name='Fecha de Salida')),
                ('hora_salida', models.TimeField(blank=True, null=True, verbose_name='Hora de Salida')),
                ('estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.estacionamiento', verbose_name='Estacionamiento')),
                ('tarifa', models.ForeignKey(default='normal', on_delete=django.db.models.deletion.CASCADE, to='erp.tarifa', verbose_name='Tarifa')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'db_table': 'reserva',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('estado_plan', models.CharField(choices=[('iniciado', 'Iniciado'), ('terminado', 'Terminado')], default='iniciado', max_length=25, verbose_name='Estado de Plan')),
                ('patente', models.CharField(max_length=15, verbose_name='Patente')),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total a pagar')),
                ('fecha_inicio', models.DateField(default=datetime.date.today, verbose_name='Fecha de Inicio')),
                ('fecha_termino', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Fecha de Termino')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cliente', verbose_name='Cliente')),
                ('estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.estacionamiento', verbose_name='Estacionamiento')),
                ('tarifa_plan', models.ForeignKey(default='mensual', on_delete=django.db.models.deletion.CASCADE, to='erp.tarifaplan', verbose_name='Tarifa Plan')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
                'db_table': 'plan',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PagoReserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('numero_boleta', models.PositiveIntegerField(verbose_name='Nro Boleta')),
                ('fecha_entrada', models.DateField(blank=True, null=True, verbose_name='Fecha de Entrada')),
                ('hora_entrada', models.TimeField(blank=True, null=True, verbose_name='Hora de Entrada')),
                ('fecha_salida', models.DateField(blank=True, null=True, verbose_name='Fecha de Salida')),
                ('hora_salida', models.TimeField(blank=True, null=True, verbose_name='Hora de Salida')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='Valor total')),
                ('obs', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observacion')),
                ('estado_pago', models.CharField(choices=[('cancelado', 'Cancelado'), ('anulado', 'Anulado'), ('revisado', 'Revisado')], default='pendiente', max_length=25, verbose_name='Estado de Pago')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservita', to='erp.reserva', verbose_name='Reserva')),
            ],
            options={
                'verbose_name': 'Pago Reserva',
                'verbose_name_plural': 'Pagos Reservas',
                'db_table': 'pago_reserva',
                'ordering': ['id'],
            },
        ),
    ]
