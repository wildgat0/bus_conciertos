from django import forms
from .models import Viaje, Reserva, HorarioViaje
from core.models import Concierto


class ViajeForm(forms.ModelForm):
    concierto_nombre = forms.CharField(
        label='Concierto',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Metallica, Ed Sheeran...',
            'autocomplete': 'off',
        })
    )

    class Meta:
        model = Viaje
        fields = ['origen', 'destino', 'fecha_salida', 'cupos_totales', 'precio_vuelta', 'estado']
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Terminal Alameda, Santiago'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Movistar Arena'}),
            'fecha_salida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cupos_totales': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_vuelta': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ej: 15000'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Al editar, prellenar el campo con el concierto actual
        if self.instance and self.instance.pk:
            self.fields['concierto_nombre'].initial = (
                f"{self.instance.concierto.artista} — {self.instance.concierto.nombre}"
            )


class HorarioViajeForm(forms.ModelForm):
    class Meta:
        model = HorarioViaje
        fields = ['ciudad', 'salida', 'hora_salida', 'precio_ida', 'precio']
        widgets = {
            'ciudad': forms.Select(attrs={'class': 'form-select'}),
            'salida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Terminal Alameda, Santiago'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'precio_ida': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ej: 15000'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ej: 25000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


class AgregarPasajeroManualForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_titular', 'rut', 'contacto', 'email', 'cantidad', 'tipo_pasaje', 'monto', 'horario', 'ciudad_vuelta', 'plataforma']
        widgets = {
            'nombre_titular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'rut':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
            'contacto':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXX XXXX'}),
            'email':          forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.cl'}),
            'cantidad':       forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tipo_pasaje':    forms.Select(attrs={'class': 'form-select'}),
            'monto':          forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'horario':        forms.Select(attrs={'class': 'form-select'}),
            'ciudad_vuelta':  forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '— Selecciona ciudad —'),
                ('Belloto', 'Belloto'),
                ('Viña del Mar', 'Viña del Mar'),
                ('Valparaíso', 'Valparaíso'),
                ('Placilla', 'Placilla'),
                ('Casablanca - Cruce Chacabuco', 'Casablanca - Cruce Chacabuco'),
            ]),
            'plataforma':     forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '— Selecciona plataforma —'),
                ('WHATSAPP', 'WhatsApp'),
                ('INSTAGRAM', 'Instagram'),
                ('PRESENCIAL', 'Presencial'),
            ]),
        }

    def __init__(self, *args, viaje=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario'].required = False
        self.fields['ciudad_vuelta'].required = False
        self.fields['email'].required = False
        self.fields['plataforma'].required = False
        if viaje:
            self.fields['horario'].queryset = viaje.horarios.all()
