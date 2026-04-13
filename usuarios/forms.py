from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PerfilUsuario


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        max_length=100, label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.cl'})
    )
    rut = forms.CharField(
        max_length=12, label='RUT',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'})
    )
    telefono = forms.CharField(
        max_length=20, label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )
    direccion = forms.CharField(
        max_length=300, label='Dirección',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección'})
    )
    region = forms.ChoiceField(
        choices=PerfilUsuario.REGION_CHOICES, label='Región',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento', required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                usuario=user,
                rut=self.cleaned_data['rut'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion'],
                region=self.cleaned_data['region'],
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )


class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PerfilUsuario
        fields = ['rut', 'telefono', 'direccion']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ─── FORMULARIOS ADMIN ────────────────────────────────────────────────────────

class CrearUsuarioAdminForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Administrador', 'Coordinador']),
        label='Perfil / Rol', required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    rut = forms.CharField(max_length=12, label='RUT', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, label='Teléfono', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            if self.cleaned_data.get('grupo'):
                user.groups.set([self.cleaned_data['grupo']])
            PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    'rut': self.cleaned_data.get('rut', ''),
                    'telefono': self.cleaned_data.get('telefono', ''),
                    'direccion': '',
                }
            )
        return user


class AsignarRolForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Administrador', 'Coordinador']),
        label='Rol a asignar', required=False,
        empty_label='(Sin rol especial)',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
