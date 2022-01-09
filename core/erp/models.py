from datetime import datetime

from django.db import models
from django.db.models import Sum, F
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import *
from django.contrib.auth import get_user_model

User = get_user_model()

############################################################################################################################
########################################################### MI APP #########################################################
############################################################################################################################

################################################ FUNCIONARIOS #########################################


class Profesion(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Profesion'
        verbose_name_plural = 'Profesiones'
        ordering = ['id']


class Funcionario(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    profesion = models.ForeignKey(
        Profesion, on_delete=models.CASCADE, verbose_name='Profesion', null=True)
    rut = models.CharField(max_length=10, unique=True, verbose_name='Rut')
    address = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Dirección')
    cell = models.CharField(max_length=9, unique=True, verbose_name='Telefono')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / {}'.format(self.names, self.profesion.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['profesion'] = self.profesion.toJSON()
        return item

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['id']


################################################ CLIENTES #############################################

class Empresa(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    rubro = models.CharField(max_length=150, verbose_name='Rubro')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    func = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name='Funcionario Asignado', null=True)
    rut = models.CharField(max_length=10, unique=True, verbose_name='Rut')
    address = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Dirección')
    cell = models.CharField(max_length=9, unique=True, verbose_name='Telefono')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / {}'.format(self.name, self.rut)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['user'] = self.user.toJSON()
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['id']

################################################ CONTRATO #############################################

# (plan A,B,C,ETC)


class Contrato(models.Model):
    contrato_choices = (
        ('nuevo', 'Nuevo'),
        ('renovado', 'Renovado'),
    )
    emp = models.OneToOneField(
        Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=False, blank=False)
    estado = models.CharField(max_length=10, choices=contrato_choices,
                              default='Nuevo', verbose_name='Estado')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_termino = models.DateField(
        default=datetime.now, verbose_name='Fecha Termino')
    activo = models.BooleanField(default=True, verbose_name='Vigente')

    def __str__(self):
        return self.emp.name

    def toJSON(self):
        item = model_to_dict(self)
        item['emp'] = self.emp.toJSON()
        item['fecha_inicio'] = self.estado
        return item

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['id']

# (faltan datos)


class Pago(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    asunto = models.CharField(
        max_length=50, verbose_name='Asunto', blank=False)
    desc = models.TextField(
        max_length=500, verbose_name='Descripcion', blank=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField(default=datetime.now,
                                        verbose_name='Fecha Expiracion')
    valor = models.IntegerField(default=0, verbose_name='Valor')
    cumplido = models.BooleanField(
        default=False, verbose_name='¿Pago Realizado?')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        return item

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['id']

# ###################################################### ACTIVIDADES ######################################################


class Actividad(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    precio = models.IntegerField(default=0, verbose_name='Precio', blank=True)
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['id']


class Horario(models.Model):
    hora = models.CharField(max_length=50, verbose_name='Hora')

    def __str__(self):
        return self.hora

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['id']

# --------------CAPACITACIONES-------------
# (A,B,C,ETC)


class Material(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['id']


class Capacitacion(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Cliente')
    act = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    func = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name='Funcionario', null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    mat = models.ForeignKey(
        Material, on_delete=models.CASCADE, verbose_name='Material')
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, verbose_name='Horario')
    asist = models.IntegerField(default=0, verbose_name='Asistentes')
    plan = models.TextField(max_length=400, verbose_name='Planificacion')
    fecha_realizacion = models.DateField(default=datetime.now,
                                         verbose_name='Fecha de Realizacion')
    completado = models.BooleanField(default=False, verbose_name='Realizado')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['mat'] = self.mat.toJSON()
        item['func'] = self.func.toJSON()
        item['horario'] = self.horario.toJSON()
        return item

    class Meta:
        verbose_name = 'Capacitacion'
        verbose_name_plural = 'Capacitaciones'
        ordering = ['id']


# -------------------VISITA---------------------
# (fiscalización, accidente, revisión, capacitación)

# class TipoVisita(models.Model):
#     nombre = models.CharField(max_length=50, verbose_name='Nombre')
#     desc = models.TextField(verbose_name='Descripcion')

#     def __str__(self):
#         return self.nombre

#     def toJSON(self):
#         item = model_to_dict(self)
#         return item

#     class Meta:
#         verbose_name = 'TipoVisita'
#         verbose_name_plural = 'TiposVista'
#         ordering = ['id']

class CheckList(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    fecha_creacion = models.DateField(auto_now_add=True)
    primera = models.CharField(max_length=50, verbose_name='1')
    segunda = models.CharField(max_length=50, verbose_name='2')
    tercera = models.CharField(max_length=50, verbose_name='3')
    cuarta = models.CharField(max_length=50, verbose_name='4')
    quinta = models.CharField(max_length=50, verbose_name='5')
    sexta = models.CharField(max_length=50, verbose_name='6')
    septima = models.CharField(max_length=50, verbose_name='7')
    octaba = models.CharField(max_length=50, verbose_name='8')
    novena = models.CharField(max_length=50, verbose_name='9')
    decima = models.CharField(max_length=50, verbose_name='10')
    # sugerencia = models.TextField(
    #     max_length=500, verbose_name='Sugerencia', blank=True)
    # complete = models.BooleanField(default=False, verbose_name='Completado')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['fecha_creacion'] = self.fecha_creacion.strftime(
            '%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'CheckList'
        verbose_name_plural = 'CheckLists'
        ordering = ['id']


class Visita(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Cliente')
    act = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    func = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name='Encargado')
    ch = models.ForeignKey(
        CheckList, on_delete=models.CASCADE, verbose_name='CheckList')
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, verbose_name='Horario')
    fecha_creacion = models.DateField(auto_now_add=True)
    plan = models.TextField(max_length=400, verbose_name='Planificacion')
    fecha_realizacion = models.DateField(default=datetime.now,
                                         verbose_name='Fecha de Realizacion')
    sugerencia = models.TextField(
        max_length=500, verbose_name='Sugerencia', blank=True)
    completado = models.BooleanField(default=False, verbose_name='Realizado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} / ({})'.format(self.cli.name, self.fecha_realizacion)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['act'] = self.act.toJSON()
        item['cli'] = self.cli.toJSON()
        item['func'] = self.func.toJSON()
        item['horario'] = self.horario.toJSON()
        return item

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['id']



# ----------------------- ASESORIA -----------------------
# (asesorar el cumplimiento que necesita la empresa)


class TipoAsesoria(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoVisita'
        verbose_name_plural = 'TiposVista'
        ordering = ['id']


class Asesoria(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Cliente')
    act = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    fecha_creacion = models.DateField(auto_now_add=True)
    func = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name='Funcionario', null=True)
    tipo = models.ForeignKey(
        TipoAsesoria, on_delete=models.CASCADE, verbose_name='Tipo')
    fecha_realizacion = models.DateField(default=datetime.now,
                                         verbose_name='Fecha de Realizacion', null=True)
    inf = models.TextField(max_length=500, verbose_name='Informacion')
    completado = models.BooleanField(default=False, verbose_name='Realizado')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['act'] = self.act.toJSON()
        item['func'] = self.func.toJSON()
        item['tipo'] = self.tipo.toJSON()
        return item

    class Meta:
        verbose_name = 'Asesoria'
        verbose_name_plural = 'Asesorias'
        ordering = ['id']

# ----------------------- ASESORIA ESPECIAL-----------------------
# (fiscalizacion, accidente)


class TipoAsesoriaEspecial(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoVisita'
        verbose_name_plural = 'TiposVista'
        ordering = ['id']


class AsesoriaEspecial(models.Model):
    cli = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name='Cliente')
    act = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    func = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, verbose_name='Funcionario', null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    tipo = models.ForeignKey(
        TipoAsesoriaEspecial, on_delete=models.CASCADE, verbose_name='Tipo')
    fecha_realizacion = models.DateField(default=datetime.now,
                                         verbose_name='Fecha de Realizacion', null=True)
    inf = models.TextField(max_length=500, verbose_name='Informacion')
    completado = models.BooleanField(default=False, verbose_name='Realizado')

    def get_full_name(self):
        return '{} [ {} ] / {} '.format(self.cli.name, self.tipo, self.fecha_realizacion)
    
    def get_full_name_cli(self):
        return '[ {} ]'.format(self.tipo)

    def __str__(self):
        return self.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['full_name_cli'] = self.get_full_name_cli()
        item['act'] = self.act.toJSON()
        item['func'] = self.func.toJSON()
        item['cli'] = self.cli.toJSON()
        item['tipo'] = self.tipo.toJSON()
        # item['completado'] = self.completado.str((True, 'Yes'), (False, 'No'))
        return item

    class Meta:
        verbose_name = 'AsesoriaEspecial'
        verbose_name_plural = 'AsesoriasEspeciales'
        ordering = ['id']


# (conversaciones, correspondencias, diligencias, juicios)
class TipoCaso(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    desc = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoCaso'
        verbose_name_plural = 'TipoCasos'
        ordering = ['id']


# (solo ante fiscalizaciones)
class Caso(models.Model):
    ase = models.ForeignKey(
        AsesoriaEspecial, on_delete=models.CASCADE, verbose_name='Empresa')
    tipo = models.ForeignKey(
        TipoCaso, on_delete=models.CASCADE, verbose_name='Tipo')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_realizacion = models.DateField(default=datetime.now,
                                         verbose_name='Fecha de Realizacion')
    resultado = models.TextField(
        max_length=500, verbose_name='Resultado', blank=True)
    completado = models.BooleanField(default=False, verbose_name='Concluido')

    def __str__(self):
        return self.ase.cli

    def toJSON(self):
        item = model_to_dict(self)
        item['ase'] = self.ase.toJSON()
        item['tipo'] = self.tipo.toJSON()
        return item

    class Meta:
        verbose_name = 'Caso'
        verbose_name_plural = 'Casos'
        ordering = ['id']

# ENTIDAD GESTIONES

# ----------------------- ACCIDENTE----------------------


class Accidente(models.Model):
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre Empresa')
    # asunto = models.CharField(max_length=50, verbose_name='Asunto')
    # desc = models.TextField(max_length=500, verbose_name='Descripcion')
    correo = models.CharField(max_length=50, verbose_name='Correo')
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha Creacion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        # item['user'] = self.user.toJSON()
        # item['correo'] = self.correo.toJSON()
        item['fecha_creacion'] = self.fecha_creacion.strftime(
            '%Y-%m-%d / %X')
        return item

    class Meta:
        verbose_name = 'Accidente'
        verbose_name_plural = 'Accidentes'
        ordering = ['id']


class Contacto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    correo = models.EmailField(max_length=50, verbose_name='Correo')
    asunto = models.CharField(max_length=50, verbose_name='Asunto')
    mensaje = models.TextField(max_length=500, verbose_name='Mensaje')
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha Creacion')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_creacion'] = self.fecha_creacion.strftime(
            '%Y-%m-%d / %X')
        return item

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['id']
# ----------------------- REPORTE----------------------

# class Report(models.Model):
#     report_choices=(
#         ('nuevo', 'Nuevo'),
#         ('actualizado', 'Actualizado'),
#     )

#     cli=models.ForeignKey(
#         Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
#     estado=models.CharField(max_length=15, choices=report_choices,
#                               default='Nuevo', verbose_name='Estado')
#     fecha_creacion=models.DateField(auto_now_add=True)
#     inf_act=models.TextField(
#         max_length=500, verbose_name='Actividades', blank=False)
#     inf_ext=models.TextField(
#         max_length=500, verbose_name='Extras', blank=False)
#     mejora=models.TextField(
#         max_length=500, verbose_name='Mejoras', blank=False)
#     cant_acc=models.IntegerField(
#         default=0, verbose_name='Cantidad Accidentes')
#     cant_cap=models.IntegerField(
#         default=0, verbose_name='Cantidad Capacitaciones')

#     def __str__(self):
#         return self.cli.name

#     def toJSON(self):
#         item=model_to_dict(self)
#         item['cli']=self.cli.toJSON()
#         item['estado']=self.estado.toJSON()
#         item['cant_acc']=self.cant_acc.toJSON()
#         item['cant_cap']=self.cant_cap.toJSON()
#         return item

#     class Meta:
#         verbose_name='Report'
#         verbose_name_plural='Reports'
#         ordering=['id']


# class Contacto(models.Model):
#     nombre = models.CharField(max_length=50, verbose_name='Nombre Empresa')
#     asunto = models.CharField(
#         max_length=20, choices=contacto_choices, default='-----------', verbose_name='Asunto')
#     desc = models.TextField(verbose_name='Descripcion')

#     def __str__(self):
#         return self.nombre

#     def toJSON(self):
#         item = model_to_dict(self)
#         return item

#     class Meta:
#         verbose_name = 'Contacto'
#         verbose_name_plural = 'Contactos'
#         ordering = ['id']


# ############################################### VA QUEDANDO ################################


# class Notificacion(models.Model):
#     cli = models.ForeignKey(
#         Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
#     fecha_creacion = models.DateField(auto_now_add=True)
#     tipo = models.CharField(
#         max_length=10, choices=notificacion_choices, default='pago', verbose_name='Tipo')
#     fecha_caducidad = models.DateField(default=datetime.now,
#                                        verbose_name='Fecha_Caducidad')
#     pendiente = models.BooleanField(default=True, verbose_name='Pendiente')

#     def __str__(self):
#         return self.cli.name

#     def toJSON(self):
#         item = model_to_dict(self)
#         item['cli'] = self.cli.name.toJSON()
#         return item

#     class Meta:
#         verbose_name = 'Notificacion'
#         verbose_name_plural = 'Notificaciones'
#         ordering = ['id']
