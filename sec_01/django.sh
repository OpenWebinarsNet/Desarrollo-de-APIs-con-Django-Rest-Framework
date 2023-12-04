#!/bin/bash
# Script Instalación Django Linux (django.sh)

if [ "$#" -eq 0 ]; then
    echo
    echo "ERROR: Faltan parámetros"
    echo "USO: ./django.sh 'nombre_proyecto' ['nombre_aplicación']"
    exit 1
fi

#!/bin/bash
# Script Instalación Django Linux (django.sh)
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install Django
python -m pip install djangorestframework
python -m pip install markdown       # Markdown support for the browsable API.
python -m pip install django-filter
django-admin startproject $1 .

if [ -n "$2" ]; then
    python manage.py startapp $2
fi

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@admin.com

echo "------------------------------"
echo "Modificar en settings.py:"
echo "  - LANGUAGE_CODE = 'es-ES'"
echo "  - TIME_ZONE = 'Europe/Madrid'"
echo "  - Registrar la aplicación 'rest_framework' en settings.py"

if [ -n "$2" ]; then
    echo "  - Registrar tu aplicación'$2' en settings.py"
fi

echo "------------------------------"
echo "  No olvides cambiar el interprete en VS Code"
echo "      Ctrl+Shift+P -> Python: Select Interpreter"
echo "------------------------------"