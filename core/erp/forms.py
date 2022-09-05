from datetime import datetime, date, time
from django.forms import *
from core.erp.models import *
from django.db.models import Q


class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs["autofocus"] = "true"

    class Meta:
        """Meta definition for Clienteform."""

        model = Cliente
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date'
        widgets = {
            'nombre': TextInput(
                attrs={'placeholder': 'Ingrese su Nombre'}
            ),
            'apellido': TextInput(
                attrs={'placeholder': 'Ingrese su Apellido'}
            ),
            'rut': TextInput(
                attrs={'placeholder': 'Ingrese su Rut'}
            ),
            'direccion': TextInput(
                attrs={'placeholder': 'Ingrese su Direccion'}
            ),
            'telefono': TextInput(
                attrs={'placeholder': 'Ingrese su Telefono'}
            ),
            'mail': TextInput(
                attrs={'placeholder': 'Ingrese su Correo'}
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                i = form.save(commit=False)
                i.save()
                data = i.toJSON()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class EstacionamientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["numero_estacionamiento"].widget.attrs["autofocus"] = "true"

    class Meta:
        model = Estacionamiento
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date'
        widgets = {
            "estado_estacionamiento": Select(attrs={
                "class": "form-control select2",
                "style": "width: 100%"
            }),
            "tipo_estacionamiento": Select(attrs={
                "class": "form-control select2",
                "style": "width: 100%"
            }),
            "observacion": Textarea(
                attrs={
                    "placeholder": "ingrese una descripción",
                    "rows": 3,
                    "cols": 3,
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
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class TarifaPlanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs["autofocus"] = "true"

    class Meta:
        model = TarifaPlan
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date'
        labels = {
            "nombre": ""
        }

        widgets = {
            "nombre": TextInput(
                attrs={
                    "placeholder": "Ingrese Nombre de Plan",
                    "hidden": True
                }
            ),
            "precio": TextInput()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class TarifaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs["autofocus"] = "true"

    class Meta:
        model = Tarifa
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date'
        widgets = {
            "nombre": TextInput(
                attrs={
                    "placeholder": "Ingrese Nombre de Tarifa",
                }
            ),
            "precio": TextInput()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = 'tarifa', 'patente', 'fecha_entrada', 'hora_entrada', 'estacionamiento'
        widgets = {

            "estacionamiento": Select(attrs={
                "style": "display:none"
            }),
            "patente": TextInput(attrs={'placeholder': 'Ingrese su Numero de Patente'}),
            "estado_reserva": Select(attrs={
                "class": "form-control",
                "style": "width: 100%"
            }),
            "fecha_entrada": DateInput(
                format="%Y-%m-%d",
                attrs={
                    # "value": date.today().strftime("%Y-%m-%d"),
                    "readonly": True,
                }
            ),
            "hora_entrada": TimeInput(
                format="%H:%M",
                attrs={
                    # "value": timezone.now().strftime("%H:%M %p"),
                    "readonly": True,
                }
            ),
        }

    def clean_patente(self):
        patente = self.cleaned_data['patente']
        reserva = Reserva.objects.filter(estado_reserva='entrada').values_list('patente', flat=True)
        print(reserva)
        if patente in reserva:
            raise forms.ValidationError(f'Esta patente esta en uso <b class="text-red"> {patente} </b>')
        return patente

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()  # me devuelve la instancia del objeto creado( el que se guardo)
                data = instance.toJSON()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class PlanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['estacionamiento'].queryset = Estacionamiento.objects.all().exclude(Q(estado_estacionamiento='reservado') | Q(estado_estacionamiento='ocupado'))
        self.fields['estacionamiento'].queryset = Estacionamiento.objects.filter(
            estado_estacionamiento='disponible')
        # self.fields['estacionamiento'].initial = Estacionamiento.objects.get(id=2)

    class Meta:
        model = Plan
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date'
        widgets = {
            "cliente": Select(attrs={
                "class": "form-select select2",
            }),
            'estado_plan': Select(attrs={
                "style": "display:none"
            }),
            "tarifa_plan": Select(attrs={
                "class": "form-control",
                "style": "width: 100%"
            }),
            "total": TextInput(attrs={
                "class": "form-control",
                "readonly": True,
            }),
            "razon_social": TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Ingrese Razon Social',
            }),
            "estacionamiento": Select(attrs={
                "class": "form-control",
                "style": "width: 100%",
                "style": "display:none"
            }),
            "patente": TextInput(attrs={'placeholder': 'Ingrese su Numero de Patente', "class": "form-control"}),
            "fecha_inicio": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "autocomplete": "off",
                    "class": "form-control datetimepicker-input",
                    "id": "fecha_inicio",
                    "data-target": "#fecha_inicio",
                    "data-toggle": "datetimepicker"
                }
            ),
            "fecha_termino": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "autocomplete": "off",
                    "class": "form-control datetimepicker-input",
                    "id": "fecha_termino",
                    "data-target": "#fecha_termino",
                    "data-toggle": "datetimepicker"
                }
            ),
        }

    def clean_patente(self):
        patente = self.cleaned_data['patente']
        reserva = Reserva.objects.filter(estado_reserva='entrada').values_list('patente', flat=True)
        plan = Plan.objects.filter(estado_plan='iniciado').values_list('patente', flat=True)
        if patente in reserva or patente in plan:
            raise forms.ValidationError(f'Esta patente esta en uso <b class="text-red"> {patente} </b>')
        return patente

    def clean_total(self):
        total = self.cleaned_data['total']
        if total == 0:
            raise forms.ValidationError('El total debe ser superior a 0')
        return total

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()  # me devuelve la instancia del objeto creado( el que se guardo)
                data = instance.toJSON()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class PagoReservaForm(ModelForm):
    class Meta:
        model = PagoReserva
        exclude = 'state', 'created_date', 'modified_date', 'deleted_date', 'estado_pago'
        widgets = {
            "reserva": Select(attrs={
                "style": "display:none"
            }),
            "fecha_entrada": DateInput(
                format="%Y-%m-%d",
                attrs={
                    # "value": date.today().strftime("%Y-%m-%d"),
                    "readonly": True,
                }
            ),
            "hora_entrada": TimeInput(
                format="%H:%M",
                attrs={
                    # "value": timezone.now().strftime("%H:%M %p"),
                    "readonly": True,
                }
            ),
            "fecha_salida": DateInput(
                format="%Y-%m-%d",
                attrs={
                    # "value": date.today().strftime("%Y-%m-%d"),
                    "readonly": True,
                }
            ),
            "hora_salida": TimeInput(
                format="%H:%M",
                attrs={
                    # "value": timezone.now().strftime("%H:%M %p"),
                    "readonly": True,
                }
            ),
            "total": TextInput(attrs={
                "readonly": True,
            }),

            "obs": Textarea(attrs={
                "placeholder": "Ingrese su observación",
                "rows": 3,
                "cols": 3
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class DashboardForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        "style": "width: 75%"
    }))
