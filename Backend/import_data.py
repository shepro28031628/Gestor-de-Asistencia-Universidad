import sqlite3
import os
import xlrd

day_map = {
    'l': 'M', 'm': 'T', 'w': 'W', 'j': 'R', 'v': 'F', 's': 'S', 'd': 'U',
    'lunes': 'M', 'martes': 'T', 'miércoles': 'W', 'miercoles': 'W', 
    'jueves': 'R', 'viernes': 'F', 'sábado': 'S', 'sabado': 'S', 'domingo': 'U'
}

def clean_str(val):
    if isinstance(val, float):
        if val == int(val):
            return str(int(val)).strip()
        return str(val).strip()
    return str(val).strip()

def run_import():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'asistencia.db')
    xls_path = os.path.join(base_dir, '..', 'Estudiantes_Materias_Profesor_Aulas 21 - 03 - 2026 (1).xls')
    
    print(f"Leyendo archivo Excel: {xls_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    book = xlrd.open_workbook(xls_path, ignore_workbook_corruption=True)
    sheet = book.sheet_by_index(0)
    
    print(f"Procesando {sheet.nrows - 1} filas...")
    
    headers = [clean_str(h) for h in sheet.row_values(0)]
    
    # Sede por defecto
    cursor.execute("INSERT OR IGNORE INTO campuses (id, name, latitude, longitude) VALUES (1, 'Sede Principal', 4.6318, -74.0665)")
    
    def get_val(row, col_name, raw=False):
        try:
            idx = headers.index(col_name)
            return row[idx] if raw else clean_str(row[idx])
        except ValueError:
            return "" if not raw else None

    def parse_date(d_val):
        if not d_val: return ""
        if isinstance(d_val, float):
            try:
                dt_tuple = xlrd.xldate_as_tuple(d_val, book.datemode)
                return f"{dt_tuple[0]:04d}-{dt_tuple[1]:02d}-{dt_tuple[2]:02d}"
            except: pass
        return clean_str(d_val)

    def parse_time(t_val):
        if isinstance(t_val, float):
            seconds = int(t_val * 86400)
            hours, minutes = seconds // 3600, (seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        s = clean_str(t_val)
        return s[:5] if len(s) >= 5 else s
        
    for row_idx in range(1, sheet.nrows):
        row = sheet.row_values(row_idx)
        if not row: continue
        
        # Extracción dinámica
        cod_estudiante = get_val(row, 'NUMERO_DOC') # Este será el username (Login)
        codigo_carnet = get_val(row, 'CODIGO_ESTUDIANTE') # Guardamos el carnet aparte
        nom_estudiante = get_val(row, 'NOMBRE_COMPLETO')
        apellidos_est = get_val(row, 'APELLIDOS')
        nombres_est = get_val(row, 'NOMBRES')
        correo_estudiante = get_val(row, 'CORREO_INSTITUCIONAL')
        tipo_doc_est = get_val(row, 'TIPO_DOC')
        numero_doc_est = get_val(row, 'NUMERO_DOC')
        semestre_est = get_val(row, 'SEMESTRE')
        
        cod_profesor = get_val(row, 'NUMERO_DOC_DOCENTE')
        nom_profesor = get_val(row, 'NOMBRE_COMPLETO_PROFESOR')
        correo_profesor = get_val(row, 'CORREO_INSTITUCIONAL_PROFESOR')
        correo_pers_prof = get_val(row, 'CORREO_PERSONAL_PROFESOR')
        
        cod_materia = get_val(row, 'CODIGO_MATERIA')
        nom_materia = get_val(row, 'NOMBRE_MATERIA')
        
        cod_grupo = get_val(row, 'CODIGO_GRUPO')
        periodo_academico = get_val(row, 'PERIODO_ACADEMICO')
        grupo_semestre = get_val(row, 'GRUPO_SEMESTRE')
        intensidad = get_val(row, 'INTENSIDAD_HORARIA')
        
        dia_semana = get_val(row, 'DIA_SEMANA').lower()
        aula = get_val(row, 'AULA')
        capacidad_aula = get_val(row, 'CAPACIDAD_AULA')
        desc_aula = get_val(row, 'DESCRIPCION_AULA')
        disp_aula = get_val(row, 'DISPONIBILIDAD_AULA')
        cod_sede = get_val(row, 'CODIGO_SEDE')
        cod_tipo_clase = get_val(row, 'CODIGO_TIPO_CLASE')
        
        fecha_ini = parse_date(get_val(row, 'FECHA_INICIAL', raw=True))
        fecha_fin = parse_date(get_val(row, 'FECHA_FINAL', raw=True))
        
        # Programa académico
        tipo_prog = get_val(row, 'TIPO_PROGRAMA')
        nom_prog = get_val(row, 'NOMBRE_PROGRAMA')
        nom_facultad = get_val(row, 'NOMBRE_FACULTAD')
        sigla_facultad = get_val(row, 'SIGLA_FACULTAD')
        
        if not cod_estudiante or not cod_profesor or not cod_materia:
            continue
            
        # Programa
        prog_id = None
        if nom_prog:
            cursor.execute("SELECT id FROM academic_programs WHERE name = ?", (nom_prog,))
            p_res = cursor.fetchone()
            if not p_res:
                cursor.execute("INSERT INTO academic_programs (name, tipo_programa, nombre_facultad, sigla_facultad) VALUES (?, ?, ?, ?)",
                               (nom_prog, tipo_prog, nom_facultad, sigla_facultad))
                prog_id = cursor.lastrowid
            else:
                prog_id = p_res[0]
            
        # 1. Estudiante
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (username, password, full_name, apellidos, nombres, email, tipo_doc, numero_doc, codigo_carnet, semestre, role, program_id) 
            VALUES (?, '123', ?, ?, ?, ?, ?, ?, ?, ?, 'estudiante', ?)
        """, (cod_estudiante, nom_estudiante, apellidos_est, nombres_est, correo_estudiante, tipo_doc_est, numero_doc_est, codigo_carnet, semestre_est, prog_id))
        
        # 2. Docente
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (username, password, full_name, email, personal_email, role) 
            VALUES (?, '123', ?, ?, ?, 'profesor')
        """, (cod_profesor, nom_profesor, correo_profesor, correo_pers_prof))
        
        # Actualizar sede si no estaba
        if cod_sede:
            cursor.execute("UPDATE campuses SET codigo_sede = ? WHERE id = 1", (cod_sede,))
            
        # 3. Aula
        cursor.execute("SELECT id FROM rooms WHERE code = ?", (aula,))
        r_res = cursor.fetchone()
        if not r_res:
            cursor.execute("INSERT INTO rooms (code, capacidad, descripcion, disponibilidad, campus_id) VALUES (?, ?, ?, ?, 1)", 
                           (aula, capacidad_aula if capacidad_aula else 0, desc_aula, disp_aula))
            room_id = cursor.lastrowid
        else:
            room_id = r_res[0]
        
        # 4. Materia
        cursor.execute("INSERT OR IGNORE INTO subjects (code, name) VALUES (?, ?)", (cod_materia, nom_materia))
        
        # Obtener IDs
        cursor.execute("SELECT id FROM users WHERE username = ?", (cod_estudiante,))
        s_res = cursor.fetchone()
        student_id = s_res[0] if s_res else None
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (cod_profesor,))
        t_res = cursor.fetchone()
        teacher_id = t_res[0] if t_res else None
        
        cursor.execute("SELECT id FROM subjects WHERE code = ?", (cod_materia,))
        sub_res = cursor.fetchone()
        subject_id = sub_res[0] if sub_res else None
        
        if not (student_id and teacher_id and subject_id):
            continue
            
        # 5. Grupo
        cursor.execute("SELECT id FROM groups WHERE group_number = ? AND subject_id = ? AND teacher_id = ?", (cod_grupo, subject_id, teacher_id))
        g_res = cursor.fetchone()
        if not g_res:
            cursor.execute("""
                INSERT INTO groups (group_number, subject_id, teacher_id, periodo_academico, grupo_semestre, intensidad_horaria, start_date, end_date) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (cod_grupo, subject_id, teacher_id, periodo_academico, grupo_semestre, intensidad, fecha_ini, fecha_fin))
            group_id = cursor.lastrowid
        else:
            group_id = g_res[0]
            
        # 6. Inscripción
        cursor.execute("INSERT OR IGNORE INTO enrollments (student_id, group_id) VALUES (?, ?)", (student_id, group_id))
        
        # 7. Horarios
        mapped_day = day_map.get(dia_semana, 'M')
        
        # Obtener la hora inicial y final (usando raw=True para evitar que se vuelva string antes de tiempo)
        hora_ini_val = get_val(row, 'HORA_INICIAL', raw=True)
        hora_fin_val = get_val(row, 'HORA_FINAL', raw=True)
            
        hora_ini_str = parse_time(hora_ini_val)
        hora_fin_str = parse_time(hora_fin_val)
        
        if hora_ini_str and hora_fin_str:
            cursor.execute("SELECT id FROM schedules WHERE group_id = ? AND room_id = ? AND day = ? AND start_time = ?", 
                           (group_id, room_id, mapped_day, hora_ini_str))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO schedules (group_id, room_id, codigo_tipo_clase, day, start_time, end_time) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (group_id, room_id, cod_tipo_clase, mapped_day, hora_ini_str, hora_fin_str))
                           
    conn.commit()
    conn.close()
    print("\nMigración completada exitosamente.")

if __name__ == '__main__':
    run_import()
