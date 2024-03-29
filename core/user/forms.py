from django.forms import *
from core.user.models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autofocus"] = "true"

    class Meta:
        model = User
        fields = 'first_name', 'last_name','rut', 'telefono', 'email', 'turno', 'username', 'password', 'image', 'groups'
        widgets = {
            "first_name": TextInput(attrs={
                "placeholder": "Ingrese sus nombres"
            }),
            "last_name": TextInput(attrs={
                "placeholder": "Ingrese sus apellidos"
            }),
            "rut": TextInput(attrs={
                "placeholder": "Ingrese su rut"
            }),
            "email": TextInput(attrs={
                "placeholder": "Ingrese su email"
            }),
            "turno": Select(attrs={
                "class": "form-control",
                "style": "width: 100%"
            }),
            "username": TextInput(attrs={
                "placeholder": "Ingrese su username"
            }),
            "password": PasswordInput(render_value=True,
                attrs={
                    "placeholder": "Ingrese su password"
                }),
            "groups": SelectMultiple(attrs={
                "class": "form-control select2",
                "style": "width: 100%",
                "multiple": "multiple"
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # metodo para extraer los datos de un componente, se usa despues del que el form sea valido
                pwd = self.cleaned_data["password"]
                # hace una pausa al guardado del objecto y devuelve el objecto actual
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data["groups"]:
                    u.groups.add(g)
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autofocus"] = "true"

    class Meta:
        model = User
        fields = 'first_name', 'last_name','rut', 'email', 'username', 'password'
        widgets = {
            "first_name": TextInput(attrs={
                "placeholder": "Ingrese sus nombres"
            }),
            "last_name": TextInput(attrs={
                "placeholder": "Ingrese sus apellidos"
            }),
            "rut": TextInput(attrs={
                "placeholder": "Ingrese su rut"
            }),
            "numero_documento": TextInput(attrs={
                "placeholder": "Ingrese su numero de documento"
            }),
            "email": TextInput(attrs={
                "placeholder": "Ingrese su email"
            }),
            "username": TextInput(attrs={
                "placeholder": "Ingrese su username"
            }),
            "password": PasswordInput(render_value=True,
                attrs={
                    "placeholder": "Ingrese su password"
                }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data["password"]
                # hace una pausa al guardado del objecto y devuelve el objecto actual
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                data = u.toJSON()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data