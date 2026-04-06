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
        fields = ['salida', 'hora_salida', 'precio_ida', 'precio']
        widgets = {
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
