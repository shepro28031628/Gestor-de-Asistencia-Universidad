import sqlite3
import os

# 1. EL ESQUEMA (Directo aquí para evitar errores de importación)
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
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, role TEXT, program_id INTEGER, profile_pic TEXT);
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
    db_path = 'Backend/asistencia.db'
    print(f"🛠️ Restaurando base de datos en: {os.path.abspath(db_path)}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar esquema
    cursor.executescript(SCHEMA)
    print("✅ Esquema creado.")

    # 2. INSERTAR PROFESORES
    profesores = [
        ('elfar_morantes', '123', 'ELFAR DIDIER MORANTES SANCHEZ', 'profesor'),
        ('dakar_sarmiento', '123', 'DAKAR SARMIENTO', 'profesor')
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role) VALUES (?,?,?,?)", profesores)
    
    # 3. INSERTAR MATERIAS Y GRUPOS (Datos de Ulises)
    # Machine Learning (Sabatino)
    cursor.execute("INSERT INTO subjects (code, name) VALUES ('IS1791', 'MACHINE LEARNING Y DEEP LEARNING')")
    sub_ml = cursor.lastrowid
    cursor.execute("INSERT INTO groups (group_number, subject_id, teacher_id, start_date, end_date, jornada) VALUES ('750', ?, 1, '2026-02-02', '2026-05-30', 'Sabatino')", (sub_ml,))
    group_ml = cursor.lastrowid

    # Videojuegos (Diurno)
    cursor.execute("INSERT INTO subjects (code, name) VALUES ('IS1792', 'DESARROLLO DE VIDEOJUEGOS')")
    sub_vg = cursor.lastrowid
    cursor.execute("INSERT INTO groups (group_number, subject_id, teacher_id, start_date, end_date, jornada) VALUES ('750', ?, 2, '2026-02-02', '2026-05-30', 'Diurno')", (sub_vg,))
    group_vg = cursor.lastrowid

    # 4. INSERTAR HORARIOS
    # Sábados para Machine Learning (2 sesiones)
    cursor.execute("INSERT INTO schedules (group_id, room_id, day, start_time, end_time) VALUES (?, 1, 'S', '07:00', '10:00')", (group_ml,))
    cursor.execute("INSERT INTO schedules (group_id, room_id, day, start_time, end_time) VALUES (?, 1, 'S', '17:00', '19:00')", (group_ml,))
    # Miércoles para Videojuegos
    cursor.execute("INSERT INTO schedules (group_id, room_id, day, start_time, end_time) VALUES (?, 1, 'W', '14:15', '17:15')", (group_vg,))

    # 5. INSERTAR ESTUDIANTES
    estudiantes = [
        ('202518003330', '123', 'ESTUDIANTE MASTER', 'estudiante'),
        ('2025100001', '123', 'OLIVIA FLORES', 'estudiante')
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role) VALUES (?,?,?,?)", estudiantes)
    
    # Inscribir a los estudiantes en las materias
    cursor.execute("SELECT id FROM users WHERE role='estudiante'")
    student_ids = [s[0] for s in cursor.fetchall()]
    cursor.execute("SELECT id FROM groups")
    group_ids = [g[0] for g in cursor.fetchall()]
    
    for sid in student_ids:
        for gid in group_ids:
            cursor.execute("INSERT INTO enrollments (student_id, group_id) VALUES (?, ?)", (sid, gid))

    conn.commit()
    conn.close()
    print("🚀 BASE DE DATOS RESTAURADA CON ÉXITO. Ya puedes iniciar sesión.")

if __name__ == '__main__':
    restore_database()
