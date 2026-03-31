from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_reserva_cantidad'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together=set(),
        ),
    ]
