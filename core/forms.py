from django import forms
from .models import Concierto


class ConciertoForm(forms.ModelForm):
    class Meta:
        model = Concierto
        fields = ['nombre', 'artista', 'fecha', 'lugar', 'region', 'descripcion', 'imagen_url', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Legends Tour'}),
            'artista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Metallica'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estadio Nacional'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
