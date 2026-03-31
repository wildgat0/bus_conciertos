from django import forms
from .models import Viaje, Reserva
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
        fields = ['origen', 'destino', 'fecha_salida', 'fecha_regreso',
                  'cupos_totales', 'precio', 'estado', 'descripcion']
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Terminal Alameda, Santiago'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Movistar Arena'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'fecha_regreso': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'cupos_totales': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_salida'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['fecha_regreso'].input_formats = ['%Y-%m-%dT%H:%M']
        # Al editar, prellenar el campo con el concierto actual
        if self.instance and self.instance.pk:
            self.fields['concierto_nombre'].initial = (
                f"{self.instance.concierto.artista} — {self.instance.concierto.nombre}"
            )


class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
