import sqlite3
import os

# ESQUEMA DE BASE DE DATOS (Sincronizado con models.py)
# Se utiliza para resetear la base de datos a un estado inicial controlado.
SCHEMA = '''
DROP TABLE IF EXISTS justifications;
DROP TABLE IF EXISTS citations;
DROP TABLE IF EXISTS attendances;
DROP TABLE IF EXISTS class_sessions;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS campuses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS academic_programs;

CREATE TABLE academic_programs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, code TEXT);
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, email TEXT, role TEXT, program_id INTEGER, profile_pic TEXT);
CREATE TABLE campuses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, latitude REAL, longitude REAL, radius_meters INTEGER);
CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT, campus_id INTEGER);
CREATE TABLE subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, name TEXT);
CREATE TABLE groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_number TEXT, subject_id INTEGER, teacher_id INTEGER, start_date TEXT, end_date TEXT, jornada TEXT);
CREATE TABLE schedules (id INTEGER PRIMARY KEY AUTOINCREMENT, group_id INTEGER, room_id INTEGER, day TEXT, start_time TEXT, end_time TEXT);
CREATE TABLE enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, group_id INTEGER);
CREATE TABLE class_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, schedule_id INTEGER, qr_token TEXT, expires_at TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_active INTEGER DEFAULT 1);
CREATE TABLE attendances (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, session_id INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, lat REAL, lng REAL, distance_to_campus REAL, status TEXT DEFAULT 'Presente');
CREATE TABLE citations (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER, student_id INTEGER, message TEXT, status TEXT DEFAULT 'activa', timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE justifications (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, schedule_id INTEGER, file_path TEXT, status TEXT DEFAULT 'pendiente', timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
'''

def restore_database():
    """
    Función de utilidad para desarrolladores. 
    Borra la base de datos actual e inserta datos de prueba realistas.
    """
    db_path = 'Backend/asistencia.db'
    print(f"🛠️ Restaurando base de datos en: {os.path.abspath(db_path)}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creación de tablas
    cursor.executescript(SCHEMA)
    print("✅ Esquema creado.")

    # --- DATOS DE PRUEBA: PROFESORES ---
    profesores = [
        ('elfar_morantes', '123', 'ELFAR DIDIER MORANTES SANCHEZ', 'profesor', 'elfar.morantes@uninpahu.edu.co'),
        ('dakar_sarmiento', '123', 'DAKAR SARMIENTO', 'profesor', 'dakar.sarmiento@uninpahu.edu.co')
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role, email) VALUES (?,?,?,?,?)", profesores)
    
    # --- DATOS DE PRUEBA: SEDES Y SALONES ---
    cursor.execute("INSERT INTO campuses (name, latitude, longitude, radius_meters) VALUES ('Sede Principal UNINPAHU', 4.6300, -74.0700, 200)")
    cursor.execute("INSERT INTO rooms (code, campus_id) VALUES ('LAB-301', 1)")
    
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
    print("🚀 BASE DE DATOS RESTAURADA CON ÉXITO. Sistema listo para pruebas.")

if __name__ == '__main__':
    restore_database()
