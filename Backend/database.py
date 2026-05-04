import sqlite3
from flask import g

# Ruta central del archivo de base de datos
DATABASE = 'Backend/asistencia.db'

def get_db():
    """
    Gestiona la conexión única por petición (Request) de Flask.
    Configura el modo de alta concurrencia y la integridad referencial.
    """
    if 'db' not in g:
        # Abrimos la conexión física
        g.db = sqlite3.connect(DATABASE)
        
        # --- CONFIGURACIÓN DE ESTABILIDAD ---
        # Modo WAL (Write-Ahead Logging): Permite lecturas y escrituras simultáneas sin bloqueos.
        g.db.execute('PRAGMA journal_mode=WAL;')
        # Activación de Llaves Foráneas: Garantiza que no se eliminen registros con dependencias activas.
        g.db.execute('PRAGMA foreign_keys=ON;')
        
        # Row Factory: Convierte las filas de la DB en diccionarios para usar nombres de columnas (user['id']).
        g.db.row_factory = sqlite3.Row
        
    return g.db

def init_db():
    """
    Utilidad para recrear la base de datos desde cero usando el esquema definido en seed.py.
    ADVERTENCIA: Borra todos los datos existentes.
    """
    with sqlite3.connect(DATABASE) as conn:
        # Importación diferida para evitar ciclos de dependencia
        from seed import SCHEMA
        # Ejecución del script SQL completo
        conn.executescript(SCHEMA)
        print("✅ Esquema de Base de Datos actualizado y limpio.")
