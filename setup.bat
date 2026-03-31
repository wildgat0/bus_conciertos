@echo off
echo.
echo  BUS CONCIERTOS - Instalacion rapida (Windows)
echo ================================================
echo.

echo Creando entorno virtual...
python -m venv venv

echo Activando entorno virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Aplicando migraciones...
python manage.py makemigrations
python manage.py migrate

echo Cargando datos de ejemplo...
python seed_data.py

echo.
echo ============================================
echo  Instalacion completada exitosamente!
echo ============================================
echo.
echo Para iniciar el servidor ejecuta:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Abre en el navegador: http://127.0.0.1:8000/
echo.
pause
