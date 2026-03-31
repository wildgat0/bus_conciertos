from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True, verbose_name='RUT')),
                ('telefono', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('direccion', models.CharField(max_length=300, verbose_name='Dirección')),
                ('region', models.CharField(choices=[('santiago', 'Región Metropolitana'), ('valparaiso', 'Región de Valparaíso'), ('otra', 'Otra región')], default='santiago', max_length=20, verbose_name='Región')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='perfiles/', verbose_name='Foto de Perfil')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfilusuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Perfil de Usuario', 'verbose_name_plural': 'Perfiles de Usuario'},
        ),
    ]
