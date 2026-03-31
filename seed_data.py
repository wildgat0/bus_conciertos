"""
Script para poblar la base de datos con datos de ejemplo.
Ejecutar: python seed_data.py  (con el entorno virtual activo y desde la carpeta del proyecto)
O bien:   python manage.py shell < seed_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_conciertos.settings')
django.setup()

from django.contrib.auth.models import User, Group
from core.models import Concierto
from reservas.models import Viaje
from usuarios.models import PerfilUsuario
from datetime import date, time, datetime
from django.utils import timezone

print("🚌 Iniciando carga de datos de ejemplo...")

# ─── 1. CREAR GRUPOS ──────────────────────────────────────────
admin_group, _ = Group.objects.get_or_create(name='Administrador')
coord_group, _ = Group.objects.get_or_create(name='Coordinador')
print("✅ Grupos creados: Administrador, Coordinador")

# ─── 2. CREAR SUPERUSUARIO ADMIN ──────────────────────────────
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@busconciertos.cl', 'admin1234')
    admin.first_name = 'Administrador'
    admin.last_name = 'Sistema'
    admin.save()
    admin.groups.add(admin_group)
    PerfilUsuario.objects.create(
        usuario=admin, rut='12.345.678-9',
        telefono='+56 9 0000 0001', direccion='Oficina Central, Santiago',
        region='santiago'
    )
    print("✅ Admin creado: usuario=admin / contraseña=admin1234")
else:
    admin = User.objects.get(username='admin')
    print("ℹ️  Admin ya existe")

# ─── 3. CREAR COORDINADOR ─────────────────────────────────────
if not User.objects.filter(username='coordinador').exists():
    coord = User.objects.create_user('coordinador', 'coord@busconciertos.cl', 'coord1234')
    coord.first_name = 'Carlos'
    coord.last_name = 'Coordinador'
    coord.save()
    coord.groups.add(coord_group)
    PerfilUsuario.objects.create(
        usuario=coord, rut='9.876.543-2',
        telefono='+56 9 1111 2222', direccion='Santiago Centro',
        region='santiago'
    )
    print("✅ Coordinador creado: usuario=coordinador / contraseña=coord1234")
else:
    coord = User.objects.get(username='coordinador')
    print("ℹ️  Coordinador ya existe")

# ─── 4. CREAR USUARIO NORMAL ──────────────────────────────────
if not User.objects.filter(username='pasajero1').exists():
    pasajero = User.objects.create_user('pasajero1', 'pasajero@email.cl', 'pasajero1234')
    pasajero.first_name = 'María'
    pasajero.last_name = 'González'
    pasajero.save()
    PerfilUsuario.objects.create(
        usuario=pasajero, rut='15.678.901-K',
        telefono='+56 9 8765 4321', direccion='Av. Providencia 1234, Santiago',
        region='santiago', fecha_nacimiento=date(1995, 6, 15)
    )
    print("✅ Usuario pasajero: usuario=pasajero1 / contraseña=pasajero1234")
else:
    print("ℹ️  pasajero1 ya existe")

# ─── 5. CREAR CONCIERTOS ──────────────────────────────────────
conciertos_data = [
    # Santiago
    {
        'nombre': 'Tour Mundial 2025', 'artista': 'Bad Bunny',
        'fecha': date(2025, 9, 15), 'hora': time(20, 0),
        'lugar': 'Estadio Nacional, Santiago', 'region': 'santiago',
        'descripcion': 'El reggaetonero puertorriqueño vuelve a Chile con su tour más ambicioso.'
    },
    {
        'nombre': 'El Último Tour Del Mundo', 'artista': 'Dua Lipa',
        'fecha': date(2025, 10, 3), 'hora': time(21, 0),
        'lugar': 'Movistar Arena, Santiago', 'region': 'santiago',
        'descripcion': 'La estrella del pop presenta su nuevo álbum en Chile.'
    },
    {
        'nombre': 'Infinite Euphoria Tour', 'artista': 'The Weeknd',
        'fecha': date(2025, 10, 25), 'hora': time(20, 30),
        'lugar': 'Estadio Monumental, Santiago', 'region': 'santiago',
        'descripcion': 'Abel Tesfaye llega con su show de luz y sonido más impresionante.'
    },
    {
        'nombre': 'Legends Tour', 'artista': 'Metallica',
        'fecha': date(2025, 11, 8), 'hora': time(19, 30),
        'lugar': 'Estadio Nacional, Santiago', 'region': 'santiago',
        'descripcion': 'Los reyes del metal regresan a Chile en una noche histórica.'
    },
    {
        'nombre': 'Renaissance World Tour', 'artista': 'Beyoncé',
        'fecha': date(2025, 11, 22), 'hora': time(21, 0),
        'lugar': 'Movistar Arena, Santiago', 'region': 'santiago',
        'descripcion': 'Queen Bey trae su espectáculo más grande a Latinoamérica.'
    },
    # Valparaíso
    {
        'nombre': 'Chile Tour 2025', 'artista': 'Mon Laferte',
        'fecha': date(2025, 9, 20), 'hora': time(20, 0),
        'lugar': 'Aula Magna PUCV, Valparaíso', 'region': 'valparaiso',
        'descripcion': 'La cantante chilena regresa a su ciudad en una noche íntima.'
    },
    {
        'nombre': 'Rock en el Puerto', 'artista': 'Los Tres',
        'fecha': date(2025, 10, 11), 'hora': time(19, 0),
        'lugar': 'Anfiteatro España, Valparaíso', 'region': 'valparaiso',
        'descripcion': 'Los Tres celebran 30 años con un concierto histórico en el puerto.'
    },
    {
        'nombre': 'Festival del Cerro', 'artista': 'Inti-Illimani',
        'fecha': date(2025, 10, 18), 'hora': time(19, 30),
        'lugar': 'Teatro Municipal de Valparaíso', 'region': 'valparaiso',
        'descripcion': 'Una noche de música latinoamericana en el corazón de Valparaíso.'
    },
]

conciertos_creados = []
for c in conciertos_data:
    obj, created = Concierto.objects.get_or_create(
        nombre=c['nombre'], artista=c['artista'],
        defaults={**c}
    )
    conciertos_creados.append(obj)
    if created:
        print(f"  🎵 Concierto: {obj.artista} — {obj.nombre}")

print(f"✅ {len(conciertos_creados)} conciertos disponibles")

# ─── 6. CREAR VIAJES ──────────────────────────────────────────
viajes_data = [
    {
        'concierto': conciertos_creados[0],  # Bad Bunny
        'origen': 'Terminal Alameda, Santiago',
        'destino': 'Estadio Nacional, Santiago',
        'fecha_salida': timezone.make_aware(datetime(2025, 9, 15, 17, 30)),
        'fecha_regreso': timezone.make_aware(datetime(2025, 9, 15, 23, 30)),
        'cupos_totales': 45, 'precio': 8000,
    },
    {
        'concierto': conciertos_creados[0],  # Bad Bunny - Valparaíso
        'origen': 'Terminal de Buses, Valparaíso',
        'destino': 'Estadio Nacional, Santiago',
        'fecha_salida': timezone.make_aware(datetime(2025, 9, 15, 15, 0)),
        'fecha_regreso': timezone.make_aware(datetime(2025, 9, 16, 1, 0)),
        'cupos_totales': 50, 'precio': 12000,
    },
    {
        'concierto': conciertos_creados[1],  # Dua Lipa
        'origen': 'Estación Central, Santiago',
        'destino': 'Movistar Arena, Santiago',
        'fecha_salida': timezone.make_aware(datetime(2025, 10, 3, 18, 0)),
        'fecha_regreso': timezone.make_aware(datetime(2025, 10, 3, 23, 59)),
        'cupos_totales': 40, 'precio': 9500,
    },
    {
        'concierto': conciertos_creados[5],  # Mon Laferte - Valpo
        'origen': 'Terminal de Buses, Viña del Mar',
        'destino': 'Aula Magna PUCV, Valparaíso',
        'fecha_salida': timezone.make_aware(datetime(2025, 9, 20, 18, 30)),
        'fecha_regreso': timezone.make_aware(datetime(2025, 9, 20, 23, 0)),
        'cupos_totales': 30, 'precio': 5000,
    },
]

for v in viajes_data:
    viaje, created = Viaje.objects.get_or_create(
        concierto=v['concierto'],
        origen=v['origen'],
        defaults={**v, 'coordinador': coord, 'estado': 'disponible'}
    )
    if created:
        print(f"  🚌 Viaje: {viaje.origen} → {viaje.destino} ({viaje.concierto.artista})")

print("✅ Viajes creados exitosamente")
print()
print("═" * 50)
print("🎉 Base de datos lista con datos de ejemplo")
print("═" * 50)
print()
print("CREDENCIALES DE ACCESO:")
print("  👑 Administrador: admin / admin1234")
print("  🔧 Coordinador:  coordinador / coord1234")
print("  👤 Pasajero:     pasajero1 / pasajero1234")
print()
print("Para iniciar el servidor:")
print("  python manage.py runserver")
print("  → http://127.0.0.1:8000/")
