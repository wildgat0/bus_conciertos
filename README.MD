# 🚌 BUS CONCIERTOS
### Sistema de Reservas de Buses a Conciertos
> Django · SQLite · WebPay Transbank · Colores corporativos: Amarillo #FFD600 y Negro #0D0D0D

---

## 📋 Descripción

**Bus Conciertos** es un sistema web completo desarrollado en Python con el framework **Django** y base de datos **SQLite**, que permite gestionar reservas de buses hacia conciertos en Santiago y la Región de Valparaíso, Chile. El pago se procesa mediante la API de **WebPay Transbank**.

---

## 🗂️ Estructura del Proyecto

```
bus_conciertos/
├── bus_conciertos/         # Configuración principal Django
│   ├── settings.py         # Configuraciones, BD, Transbank
│   ├── urls.py             # URLs raíz
│   └── wsgi.py
│
├── core/                   # App principal (Inicio, Quiénes Somos)
│   ├── models.py           # Modelo Concierto
│   ├── views.py            # Vistas: inicio, quienes_somos
│   ├── urls.py
│   └── templates/core/
│       ├── inicio.html
│       └── quienes_somos.html
│
├── reservas/               # App de reservas y viajes
│   ├── models.py           # Modelos: Viaje, Reserva
│   ├── views.py            # Viajes, WebPay, auditoría
│   ├── forms.py            # Formularios
│   ├── urls.py
│   └── templates/reservas/
│       ├── lista_viajes.html
│       ├── detalle_viaje.html
│       ├── webpay_redirect.html
│       ├── pago_exitoso.html
│       ├── pago_fallido.html
│       ├── mis_reservas.html
│       ├── gestion_viajes.html
│       ├── form_viaje.html
│       ├── pasajeros_viaje.html
│       ├── form_pasajero.html
│       ├── confirmar_eliminar.html
│       └── auditoria.html
│
├── usuarios/               # App de usuarios y perfiles
│   ├── models.py           # Modelo PerfilUsuario
│   ├── views.py            # Login, registro, gestión admin
│   ├── forms.py            # Formularios de usuario
│   ├── decorators.py       # @coordinador_required, @admin_required
│   ├── urls.py
│   └── templates/usuarios/
│       ├── login.html
│       ├── registro.html
│       ├── mi_perfil.html
│       ├── gestion_usuarios.html
│       ├── form_usuario.html
│       ├── editar_usuario.html
│       ├── asignar_rol.html
│       └── confirmar_eliminar_usuario.html
│
├── templates/
│   └── base.html           # Template base (navbar, footer, WhatsApp)
│
├── static/
│   ├── css/main.css        # Estilos corporativos (Amarillo/Negro)
│   └── js/main.js          # JavaScript principal
│
├── manage.py
├── seed_data.py            # Script para cargar datos de ejemplo
└── requirements.txt
```

---

## 🚀 Instalación y Configuración

### 1. Requisitos previos
- Python 3.10 o superior
- pip

### 2. Clonar y configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar datos de ejemplo

```bash
python seed_data.py
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000/**

---

## 👤 Credenciales de Acceso

| Perfil | Usuario | Contraseña |
|--------|---------|------------|
| 👑 Administrador | `admin` | `admin1234` |
| 🔧 Coordinador | `coordinador` | `coord1234` |
| 👤 Pasajero | `pasajero1` | `pasajero1234` |

---

## 🔐 Perfiles y Permisos

### 👑 Administrador
- Acceso completo a todos los módulos
- **Módulo privado de Auditoría**: Ganancias totales por viaje
- **Módulo de Gestión de Usuarios**: Crear, editar, eliminar usuarios y asignar roles
- Puede hacer todo lo que hace el Coordinador

### 🔧 Coordinador
- Crear/editar/eliminar viajes (concierto, cupos, horarios, precio)
- Ver listado de pasajeros por viaje
- Modificar estado de reservas de pasajeros
- Eliminar pasajeros de un viaje

### 👤 Usuario Normal
- Registro e inicio de sesión
- Ver viajes disponibles
- Reservar viajes (requiere pago con WebPay)
- Ver historial de reservas propias
- Editar su perfil personal

---

## 💳 Integración WebPay (Transbank)

El sistema usa el **ambiente de integración (TEST)** de Transbank. Para pasar a producción:

### Cambiar en `settings.py`:
```python
TRANSBANK_COMMERCE_CODE = 'TU_CODIGO_COMERCIO_REAL'
TRANSBANK_API_KEY = 'TU_API_KEY_REAL'
TRANSBANK_ENVIRONMENT = 'LIVE'  # Cambiar de 'TEST' a 'LIVE'
```

### Tarjeta de prueba WebPay (ambiente TEST):
- **Número**: 4051 8856 0044 6623
- **CVV**: 123
- **Fecha vencimiento**: cualquier fecha futura
- **RUT**: 11.111.111-1
- **Contraseña internet**: 123

Documentación completa: https://www.transbankdevelopers.cl/referencia/webpay

---

## 📱 Funcionalidades Principales

### 🏠 Módulo Inicio
- Información de próximos conciertos en Santiago y Valparaíso
- Calendario visual con fechas de conciertos
- Acceso directo a WhatsApp de la empresa

### 🎫 Módulo Reservas
- Listado de viajes disponibles con cupos en tiempo real
- Detalle del viaje con datos del pasajero pre-llenados
- Pago online con WebPay Transbank
- Historial de reservas por usuario

### 👥 Módulo Quiénes Somos
- Información de la empresa
- Estadísticas y equipo

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|-----------|-----|
| Python 3.10+ | Lenguaje principal |
| Django 4.x | Framework web |
| SQLite | Base de datos |
| WebPay Transbank | Pasarela de pago |
| Font Awesome 6 | Iconografía |
| Google Fonts | Tipografías (Bebas Neue, Barlow) |
| WhatsApp API | Botón de contacto directo |

---

## ⚙️ Variables de Configuración (`settings.py`)

```python
# WhatsApp de la empresa
WHATSAPP_NUMBER = '+56998762197'

# Transbank (TEST/LIVE)
TRANSBANK_COMMERCE_CODE = '597055555532'
TRANSBANK_API_KEY = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
TRANSBANK_ENVIRONMENT = 'TEST'
```

---

## 📞 Soporte

Para consultas, utilizar el botón de WhatsApp en la plataforma o escribir a: contacto@busconciertos.cl
