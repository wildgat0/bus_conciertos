from django.contrib import admin
from .models import Viaje, Reserva


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ['concierto', 'origen', 'destino', 'fecha_salida', 'cupos_totales', 'cupos_disponibles', 'precio', 'estado']
    list_filter = ['estado', 'concierto__region']
    search_fields = ['concierto__nombre', 'origen', 'destino']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['orden_compra', 'usuario', 'viaje', 'estado', 'monto', 'fecha_reserva']
    list_filter = ['estado']
    search_fields = ['orden_compra', 'usuario__username', 'usuario__email']
