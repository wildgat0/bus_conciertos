from django.db import models
from django.contrib.auth.models import User
from core.models import Concierto


class Viaje(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('completo', 'Completo'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
    ]

    concierto = models.ForeignKey(Concierto, on_delete=models.CASCADE, verbose_name='Concierto')
    coordinador = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='viajes_coordinados', verbose_name='Coordinador'
    )
    origen = models.CharField(max_length=200, verbose_name='Punto de Origen')
    destino = models.CharField(max_length=200, verbose_name='Destino')
    fecha_salida = models.DateField(verbose_name='Fecha de Salida')
    cupos_totales = models.PositiveIntegerField(verbose_name='Cupos Totales')
    precio_vuelta = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Precio Solo Vuelta (CLP)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    descripcion = models.TextField(blank=True, verbose_name='Descripción adicional')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering = ['fecha_salida']

    def __str__(self):
        fecha = self.fecha_salida.strftime("%d/%m/%Y") if self.fecha_salida else 'sin fecha'
        return f'Viaje a {self.concierto.nombre} - {fecha}'

    @property
    def cupos_disponibles(self):
        from django.db.models import Sum
        cupos_usados = self.reserva_set.filter(estado='pagado').aggregate(total=Sum('cantidad'))['total'] or 0
        return self.cupos_totales - cupos_usados

    @property
    def cupos_ocupados(self):
        from django.db.models import Sum
        return self.reserva_set.filter(estado='pagado').aggregate(total=Sum('cantidad'))['total'] or 0

    @property
    def ganancia_total(self):
        from django.db.models import Sum
        total = self.reserva_set.filter(estado='pagado').aggregate(total=Sum('monto'))['total'] or 0
        return total


class HorarioViaje(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='horarios', verbose_name='Viaje')
    salida = models.CharField(max_length=200, verbose_name='Salida')
    hora_salida = models.TimeField(verbose_name='Hora de Salida')
    precio_ida = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Precio Solo Ida (CLP)')
    precio_vuelta = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Precio Solo Vuelta (CLP)')
    precio = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Precio Ida y Vuelta (CLP)')

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['hora_salida']

    def __str__(self):
        return f'{self.salida} | {self.hora_salida.strftime("%H:%M")}'



class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de Pago'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    TIPO_PASAJE_CHOICES = [
        ('ida_vuelta', 'Ida y Vuelta'),
        ('solo_ida',   'Solo Ida'),
        ('solo_vuelta','Solo Vuelta'),
    ]

    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name='Viaje')
    horario = models.ForeignKey(HorarioViaje, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas', verbose_name='Horario')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Pasajero')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad de cupos')
    tipo_pasaje = models.CharField(max_length=20, choices=TIPO_PASAJE_CHOICES, default='ida_vuelta', verbose_name='Tipo de pasaje')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    token_webpay = models.CharField(max_length=255, blank=True, null=True)
    orden_compra = models.CharField(max_length=50, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_reserva']

    def __str__(self):
        return f'Reserva #{self.id} - {self.usuario.get_full_name()} - {self.viaje}'

    def save(self, *args, **kwargs):
        if not self.orden_compra:
            import uuid
            self.orden_compra = f'BC-{uuid.uuid4().hex[:10].upper()}'
        if not self.monto:
            self.monto = self.viaje.precio * self.cantidad
        super().save(*args, **kwargs)
