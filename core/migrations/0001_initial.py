from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Concierto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre del Concierto')),
                ('artista', models.CharField(max_length=200, verbose_name='Artista / Banda')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('lugar', models.CharField(max_length=300, verbose_name='Lugar / Recinto')),
                ('region', models.CharField(choices=[('santiago', 'Santiago'), ('valparaiso', 'Región de Valparaíso')], max_length=20, verbose_name='Región')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('imagen_url', models.URLField(blank=True, verbose_name='URL Imagen')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Concierto', 'verbose_name_plural': 'Conciertos', 'ordering': ['fecha']},
        ),
    ]
