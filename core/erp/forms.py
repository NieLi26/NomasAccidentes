from datetime import datetime
from django.forms import *
from django import forms
from django.forms import ModelForm, Form

from core.erp.models import *

############################################################################################################################
########################################################### MI APP #########################################################
############################################################################################################################

################################################ FUNCIONARIOS #########################################


class FuncionarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Funcionario
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Nombre',
                }
            ),
            'rut': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Rut',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Dirección',
                }
            ),
            'cell': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Numero',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

################################################ CLIENTES #############################################


class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese Nombre Empresa',
                }
            ),
            'rubro': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Rubro',
                }
            ),
            'rut': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Rut',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Dirección',
                }
            ),
            'cell': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Numero',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

################################################ CONTRATO #############################################


class ContratoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['emp'].widget.attrs['autofocus'] = True

    class Meta:
        model = Contrato
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'emp': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'fecha_termino': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_termino',
                    'data-target': '#fecha_termino',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# ###################################################### ACTIVIDADES ######################################################


class ActividadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Actividad
        fields = '__all__'
        widgets = {
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese Descripcion',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# --------------CAPACITACIONES-------------


class CapacitacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Empresa.objects.all()

    class Meta:
        model = Capacitacion
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'act': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'mat': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'horario': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'plan': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su Planificacion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'fecha_realizacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_realizacion',
                    'data-target': '#fecha_realizacion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'completado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# -------------------VISITA---------------------


class VisitaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Empresa.objects.all()

    class Meta:
        model = Visita
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'act': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'func': forms.Select(
                attrs={
                    'class': 'select2',
                    # 'style': 'width: 100%'
                }
            ),
            'ch': forms.Select(
                attrs={
                    'class': 'select2',
                    # 'style': 'width: 100%'
                }
            ),
            'fecha_realizacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_realizacion',
                    'data-target': '#fecha_realizacion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'horario': forms.Select(
                attrs={
                    'class': 'select2',
                    # 'style': 'width: 100%'
                }
            ),
            'plan': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su Planificacion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'sugerencia': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su Planificacion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'completado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CheckListForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['text'].widget.attrs['autofocus'] = True

    class Meta:
        model = CheckList
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# ----------------------- ASESORIA -----------------------

class AsesoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Empresa.objects.all()

    class Meta:
        model = Asesoria
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'act': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'func': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'tipo': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'fecha_realizacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_realizacion',
                    'data-target': '#fecha_realizacion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'inf': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese la Informacion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'completado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# ------------------------ ASESORIA ESPECIAL --------------


class AsesoriaEspecialForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Empresa.objects.all()

    class Meta:
        model = AsesoriaEspecial
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'act': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'tipo': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'fecha_realizacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_realizacion',
                    'data-target': '#fecha_realizacion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'inf': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese la Informacion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'completado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# FISCALIZACIONES


class CasoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ase'].queryset = Empresa.objects.all()

    class Meta:
        model = Caso
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'ase': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'tipo': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'fecha_realizacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_realizacion',
                    'data-target': '#fecha_realizacion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'resultado': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su Resultado',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'completado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# PAGO
class PagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Empresa.objects.all()

    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'fecha_expiracion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_expiracion',
                    'data-target': '#fecha_expiracion',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su Descripcion',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'cumplido': forms.CheckboxInput(
                attrs={
                    'style': 'width: 5%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# FISCALIZACIONES O ACCIDENTES(cliente)


class AccidenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ase'].queryset = Empresa.objects.all()

    class Meta:
        model = Accidente
        fields = '__all__'
        exclude = ['fecha_creacion', 'nombre', 'correo']
        # widgets = {
        #     'desc': forms.Textarea(
        #         attrs={
        #             'placeholder': 'Ingrese Descripcion',
        #             'rows': 3,
        #             'cols': 3
        #         })
        # }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# CONTACTO

class ContactoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ase'].queryset = Empresa.objects.all()

    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'mensaje': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese su mensaje',
                    'rows': 3,
                    'cols': 3
                })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Report

class FacturaForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
