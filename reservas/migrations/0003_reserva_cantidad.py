from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_unique_reserva_por_usuario_viaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, verbose_name='Cantidad de cupos'),
        ),
    ]
