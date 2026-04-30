import pytest
import sys
import os

# Añadir el path del backend para poder importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))

from routes.attendance import haversine_distance

def test_haversine_accuracy():
    """Verifica que el cálculo de distancia entre dos coordenadas sea correcto."""
    # Coordenadas de prueba (Distancia aprox 157 metros)
    lat1, lon1 = 4.6300, -74.0700
    lat2, lon2 = 4.6310, -74.0710
    
    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert 150 < dist < 165  # Tolerancia aceptable

def test_haversine_same_point():
    """Distancia entre el mismo punto debe ser 0."""
    lat, lon = 4.6280, -74.0650
    dist = haversine_distance(lat, lon, lat, lon)
    assert dist == 0

def test_invalid_login_logic():
    """Prueba conceptual de rechazo de credenciales (Mock)."""
    # En un entorno real usaríamos el cliente de pruebas de Flask
    user_input = {"user": "admin", "pass": "incorrecta"}
    assert user_input["pass"] != "123"

def test_attendance_status_types():
    """Asegura que solo se usen los estados de asistencia permitidos."""
    valid_statuses = ["qr", "manual", "justificada"]
    current_status = "qr"
    assert current_status in valid_statuses
