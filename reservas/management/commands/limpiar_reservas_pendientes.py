from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservas.models import Reserva


class Command(BaseCommand):
    help = 'Elimina reservas pendientes de pago cuyo viaje es en menos de 2 días'

    def handle(self, *args, **options):
        limite = timezone.now() + timedelta(days=2)

        reservas = Reserva.objects.filter(
            estado='pendiente',
            viaje__fecha_salida__lte=limite
        ).select_related('viaje__concierto', 'usuario')

        total = reservas.count()

        if total == 0:
            self.stdout.write('No hay reservas pendientes vencidas.')
            return

        for r in reservas:
            self.stdout.write(
                f'  Eliminando: {r.usuario.get_full_name() or r.usuario.username} '
                f'— {r.viaje.concierto.artista} ({r.viaje.fecha_salida.strftime("%d/%m/%Y")})'
            )

        reservas.delete()
        self.stdout.write(self.style.SUCCESS(f'{total} reserva(s) pendiente(s) eliminada(s).'))
