import os
import datetime
import segno
import csv
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

# Importar componentes de la arquitectura
from config import LAT_TEST, LON_TEST, RADIO_MAXIMO_METROS, HORARIO_ESTUDIANTE
from services.geo_service import calcular_distancia
from models import session_manager

app = Flask(__name__)
app.secret_key = "uninpahu_secret_key_2024" # Necesaria para sesiones

@app.route('/')
def index():
    # Si ya está logueado, redirigir a su panel
    if session.get('logged_in'):
        return redirect(url_for(session.get('role')))
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')

    # Credenciales de prueba
    USERS = {
        "estudiante": {"user": "estudiante", "pass": "123"},
        "profesor": {"user": "docente", "pass": "123"}
    }

    if role in USERS and username == USERS[role]["user"] and password == USERS[role]["pass"]:
        session['logged_in'] = True
        session['role'] = role # 'estudiante' o 'profesor' (coincide con nombres de función)
        session['username'] = username
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Usuario o contraseña incorrectos."})

@app.route('/estudiante')
def estudiante():
    # Solo estudiantes permitidos
    if not session.get('logged_in') or session.get('role') != 'estudiante':
        return redirect(url_for('index'))
    return render_template('estudiante.html', horario=HORARIO_ESTUDIANTE)

@app.route('/profesor')
def profesor():
    # Solo docentes permitidos
    if not session.get('logged_in') or session.get('role') != 'profesor':
        return redirect(url_for('index'))
    from config import MATERIAS_DISPONIBLES, HORARIO_ESTUDIANTE
    return render_template('profesor.html', materias=MATERIAS_DISPONIBLES, horario=HORARIO_ESTUDIANTE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/generar-clase', methods=['POST'])
def api_generar_clase():
    """El docente activa la clase, validando su ubicación y seleccionando la materia."""
    data = request.json
    lat_profesor = data.get('lat')
    lng_profesor = data.get('lng')
    materia = data.get('materia')

    if not materia:
        return jsonify({"success": False, "error": "Debes seleccionar una materia."})

    distancia = calcular_distancia(lat_profesor, lng_profesor, LAT_TEST, LON_TEST)
    if distancia > RADIO_MAXIMO_METROS:
        return jsonify({
            "success": False, 
            "error": f"Docente fuera de rango ({int(distancia)}m). Recibido: {lat_profesor}, {lng_profesor}"
        })

    ahora = datetime.datetime.now()
    expiracion = ahora + datetime.timedelta(minutes=15)
    token_clase = f"CLASE_{int(ahora.timestamp())}"
    
    # El token ahora incluye información de la materia
    payload_clase = {"token": token_clase, "type": "CLASS_AUTH", "materia": materia}
    
    qr = segno.make(str(payload_clase))
    qr_path = "static/qrs/qr_clase.png"
    qr.save(qr_path, scale=10)

    session_manager.set_sesion(token_clase, expiracion, materia)

    return jsonify({
        "success": True,
        "qr_url": "/" + qr_path + "?v=" + str(int(ahora.timestamp())),
        "expiracion": int(expiracion.timestamp() * 1000)
    })

@app.route('/api/docente-escanea-alumno', methods=['POST'])
def api_docente_escanea_alumno():
    """El docente escanea el carnet del alumno."""
    data = request.json
    student_id = data.get('student_id')

    if not session_manager.is_sesion_valid():
        return jsonify({"success": False, "error": "La sesión de clase no está activa o expiró."})

    if session_manager.is_student_scanned(student_id):
        return jsonify({"success": False, "error": "Este estudiante ya fue escaneado en esta sesión."})

    session_manager.add_scanned_student(student_id)
    print(f"VALIDACIÓN 1/2: Docente escaneó carnet de {student_id}")
    return jsonify({"success": True})

@app.route('/api/estudiante-escanea-clase', methods=['POST'])
def api_estudiante_escanea_clase():
    """El estudiante escanea el QR de la clase. Solo funciona si es su materia."""
    data = request.json
    qr_data_str = data.get('qr_data')
    lat_estudiante = data.get('lat')
    lng_estudiante = data.get('lng')
    materia_seleccionada = data.get('materia')
    student_id = "EST-UNINPAHU-2024-001" # Simulado para pruebas

    # 1. Validar ubicación del estudiante
    distancia = calcular_distancia(lat_estudiante, lng_estudiante, LAT_TEST, LON_TEST)
    if distancia > RADIO_MAXIMO_METROS:
        return jsonify({"success": False, "error": "Estudiante fuera de rango."})

    # 2. Validar token y materia
    try:
        import ast
        payload = ast.literal_eval(qr_data_str)
        token_escaneado = payload.get("token")
        materia_clase = payload.get("materia")
    except:
        return jsonify({"success": False, "error": "QR de clase inválido."})

    if not session_manager.is_sesion_valid(token_escaneado):
        return jsonify({"success": False, "error": "QR de clase expirado."})

    # 3. Validar coincidencia de materia seleccionada vs activa
    if materia_seleccionada != materia_clase:
        return jsonify({
            "success": False, 
            "error": f"Error: Has seleccionado '{materia_seleccionada}', pero esta clase es de '{materia_clase}'."
        })

    # 3. Validar que el estudiante tenga esa materia en su horario
    tiene_materia = any(h['materia'] == materia_clase for h in HORARIO_ESTUDIANTE)
    if not tiene_materia:
        return jsonify({
            "success": False, 
            "error": f"No tienes la materia '{materia_clase}' registrada en tu horario."
        })

    # Guardar asistencia persistente
    from models import attendance_manager
    
    if attendance_manager.is_already_registered(student_id, materia_clase):
        return jsonify({"success": False, "error": "Ya has registrado tu asistencia para esta materia hoy."})
        
    attendance_manager.save_attendance(student_id, materia_clase)

    print(f"VALIDACIÓN 2/2: Estudiante {student_id} validó asistencia para {materia_clase}")
    return jsonify({"success": True})

@app.route('/api/historial-estudiante')
def api_historial_estudiante():
    from models import attendance_manager
    return jsonify(attendance_manager.get_all_attendance())

@app.route('/api/alertas-desercion')
def api_alertas_desercion():
    materia = request.args.get('materia')
    if not materia:
        return jsonify([])
    from models import attendance_manager
    return jsonify(attendance_manager.get_desertion_alerts(materia))

@app.route('/api/upload-lista', methods=['POST'])
def api_upload_lista():
    if session.get('role') != 'profesor':
        return jsonify({"success": False, "error": "No autorizado"}), 403
    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No hay archivo"})
    
    file = request.files['file']
    materia = request.form.get('materia')
    
    if file.filename == '':
        return jsonify({"success": False, "error": "Nombre de archivo vacío"})

    try:
        content = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(content)
        
        # Cargar base actual
        student_file = "data/estudiantes_materia.json"
        all_students = []
        if os.path.exists(student_file):
            with open(student_file, 'r') as f:
                all_students = json.load(f)
        
        for row in reader:
            sid = row.get('student_id')
            name = row.get('name')
            if sid and name:
                # Buscar si ya existe
                student = next((s for s in all_students if s['student_id'] == sid), None)
                if student:
                    if materia not in student['materias']:
                        student['materias'].append(materia)
                else:
                    all_students.append({
                        "student_id": sid,
                        "name": name,
                        "materias": [materia]
                    })
        
        with open(student_file, 'w') as f:
            json.dump(all_students, f, indent=4)
            
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# --- JUSTIFICACIONES Y FEEDBACK ---
@app.route('/api/upload-excusa', methods=['POST'])
def api_upload_excusa():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No hay archivo"})
    
    file = request.files['file']
    student_id = session.get('username')
    materia = request.form.get('materia')
    fecha_falta = request.form.get('fecha_falta') # Formato YYYY-MM-DD

    if file and student_id:
        filename = secure_filename(f"excusa_{student_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        if not os.path.exists('static/excusas'):
            os.makedirs('static/excusas')
        file.save(os.path.join('static/excusas', filename))
        
        # Guardar registro de excusa
        excusas_file = "data/excusas.json"
        excusas = []
        if os.path.exists(excusas_file):
            with open(excusas_file, 'r') as f:
                excusas = json.load(f)
        
        excusas.append({
            "student_id": student_id,
            "materia": materia,
            "fecha_falta": fecha_falta,
            "archivo": filename,
            "status": "pendiente",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        with open(excusas_file, 'w') as f:
            json.dump(excusas, f, indent=4)
            
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Error al procesar"})

@app.route('/api/get-excusas-docente')
def api_get_excusas_docente():
    if session.get('role') != 'profesor':
        return jsonify({"success": False, "error": "No autorizado"}), 403
        
    excusas_file = "data/excusas.json"
    if os.path.exists(excusas_file):
        with open(excusas_file, 'r') as f:
            try:
                return jsonify(json.load(f))
            except:
                return jsonify([])
    return jsonify([])

@app.route('/api/aprobar-excusa', methods=['POST'])
def api_aprobar_excusa():
    if session.get('role') != 'profesor':
        return jsonify({"success": False, "error": "No autorizado"}), 403
        
    data = request.json
    student_id = data.get('student_id')
    timestamp = data.get('timestamp')
    
    excusas_file = "data/excusas.json"
    if os.path.exists(excusas_file):
        with open(excusas_file, 'r') as f:
            excusas = json.load(f)
        
        for e in excusas:
            if e['student_id'] == student_id and e['timestamp'] == timestamp:
                e['status'] = "aprobada"
                break
        
        with open(excusas_file, 'w') as f:
            json.dump(excusas, f, indent=4)
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/enviar-feedback', methods=['POST'])
def api_enviar_feedback():
    if not session.get('logged_in'):
        return jsonify({"success": False, "error": "No autorizado"}), 403
        
    data = request.json
    student_id = session.get('username')
    materia = data.get('materia')
    estrellas = data.get('estrellas')
    
    feedback_file = "data/feedback.json"
    feedbacks = []
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedbacks = json.load(f)
            
    feedbacks.append({
        "student_id": student_id,
        "materia": materia,
        "estrellas": estrellas,
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(feedback_file, 'w') as f:
        json.dump(feedbacks, f, indent=4)
    return jsonify({"success": True})

@app.route('/api/get-feedback-stats')
def api_get_feedback_stats():
    if session.get('role') != 'profesor':
        return jsonify({"success": False, "error": "No autorizado"}), 403
        
    materia = request.args.get('materia')
    feedback_file = "data/feedback.json"
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            try:
                feedbacks = json.load(f)
            except:
                feedbacks = []
                
            if materia:
                feedbacks = [f for f in feedbacks if f['materia'] == materia]
            
            if not feedbacks: return jsonify({"avg": 0, "count": 0})
            
            avg = sum(f['estrellas'] for f in feedbacks) / len(feedbacks)
            return jsonify({"avg": round(avg, 1), "count": len(feedbacks)})
    return jsonify({"avg": 0, "count": 0})

if __name__ == '__main__':
    if not os.path.exists('static/qrs'):
        os.makedirs('static/qrs')
    app.run(debug=True, port=5000)