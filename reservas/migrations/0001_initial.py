from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=200, verbose_name='Punto de Origen')),
                ('destino', models.CharField(max_length=200, verbose_name='Destino')),
                ('fecha_salida', models.DateTimeField(verbose_name='Fecha y Hora de Salida')),
                ('fecha_regreso', models.DateTimeField(verbose_name='Fecha y Hora de Regreso')),
                ('cupos_totales', models.PositiveIntegerField(verbose_name='Cupos Totales')),
                ('precio', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Precio por Pasajero (CLP)')),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('completo', 'Completo'), ('cancelado', 'Cancelado'), ('realizado', 'Realizado')], default='disponible', max_length=20)),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción adicional')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('concierto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.concierto', verbose_name='Concierto')),
                ('coordinador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='viajes_coordinados', to=settings.AUTH_USER_MODEL, verbose_name='Coordinador')),
            ],
            options={'verbose_name': 'Viaje', 'verbose_name_plural': 'Viajes', 'ordering': ['fecha_salida']},
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente de Pago'), ('pagado', 'Pagado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('fecha_reserva', models.DateTimeField(auto_now_add=True)),
                ('token_webpay', models.CharField(blank=True, max_length=255, null=True)),
                ('orden_compra', models.CharField(max_length=50, unique=True)),
                ('monto', models.DecimalField(decimal_places=0, max_digits=10)),
                ('viaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.viaje', verbose_name='Viaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Pasajero')),
            ],
            options={'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas', 'ordering': ['-fecha_reserva']},
        ),
    ]
