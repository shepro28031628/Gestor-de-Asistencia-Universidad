import datetime

# Almacén temporal de sesiones de clase activa
sesion_activa = {
    "token": None,
    "expiracion": None,
    "materia": None,
    "scanned_students": [] # Usamos lista para facilitar serialización si fuera necesaria
}

def get_sesion():
    return sesion_activa

def set_sesion(token, expiracion, materia=None):
    global sesion_activa
    sesion_activa["token"] = token
    sesion_activa["expiracion"] = expiracion
    sesion_activa["materia"] = materia
    sesion_activa["scanned_students"] = [] # Reset de escaneos para nueva sesión

def is_sesion_valid(token_escaneado=None):
    if not sesion_activa["token"]:
        return False
    if datetime.datetime.now() > sesion_activa["expiracion"]:
        return False
    if token_escaneado and token_escaneado != sesion_activa["token"]:
        return False
    return True

def add_scanned_student(student_id):
    if student_id not in sesion_activa["scanned_students"]:
        sesion_activa["scanned_students"].append(student_id)
        return True
    return False

def is_student_scanned(student_id):
    return student_id in sesion_activa["scanned_students"]
