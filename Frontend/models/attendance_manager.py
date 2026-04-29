import json
import os
from datetime import datetime

ATTENDANCE_FILE = "data/asistencias.json"

def save_attendance(student_id, materia):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    asistencias = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            try:
                asistencias = json.load(f)
            except:
                asistencias = []
    
    registro = {
        "student_id": student_id,
        "materia": materia,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    asistencias.append(registro)
    
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(asistencias, f, indent=4)
    
    return registro

def is_already_registered(student_id, materia):
    if not os.path.exists(ATTENDANCE_FILE):
        return False
    
    with open(ATTENDANCE_FILE, 'r') as f:
        try:
            asistencias = json.load(f)
            hoy = datetime.now().strftime("%Y-%m-%d")
            return any(a['student_id'] == student_id and a['materia'] == materia and a['fecha'].startswith(hoy) for a in asistencias)
        except:
            return False

def get_all_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            return json.load(f)
    return []

def get_desertion_alerts(materia_target):
    asistencias = get_all_attendance()
    
    # 1. Cargar base de estudiantes inscritos
    estudiantes_inscritos = []
    student_file = "data/estudiantes_materia.json"
    if os.path.exists(student_file):
        with open(student_file, 'r') as f:
            all_students = json.load(f)
            estudiantes_inscritos = [s for s in all_students if materia_target in s['materias']]
    
    # 2. Identificar sesiones totales de la materia (días únicos con registros)
    sesiones_totales = len(set(a['fecha'].split(' ')[0] for a in asistencias if a['materia'] == materia_target))
    
    # Si no ha habido clases, no hay alertas
    if sesiones_totales == 0:
        return []

    alerts = []
    for est in estudiantes_inscritos:
        asistencias_est = len([a for a in asistencias if a['materia'] == materia_target and a['student_id'] == est['student_id']])
        porcentaje = (asistencias_est / sesiones_totales) * 100
        faltas = sesiones_totales - asistencias_est
        
        alerts.append({
            "student_id": est['student_id'],
            "name": est['name'],
            "asistencias": asistencias_est,
            "total_sesiones": sesiones_totales,
            "porcentaje": round(porcentaje, 1),
            "faltas": faltas,
            "riesgo": porcentaje < 80 # Riesgo si falta más del 20%
        })
        
    return alerts
