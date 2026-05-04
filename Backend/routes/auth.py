from flask import Blueprint, request, jsonify, session
from database import get_db
import os
from werkzeug.utils import secure_filename

# Definición del blueprint para agrupar rutas de autenticación
auth_bp = Blueprint('auth', __name__)

# Configuración de la ruta absoluta para el almacenamiento de archivos subidos
UPLOAD_FOLDER = os.path.abspath(os.path.join('Frontend', 'static', 'uploads'))

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Valida las credenciales del usuario (Código y Password).
    Devuelve el perfil completo incluyendo la ruta de la foto de perfil.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    with get_db() as conn:
        # Consulta segura para verificar identidad y rol
        user = conn.execute(
            'SELECT id, username, full_name, role, profile_pic FROM users WHERE username = ? AND password = ? AND role = ?', 
            (username, password, role)
        ).fetchone()

        if user:
            user_data = dict(user)
            # Establecer sesión de servidor para acceso a rutas protegidas
            session['logged_in'] = True
            session['user_id'] = user_data['id']
            session['role'] = user_data['role']
            session['username'] = user_data['username']
            session['full_name'] = user_data['full_name']

            return jsonify({
                "success": True,
                "user_id": user_data['id'],
                "username": user_data['username'],
                "full_name": user_data['full_name'],
                "role": user_data['role'],
                "profile_pic": user_data['profile_pic']
            })
            
    # Error de seguridad en caso de fallo
    return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

@auth_bp.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    """
    Gestiona la subida de imágenes de perfil.
    Guarda el archivo en disco y actualiza la ruta en la base de datos.
    """
    try:
        if 'file' not in request.files: return jsonify({"success": False}), 400
        file = request.files['file']
        user_id = request.form.get('user_id')
        
        # Asegura que la carpeta de destino exista en el servidor
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
        # Limpieza del nombre del archivo para evitar ataques de inyección de rutas
        filename = secure_filename(f"profile_{user_id}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Guardado físico del archivo
        file.save(file_path)
        
        # Generación de la URL relativa que el navegador usará para mostrar la imagen
        relative_path = f"/static/uploads/{filename}"
        
        # Persistencia en la DB
        with get_db() as conn:
            conn.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (relative_path, user_id))
            conn.commit()
        
        return jsonify({"success": True, "profile_pic": relative_path})
    except Exception as e:
        # Registro de errores internos del servidor
        return jsonify({"success": False, "message": str(e)}), 500
