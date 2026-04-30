import sqlite3
from flask import g

DATABASE = 'Backend/asistencia.db'

def get_db():
    """Conexión a la base de datos con soporte para nombres de columnas (Row Factory)"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        # ESTA ES LA LÍNEA CRÍTICA: Permite acceder a datos como user['username'] en lugar de user[0]
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    """Inicialización manual del esquema (Solo si se requiere resetear)"""
    with sqlite3.connect(DATABASE) as conn:
        # Re-usamos el esquema definido en el seed para mayor consistencia
        from seed import SCHEMA
        conn.executescript(SCHEMA)
        print("✅ Esquema de Base de Datos actualizado y limpio.")
