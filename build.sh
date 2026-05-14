#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalación de dependencias
pip install -r requirements.txt

# Inicializar base de datos si no existe
if [ ! -f Backend/asistencia.db ]; then
    echo "Base de datos no encontrada. Inicializando..."
    python Backend/seed.py
fi
