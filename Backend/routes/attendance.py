import math
import uuid
import smtplib
import threading
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, request, jsonify
from database import get_db

attendance_bp = Blueprint('attendance', __name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en metros entre dos puntos geográficos (Lat/Lng)
    utilizando la fórmula de Haversine. Crucial para la geocerca.
    """
    R = 6371000 # Radio de la Tierra en metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_dia_code(date_obj):
    """Convierte el día de la semana de Python al formato de la DB (M, T, W, R, F, S, U)"""
    mapping = {0: "M", 1: "T", 2: "W", 3: "R", 4: "F", 5: "S", 6: "U"}
    return mapping.get(date_obj.weekday())

@attendance_bp.route('/progreso/<username>', methods=['GET'])
def get_progreso_estudiante(username):
    """
    Calcula el porcentaje de asistencia del alumno basándose en las semanas 
    transcurridas y las clases que debió haber tenido.
    """
    with get_db() as conn:
        # Consulta que cruza inscripciones, grupos y asistencias registradas
        query = '''
            SELECT s.name as materia, g.start_date, g.end_date, g.id as group_id,
            (SELECT COUNT(*) FROM schedules WHERE group_id = g.id) as sesiones_semanales,
            (SELECT COUNT(*) FROM attendances a 
             JOIN class_sessions cs ON a.session_id = cs.id 
             JOIN users u ON a.student_id = u.id 
             JOIN schedules sch ON cs.schedule_id = sch.id
             WHERE u.username = ? AND sch.group_id = g.id) as asistencias
            FROM users u
            JOIN enrollments e ON u.id = e.student_id
            JOIN groups g ON e.group_id = g.id
            JOIN subjects s ON g.subject_id = s.id
            WHERE u.username = ?
        '''
        results = conn.execute(query, (username, username)).fetchall()
        progreso = []
        for r in results:
            try:
                # Cálculo matemático de clases esperadas vs reales
                start = datetime.strptime(r['start_date'], "%Y-%m-%d")
                end = datetime.strptime(r['end_date'], "%Y-%m-%d")
                semanas = max(1, math.ceil((end - start).days / 7))
                total_esperado = max(1, semanas * r['sesiones_semanales'])
                porcentaje = int((r['asistencias'] / total_esperado) * 100)
            except:
                # Valores por defecto en caso de datos de fecha corruptos
                total_esperado, porcentaje, semanas = 16, 0, 16
            progreso.append({"materia": r['materia'], "porcentaje": min(100, porcentaje), "asistencias": r['asistencias'], "total": total_esperado, "semanas": semanas})
        return jsonify(progreso)

@attendance_bp.route('/historial', methods=['GET'])
def get_historial():
    """Obtiene el historial global de asistencias. Maneja casos de tabla vacía."""
    try:
        with get_db() as conn:
            query = '''
                SELECT a.status, a.timestamp as fecha, u.full_name as student_name, sub.name as materia 
                FROM attendances a 
                JOIN users u ON a.student_id = u.id 
                JOIN class_sessions cs ON a.session_id = cs.id 
                JOIN schedules sch ON cs.schedule_id = sch.id 
                JOIN groups g ON sch.group_id = g.id 
                JOIN subjects sub ON g.subject_id = sub.id 
                ORDER BY a.timestamp DESC
            '''
            rows = conn.execute(query).fetchall()
            return jsonify([dict(row) for row in rows])
    except Exception as e:
        print(f"Error en historial: {e}")
        return jsonify([]) # Devolver lista vacía en lugar de error 500

@attendance_bp.route('/marcar', methods=['POST'])
def marcar_asistencia():
    """
    Endpoint principal para estudiantes. Valida:
    1. Token QR activo. 2. Horario de clase. 3. Ubicación GPS. 4. Unicidad.
    """
    data = request.json
    with get_db() as conn:
        # Recuperamos la sesión y los parámetros de ubicación de la sede
        session = conn.execute('SELECT cs.id, c.latitude, c.longitude, c.radius_meters, cs.expires_at, sch.day FROM class_sessions cs JOIN schedules sch ON cs.schedule_id = sch.id JOIN rooms r ON sch.room_id = r.id JOIN campuses c ON r.campus_id = c.id WHERE cs.qr_token = ? AND cs.is_active = 1', (data.get('token'),)).fetchone()
        
        if not session: return jsonify({"success": False, "message": "QR inválido"}), 400
        
        # Validación de Tiempo y Día
        now = datetime.now()
        if session['day'] != get_dia_code(now) or now > datetime.fromisoformat(session['expires_at']):
            return jsonify({"success": False, "message": "QR fuera de tiempo o día"}), 403
        
        # GEOFENCING: Validación de ubicación física
        distancia = haversine_distance(data.get('lat'), data.get('lng'), session['latitude'], session['longitude'])
        if distancia > session['radius_meters'] and session['latitude'] != 0:
            return jsonify({"success": False, "message": "Fuera de rango"}), 403
            
        try:
            # Registro oficial en la base de datos
            conn.execute('INSERT INTO attendances (student_id, session_id, lat, lng, distance_to_campus) VALUES (?, ?, ?, ?, ?)', 
                         (data.get('student_id'), session['id'], data.get('lat'), data.get('lng'), distancia))
            conn.commit()
            return jsonify({"success": True, "message": "Asistencia exitosa"})
        except: 
            # Evita duplicados (Un estudiante no puede marcar dos veces la misma sesión)
            return jsonify({"success": False, "message": "Ya marcaste asistencia"}), 500

@attendance_bp.route('/activar', methods=['POST'])
def activar_clase():
    """
    Activa manualmente una sesión de clase. 
    Invalida tokens previos para asegurar que solo el nuevo sea válido.
    """
    data = request.json
    now = datetime.now()
    schedule_id = data.get('schedule_id')
    
    with get_db() as conn:
        # SEGURIDAD: Desactivamos tokens anteriores del mismo horario para evitar fraude
        conn.execute('UPDATE class_sessions SET is_active = 0 WHERE schedule_id = ? AND is_active = 1', (schedule_id,))
        
        # Generación de identificador único (UUID)
        token = str(uuid.uuid4())
        expires_at = (now + timedelta(minutes=15)).isoformat() # Ventana de 15 min de validez
        
        conn.execute('INSERT INTO class_sessions (schedule_id, qr_token, expires_at, is_active) VALUES (?, ?, ?, 1)', 
                    (schedule_id, token, expires_at))
        conn.commit()
        
        return jsonify({
            "success": True, 
            "token": token, 
            "expires_at_ms": int((now + timedelta(minutes=15)).timestamp() * 1000)
        })

@attendance_bp.route('/token-vivo/<schedule_id>', methods=['GET'])
def get_token_vivo(schedule_id):
    """
    Implementa la ROTACIÓN VIVA: Genera un nuevo token cada 15 segundos
    pero mantiene válidos los anteriores por 60 segundos (Ventana de Gracia).
    """
    now = datetime.now()
    with get_db() as conn:
        # 1. LIMPIEZA: Solo desactivamos tokens que tengan más de 1 minuto (Margen para el estudiante)
        limite_gracia = (now - timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute('UPDATE class_sessions SET is_active = 0 WHERE schedule_id = ? AND created_at < ? AND is_active = 1', (schedule_id, limite_gracia))
        
        # 2. ROTACIÓN: Buscamos si ya se generó uno en los últimos 15 segundos
        limite_rotacion = (now - timedelta(seconds=15)).strftime("%Y-%m-%d %H:%M:%S")
        reciente = conn.execute('SELECT qr_token FROM class_sessions WHERE schedule_id = ? AND created_at >= ? AND is_active = 1 ORDER BY created_at DESC', (schedule_id, limite_rotacion)).fetchone()
        
        if reciente:
            return jsonify({"token": reciente['qr_token']})
        
        # 3. Si no hay token fresco, creamos el siguiente eslabón de la cadena
        nuevo_token = str(uuid.uuid4())
        expires_at = (now + timedelta(minutes=15)).isoformat()
        conn.execute('INSERT INTO class_sessions (schedule_id, qr_token, expires_at, is_active) VALUES (?, ?, ?, 1)', (schedule_id, nuevo_token, expires_at))
        conn.commit()
        return jsonify({"token": nuevo_token})

@attendance_bp.route('/finalizar', methods=['POST'])
def finalizar_clase():
    """Cierra la sesión y envía reporte al docente."""
    data = request.json
    schedule_id = data.get('schedule_id')
    
    with get_db() as conn:
        # 1. Obtener datos del reporte
        query_info = '''
            SELECT s.name as materia, u.full_name as profesor, u.email, r.code as salon
            FROM schedules sch
            JOIN groups g ON sch.group_id = g.id
            JOIN subjects s ON g.subject_id = s.id
            JOIN users u ON g.teacher_id = u.id
            JOIN rooms r ON sch.room_id = r.id
            WHERE sch.id = ?
        '''
        info = conn.execute(query_info, (schedule_id,)).fetchone()
        if not info: return jsonify({"success": False, "message": "Horario no encontrado"}), 404
        
        # 2. Obtener lista de asistentes
        query_asistentes = '''
            SELECT u.full_name, u.username, a.timestamp, a.status
            FROM attendances a
            JOIN users u ON a.student_id = u.id
            JOIN class_sessions cs ON a.session_id = cs.id
            WHERE cs.schedule_id = ? AND date(cs.created_at) = date("now")
            ORDER BY u.full_name ASC
        '''
        asistentes = conn.execute(query_asistentes, (schedule_id,)).fetchall()
        
        # 3. Inactivar sesión
        conn.execute('UPDATE class_sessions SET is_active = 0 WHERE schedule_id = ?', (schedule_id,))
        conn.commit()
        
        # 4. Generar y enviar correo (Simulado/Configurable)
        if info['email']:
            enviar_reporte_email(info, asistentes)
            
        return jsonify({
            "success": True, 
            "message": "Clase finalizada y reporte enviado",
            "count": len(asistentes)
        })

def cerrar_sesion_y_reportar(conn, schedule_id):
    """Lógica centralizada de cierre para uso manual y automático."""
    # 1. Obtener datos del reporte
    query_info = '''
        SELECT s.name as materia, u.full_name as profesor, u.email, r.code as salon
        FROM schedules sch
        JOIN groups g ON sch.group_id = g.id
        JOIN subjects s ON g.subject_id = s.id
        JOIN users u ON g.teacher_id = u.id
        JOIN rooms r ON sch.room_id = r.id
        WHERE sch.id = ?
    '''
    info = conn.execute(query_info, (schedule_id,)).fetchone()
    if not info: return
    
    # 2. Obtener asistentes
    query_asistentes = '''
        SELECT u.full_name, u.username, a.timestamp, a.status
        FROM attendances a
        JOIN users u ON a.student_id = u.id
        JOIN class_sessions cs ON a.session_id = cs.id
        WHERE cs.schedule_id = ? AND date(cs.created_at) = date("now")
        ORDER BY u.full_name ASC
    '''
    asistentes = conn.execute(query_asistentes, (schedule_id,)).fetchall()
    
    # 3. Inactivar
    conn.execute('UPDATE class_sessions SET is_active = 0 WHERE schedule_id = ?', (schedule_id,))
    conn.commit()
    
    # 4. Reportar
    if info['email']:
        enviar_reporte_email(info, asistentes)

def monitor_de_horarios(app_context):
    """
    PROCESO EN SEGUNDO PLANO (THREAD):
    Verifica cada minuto si alguna clase activa ya llegó a su hora de fin.
    Si es así, dispara el auto-cierre y el envío de reporte por email.
    """
    with app_context:
        print("Monitor de Horarios Iniciado (Auto-Cierre)")
        while True:
            try:
                now = datetime.now()
                hora_actual = now.strftime("%H:%M")
                dia_actual = get_dia_code(now)
                
                with get_db() as conn:
                    # Buscamos sesiones cuya hora de fin (end_time) sea menor o igual a la actual
                    query_expirados = '''
                        SELECT cs.schedule_id 
                        FROM class_sessions cs
                        JOIN schedules sch ON cs.schedule_id = sch.id
                        WHERE cs.is_active = 1 
                        AND sch.day = ? 
                        AND sch.end_time <= ?
                    '''
                    expirados = conn.execute(query_expirados, (dia_actual, hora_actual)).fetchall()
                    
                    for row in expirados:
                        print(f"Auto-Cierre ejecutado para horario ID: {row['schedule_id']}")
                        cerrar_sesion_y_reportar(conn, row['schedule_id'])
            except Exception as e:
                print(f"Error en monitor: {e}")
            time.sleep(60) # Pausa de 1 minuto entre verificaciones

def iniciar_monitor(app):
    """Lanzador del hilo daemon para el monitor."""
    threading.Thread(target=monitor_de_horarios, args=(app.app_context(),), daemon=True).start()

def enviar_reporte_email(info, asistentes):
    """
    Genera un cuerpo HTML con la tabla de asistentes y lo envía 
    al correo electrónico del profesor mediante SMTP.
    """
    msg = MIMEMultipart()
    msg['From'] = "sistema.asistencia@uninpahu.edu.co"
    msg['To'] = info['email']
    msg['Subject'] = f"Reporte de Asistencia: {info['materia']} - {datetime.now().strftime('%d/%m/%Y')}"
    
    # Construcción dinámica de la tabla HTML
    html = f"""
    <html>
        <body style="font-family: sans-serif; color: #002B49;">
            <h2 style="color: #FF4D00;">Reporte de Asistencia Académica</h2>
            <p><b>Materia:</b> {info['materia']}<br>
            <b>Docente:</b> {info['profesor']}<br>
            <b>Salón:</b> {info['salon']}<br>
            <b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #002B49; color: white;">
                    <th>Estudiante</th>
                    <th>Código</th>
                    <th>Hora</th>
                    <th>Estado</th>
                </tr>
    """
    for a in asistentes:
        html += f"<tr><td>{a['full_name']}</td><td>{a['username']}</td><td>{a['timestamp']}</td><td>{a['status']}</td></tr>"
    
    html += "</table><p><i>Generado automáticamente por UNINPAHU Asistencia.</i></p></body></html>"
    msg.attach(MIMEText(html, 'html'))
    
    # NOTA: Para habilitar el envío real, descomenta y configura las líneas de abajo
    # try:
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.starttls()
    #     server.login("tu_correo@gmail.com", "TU_APP_PASSWORD")
    #     server.send_message(msg)
    #     server.quit()
    # except Exception as e:
    #     print(f"Error enviando correo: {e}")
    print(f"📧 SIMULACIÓN: Reporte enviado a {info['email']}")

@attendance_bp.route('/horario/<username>', methods=['GET'])
def get_horario(username):
    with get_db() as conn:
        user = conn.execute('SELECT id, role FROM users WHERE username = ?', (username,)).fetchone()
        if not user: return jsonify([]), 404
        if user['role'] == 'profesor':
            query = 'SELECT sch.id as schedule_id, s.name as materia, r.code as aula, sch.day, sch.start_time, sch.end_time, (SELECT COUNT(*) FROM enrollments WHERE group_id = g.id) as inscritos FROM users u JOIN groups g ON u.id = g.teacher_id JOIN subjects s ON g.subject_id = s.id JOIN schedules sch ON g.id = sch.group_id JOIN rooms r ON sch.room_id = r.id WHERE u.username = ?'
        else:
            query = '''
            SELECT s.id as schedule_id, sub.name as materia, s.day, s.start_time, s.end_time,
            r.code as salon, c.name as sede
            FROM schedules s
            JOIN groups g ON s.group_id = g.id
            JOIN subjects sub ON g.subject_id = sub.id
            JOIN enrollments e ON g.id = e.group_id
            JOIN users u ON e.student_id = u.id
            JOIN rooms r ON s.room_id = r.id
            JOIN campuses c ON r.campus_id = c.id
            WHERE u.username = ?
        '''
        return jsonify([dict(ix) for ix in conn.execute(query, (username,)).fetchall()])

@attendance_bp.route('/sesiones-activas/<username>', methods=['GET'])
def get_sesiones_activas(username):
    with get_db() as conn:
        query = '''
            SELECT cs.id as session_id, sub.name as materia, r.code as salon, c.name as sede, cs.expires_at
            FROM class_sessions cs
            JOIN schedules s ON cs.schedule_id = s.id
            JOIN groups g ON s.group_id = g.id
            JOIN subjects sub ON g.subject_id = sub.id
            JOIN enrollments e ON g.id = e.group_id
            JOIN users u ON e.student_id = u.id
            JOIN rooms r ON s.room_id = r.id
            JOIN campuses c ON r.campus_id = c.id
            WHERE u.username = ? AND cs.is_active = 1
        '''
        results = conn.execute(query, (username,)).fetchall()
        activas = []
        now = datetime.now()
        for r in results:
            if now < datetime.fromisoformat(r['expires_at']): activas.append(dict(r))
        return jsonify(activas)

@attendance_bp.route('/estudiantes-sesion/<schedule_id>', methods=['GET'])
def get_estudiantes_sesion(schedule_id):
    """Lista de estudiantes inscritos en el grupo de este horario y su estado de asistencia hoy."""
    with get_db() as conn:
        # Obtenemos el group_id desde el schedule
        group = conn.execute('SELECT group_id FROM schedules WHERE id = ?', (schedule_id,)).fetchone()
        if not group: return jsonify([]), 404
        
        # Buscamos la sesión de clase de hoy para este horario
        session = conn.execute('SELECT id FROM class_sessions WHERE schedule_id = ? AND date(created_at) = date("now")', (schedule_id,)).fetchone()
        session_id = session['id'] if session else 0

        # Obtenemos estudiantes inscritos y cruzamos con asistencia
        query = '''
            SELECT u.id, u.full_name, u.username,
            (SELECT COUNT(*) FROM attendances a WHERE a.student_id = u.id AND a.session_id = ?) as asistio
            FROM users u
            JOIN enrollments e ON u.id = e.student_id
            WHERE e.group_id = ?
            ORDER BY u.full_name ASC
        '''
        estudiantes = conn.execute(query, (session_id, group['group_id'])).fetchall()
        return jsonify([dict(e) for e in estudiantes])

@attendance_bp.route('/marcar-manual', methods=['POST'])
def marcar_manual():
    """Registro de asistencia por parte del docente."""
    data = request.json
    student_id = data.get('student_id')
    schedule_id = data.get('schedule_id')
    
    with get_db() as conn:
        # Aseguramos que exista una sesión de clase para hoy
        session = conn.execute('SELECT id FROM class_sessions WHERE schedule_id = ? AND date(created_at) = date("now")', (schedule_id,)).fetchone()
        if not session:
            # Si no hay sesión, la creamos (por si el profesor quiere marcar antes de activar el QR)
            now = datetime.now()
            token = f"MANUAL-{uuid.uuid4().hex[:6].upper()}"
            expires = (now + timedelta(minutes=60)).isoformat()
            cursor = conn.execute('INSERT INTO class_sessions (schedule_id, qr_token, expires_at, is_active) VALUES (?, ?, ?, 1)', 
                                (schedule_id, token, expires))
            session_id = cursor.lastrowid
        else:
            session_id = session['id']

        try:
            conn.execute('INSERT INTO attendances (student_id, session_id, status) VALUES (?, ?, "manual")', 
                        (student_id, session_id))
            conn.commit()
            return jsonify({"success": True, "message": "Asistencia registrada"})
        except:
            return jsonify({"success": False, "message": "Ya tiene asistencia"})

import os
from werkzeug.utils import secure_filename

# RUTA UNIFICADA CON FRONTEND
UPLOAD_FOLDER = os.path.abspath(os.path.join('Frontend', 'static', 'uploads'))

@attendance_bp.route('/subir-justificacion', methods=['POST'])
def subir_justificacion():
    """Recibe y guarda el documento de soporte del estudiante."""
    if 'file' not in request.files: return jsonify({"success": False, "message": "No hay archivo"}), 400
    
    file = request.files['file']
    student_id = request.form.get('student_id')
    schedule_id = request.form.get('schedule_id')

    if file.filename == '': return jsonify({"success": False, "message": "Archivo vacío"}), 400

    filename = secure_filename(f"excusa_{student_id}_{schedule_id}_{file.filename}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    with get_db() as conn:
        conn.execute('INSERT INTO justifications (student_id, schedule_id, file_path) VALUES (?, ?, ?)', 
                    (student_id, schedule_id, f"/static/uploads/{filename}"))
        conn.commit()

    return jsonify({"success": True, "message": "Soporte subido correctamente"})

@attendance_bp.route('/get-justificaciones-docente', methods=['GET'])
def get_justificaciones_docente():
    """Lista las justificaciones de los estudiantes para el docente."""
    with get_db() as conn:
        query = '''
            SELECT j.id, u.full_name as student_name, sub.name as materia, j.file_path, j.timestamp, j.status
            FROM justifications j
            JOIN users u ON j.student_id = u.id
            JOIN schedules sch ON j.schedule_id = sch.id
            JOIN groups g ON sch.group_id = g.id
            JOIN subjects sub ON g.subject_id = sub.id
            ORDER BY j.timestamp DESC
        '''
        rows = conn.execute(query).fetchall()
        return jsonify([dict(row) for row in rows])

@attendance_bp.route('/historial-docente/<username>', methods=['GET'])
def get_historial_docente(username):
    """Obtiene el resumen de sesiones pasadas del profesor con conteo de asistencia."""
    with get_db() as conn:
        query = '''
            SELECT cs.id, s.name as materia, cs.created_at as fecha,
            (SELECT COUNT(*) FROM attendances a WHERE a.session_id = cs.id) as presentes,
            (SELECT COUNT(*) FROM enrollments e WHERE e.group_id = g.id) as inscritos
            FROM class_sessions cs
            JOIN schedules sch ON cs.schedule_id = sch.id
            JOIN groups g ON sch.group_id = g.id
            JOIN subjects s ON g.subject_id = s.id
            JOIN users u ON g.teacher_id = u.id
            WHERE u.username = ?
            ORDER BY cs.created_at DESC
        '''
        rows = conn.execute(query, (username,)).fetchall()
        return jsonify([dict(row) for row in rows])
@attendance_bp.route('/crear-citacion', methods=['POST'])
def crear_citacion():
    """Registra una nueva citación para un estudiante en riesgo."""
    data = request.json
    with get_db() as conn:
        conn.execute('INSERT INTO citations (teacher_id, student_id, message) VALUES (?, ?, ?)',
                    (data['teacher_id'], data['student_id'], "Revisión de asistencia crítica"))
        conn.commit()
    return jsonify({"success": True, "message": "Citación enviada con éxito"})

@attendance_bp.route('/get-citaciones/<student_id>', methods=['GET'])
def get_citaciones(student_id):
    """Obtiene las citaciones activas para el estudiante."""
    with get_db() as conn:
        query = '''
            SELECT c.id, u.full_name as teacher_name, c.timestamp 
            FROM citations c 
            JOIN users u ON c.teacher_id = u.id 
            WHERE c.student_id = ? AND c.status = 'activa'
        '''
        rows = conn.execute(query, (student_id,)).fetchall()
        return jsonify([dict(r) for r in rows])
