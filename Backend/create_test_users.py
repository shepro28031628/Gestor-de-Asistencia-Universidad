import sqlite3
from datetime import datetime, timedelta

def create_test_users():
    conn = sqlite3.connect('Backend/asistencia.db')
    cursor = conn.cursor()

    # 1. Crear Programa Académico si no existe
    cursor.execute("INSERT OR IGNORE INTO academic_programs (name, code) VALUES ('Ingeniería de Pruebas', 'IP001')")
    prog_id = cursor.execute("SELECT id FROM academic_programs WHERE code = 'IP001'").fetchone()[0]

    # 2. Crear Profesor
    # Username: profe_test, Pass: 123
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role, program_id)
        VALUES ('profe_test', '123', 'Profesor de Pruebas', 'profe@test.com', 'profesor', ?)
    """, (prog_id,))
    teacher_id = cursor.execute("SELECT id FROM users WHERE username = 'profe_test'").fetchone()[0]

    # 3. Crear Estudiante
    # Username: est_test, Pass: 123
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role, program_id, numero_doc)
        VALUES ('est_test', '123', 'Estudiante de Pruebas', 'est@test.com', 'estudiante', ?, '1000555')
    """, (prog_id,))
    student_id = cursor.execute("SELECT id FROM users WHERE username = 'est_test'").fetchone()[0]

    # 4. Crear Materia
    cursor.execute("INSERT OR IGNORE INTO subjects (code, name) VALUES ('TEST101', 'Materia de Pruebas')")
    subject_id = cursor.execute("SELECT id FROM subjects WHERE code = 'TEST101'").fetchone()[0]

    # 5. Crear Grupo (iniciado hace 4 semanas para forzar riesgo)
    four_weeks_ago = (datetime.now() - timedelta(weeks=4)).strftime('%Y-%m-%d')
    future_end = (datetime.now() + timedelta(weeks=12)).strftime('%Y-%m-%d')
    
    cursor.execute("""
        INSERT OR IGNORE INTO groups (group_number, subject_id, teacher_id, start_date, end_date, periodo_academico)
        VALUES ('G-TEST', ?, ?, ?, ?, '2026-1')
    """, (subject_id, teacher_id, four_weeks_ago, future_end))
    group_id = cursor.execute("SELECT id FROM groups WHERE group_number = 'G-TEST'").fetchone()[0]

    # 6. Inscribir Estudiante
    cursor.execute("INSERT OR IGNORE INTO enrollments (student_id, group_id) VALUES (?, ?)", (student_id, group_id))

    # 7. Crear Horario para HOY para que puedan probar activación
    # Obtener código del día actual
    days = ['U', 'M', 'T', 'W', 'R', 'F', 'S']
    today_code = days[datetime.now().weekday() if datetime.now().weekday() < 6 else 6]
    # En Python weekday() 0=Monday... 6=Sunday. 
    # El mapeo de la DB es M=Lunes, T=Martes, W=Miércoles, R=Jueves, F=Viernes, S=Sábado, U=Domingo.
    python_to_db = {0: 'M', 1: 'T', 2: 'W', 3: 'R', 4: 'F', 5: 'S', 6: 'U'}
    db_day = python_to_db[datetime.now().weekday()]

    cursor.execute("""
        INSERT OR IGNORE INTO schedules (group_id, room_id, day, start_time, end_time)
        VALUES (?, 1, ?, '06:00', '22:00')
    """, (group_id, db_day))

    # 8. Crear algunas sesiones pasadas SIN asistencia para que aparezca en RIESGO
    # El cálculo de riesgo mira: asistencias / (semanas * sesiones_semanales)
    # Al no insertar nada en 'attendances', el porcentaje será 0%.

    conn.commit()
    conn.close()
    print("Usuarios de prueba creados exitosamente.")
    print("Docente: profe_test / 123")
    print("Estudiante: est_test / 123")

if __name__ == "__main__":
    create_test_users()
