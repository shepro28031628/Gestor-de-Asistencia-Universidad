import sqlite3
import os

def update_passwords():
    """Actualiza todas las contraseñas para que coincidan con el documento (username)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'asistencia.db')
    
    if not os.path.exists(db_path):
        print("❌ Error: No se encontró la base de datos.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL masivo para igualar contraseña a documento
    cursor.execute("UPDATE users SET password = username")
    
    conn.commit()
    count = cursor.rowcount
    conn.close()
    print(f"✅ Proceso completado: {count} usuarios actualizados.")

if __name__ == '__main__':
    update_passwords()
