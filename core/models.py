from django.db import models


class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=300, verbose_name='Pregunta')
    respuesta = models.TextField(verbose_name='Respuesta')
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'
        ordering = ['orden']

    def __str__(self):
        return self.pregunta


class Concierto(models.Model):
    REGION_CHOICES = [
        ('santiago', 'Santiago'),
        ('valparaiso', 'Región de Valparaíso'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre del Concierto')
    artista = models.CharField(max_length=200, verbose_name='Artista / Banda')
    fecha = models.DateField(verbose_name='Fecha')
    lugar = models.CharField(max_length=300, verbose_name='Lugar / Recinto')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name='Región')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    imagen_url = models.URLField(blank=True, verbose_name='URL Imagen')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['fecha']

    def __str__(self):
        return f'{self.nombre} - {self.artista} ({self.fecha})'
