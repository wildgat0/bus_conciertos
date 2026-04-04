from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    REGION_CHOICES = [
        ('santiago', 'Región Metropolitana'),
        ('valparaiso', 'Región de Valparaíso'),
        ('otra', 'Otra región'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfilusuario')
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    direccion = models.CharField(max_length=300, verbose_name='Dirección')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='santiago', verbose_name='Región')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f'Perfil de {self.usuario.get_full_name() or self.usuario.username}'

    def get_nombre_completo(self):
        return self.usuario.get_full_name() or self.usuario.username


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        # Solo crear perfil vacío para usuarios que se registren via el formulario
        pass
