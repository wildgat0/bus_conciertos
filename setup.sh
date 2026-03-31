#!/bin/bash
# ════════════════════════════════════════
#  BUS CONCIERTOS — Script de instalación
# ════════════════════════════════════════

echo ""
echo "🚌 BUS CONCIERTOS — Instalación automática"
echo "══════════════════════════════════════════"
echo ""

# 1. Crear entorno virtual
echo "📦 Creando entorno virtual..."
python -m venv venv

# 2. Activar entorno
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 3. Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt -q

# 4. Migraciones
echo "🗄️  Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# 5. Datos de ejemplo
echo "🌱 Cargando datos de ejemplo..."
python seed_data.py

echo ""
echo "✅ Instalación completada"
echo ""
echo "Para iniciar el servidor:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\\Scripts\\activate     (Windows)"
echo "  python manage.py runserver"
echo ""
echo "Abrir en el navegador: http://127.0.0.1:8000/"
