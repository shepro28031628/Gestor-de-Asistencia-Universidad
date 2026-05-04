import sqlite3
import os

from models import SCHEMA

def restore_database():
    """
    Función de utilidad para desarrolladores. 
    Borra la base de datos actual e inserta datos de prueba realistas.
    """
    # Determinamos la ruta absoluta para evitar errores de directorio de trabajo (CWD)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'asistencia.db')
    print(f"Restaurando base de datos en: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Limpieza total de la base de datos
    tablas = [
        'justifications', 'citations', 'attendances', 'class_sessions', 
        'enrollments', 'schedules', 'groups', 'subjects', 'rooms', 
        'campuses', 'users', 'academic_programs'
    ]
    for tabla in tablas:
        cursor.execute(f"DROP TABLE IF EXISTS {tabla}")
    
    # Creación de tablas
    cursor.executescript(SCHEMA)
    print("Esquema creado.")

    # --- DATOS DE PRUEBA: PROFESORES ---
    profesores = [
        ('elfar_morantes', '123', 'ELFAR DIDIER MORANTES SANCHEZ', 'profesor', 'elfar.morantes@uninpahu.edu.co'),
        ('dakar_sarmiento', '123', 'DAKAR SARMIENTO', 'profesor', 'dakar.sarmiento@uninpahu.edu.co')
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role, email) VALUES (?,?,?,?,?)", profesores)
    
    # --- DATOS DE PRUEBA: SEDES Y SALONES REALES ---
    sedes = [
        ('Sede Teusaquillo (Dg. 40a)', 4.6300, -74.0684, 100),
        ('Sede Principal (Cra. 16)', 4.6318, -74.0665, 100),
        ('Sede Parkway (Dg. 40a)', 4.6310, -74.0685, 100)
    ]
    cursor.executemany("INSERT INTO campuses (name, latitude, longitude, radius_meters) VALUES (?,?,?,?)", sedes)
    
    # Vincular salones a las sedes reales
    cursor.execute("INSERT INTO rooms (code, campus_id) VALUES ('LAB-301', 1)") # En Dg. 40a
    cursor.execute("INSERT INTO rooms (code, campus_id) VALUES ('AUD-102', 2)") # En Cra. 16
    
    # --- DATOS DE PRUEBA: MATERIAS Y GRUPOS ---
    # Machine Learning
    cursor.execute("INSERT INTO subjects (code, name) VALUES ('IS1791', 'MACHINE LEARNING Y DEEP LEARNING')")
    sub_ml = cursor.lastrowid
    cursor.execute("INSERT INTO groups (group_number, subject_id, teacher_id, start_date, end_date, jornada) VALUES ('750', ?, 1, '2026-02-02', '2026-05-30', 'Sabatino')", (sub_ml,))
    group_ml = cursor.lastrowid

    # Videojuegos
    cursor.execute("INSERT INTO subjects (code, name) VALUES ('IS1792', 'DESARROLLO DE VIDEOJUEGOS')")
    sub_vg = cursor.lastrowid
    cursor.execute("INSERT INTO groups (group_number, subject_id, teacher_id, start_date, end_date, jornada) VALUES ('750', ?, 2, '2026-02-02', '2026-05-30', 'Diurno')", (sub_vg,))
    group_vg = cursor.lastrowid

    # --- DATOS DE PRUEBA: HORARIOS ---
    # Sábados
    cursor.execute("INSERT INTO schedules (group_id, room_id, day, start_time, end_time) VALUES (?, 1, 'S', '07:00', '23:59')", (group_ml,))
    # Miércoles
    cursor.execute("INSERT INTO schedules (group_id, room_id, day, start_time, end_time) VALUES (?, 1, 'W', '14:15', '17:15')", (group_vg,))

    # --- DATOS DE PRUEBA: ESTUDIANTES ---
    estudiantes = [
        ('202518003330', '123', 'ESTUDIANTE MASTER', 'estudiante'),
        ('2025100001', '123', 'OLIVIA FLORES', 'estudiante')
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role) VALUES (?,?,?,?)", estudiantes)
    
    # Inscripción masiva de estudiantes en grupos
    cursor.execute("SELECT id FROM users WHERE role='estudiante'")
    student_ids = [s[0] for s in cursor.fetchall()]
    cursor.execute("SELECT id FROM groups")
    group_ids = [g[0] for g in cursor.fetchall()]
    
    for sid in student_ids:
        for gid in group_ids:
            cursor.execute("INSERT INTO enrollments (student_id, group_id) VALUES (?, ?)", (sid, gid))

    conn.commit()
    conn.close()
    print("BASE DE DATOS RESTAURADA CON EXITO. Sistema listo para pruebas.")

if __name__ == '__main__':
    restore_database()
