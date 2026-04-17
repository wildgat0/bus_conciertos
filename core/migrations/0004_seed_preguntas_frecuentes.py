from django.db import migrations

PREGUNTAS = [
    (
        1,
        '¿Puedo reservar sin pagar de inmediato?',
        'Sí. Puedes guardar una reserva como "pendiente" y pagar antes de la fecha del viaje. '
        'Sin embargo, el cupo no queda asegurado hasta el pago.',
    ),
    (
        2,
        '¿Cómo sé si mi pago fue exitoso?',
        'Recibirás un correo de confirmación con el comprobante de pago y número de orden. '
        'Además, el estado de tu reserva en "Mis Reservas" cambiará a Pagado.',
    ),
    (
        3,
        '¿Qué pasa si el viaje se cancela?',
        'El coordinador actualiza el estado del viaje a Cancelado. Te recomendamos contactar '
        'al equipo por WhatsApp (botón disponible en el sitio) para coordinar el reembolso.',
    ),
    (
        4,
        '¿Cómo puedo saber cuántos descuentos tengo acumulados?',
        'En el detalle de cualquier viaje disponible, el sistema muestra tu progreso de '
        'fidelidad y cuántos asientos te faltan para el próximo descuento.',
    ),
    (
        5,
        '¿Puedo comprar asientos para otras personas?',
        'Sí. Al crear la reserva puedes ingresar el nombre y RUT del titular (quien viaja), '
        'que puede ser distinto al usuario que realiza la compra.',
    ),
    (
        6,
        '¿Dónde puedo obtener ayuda?',
        'Usa el botón de WhatsApp disponible en todas las páginas del sitio para contactar '
        'directamente al equipo de Bus Conciertos.',
    ),
]


def seed(apps, schema_editor):
    PreguntaFrecuente = apps.get_model('core', 'PreguntaFrecuente')
    for orden, pregunta, respuesta in PREGUNTAS:
        PreguntaFrecuente.objects.create(orden=orden, pregunta=pregunta, respuesta=respuesta)


def unseed(apps, schema_editor):
    apps.get_model('core', 'PreguntaFrecuente').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_preguntas_frecuentes'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
