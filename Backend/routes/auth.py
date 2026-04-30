from flask import Blueprint, request, jsonify
from database import get_db
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)

# RUTA DEFINITIVA: Alineada con la carpeta estática de Flask
UPLOAD_FOLDER = os.path.abspath(os.path.join('Frontend', 'static', 'uploads'))

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticación con soporte para foto de perfil."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    with get_db() as conn:
        user = conn.execute(
            'SELECT id, username, full_name, role, profile_pic FROM users WHERE username = ? AND password = ? AND role = ?', 
            (username, password, role)
        ).fetchone()

        if user:
            user_data = dict(user)
            return jsonify({
                "success": True,
                "user_id": user_data['id'],
                "username": user_data['username'],
                "full_name": user_data['full_name'],
                "role": user_data['role'],
                "profile_pic": user_data['profile_pic']
            })
    return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

@auth_bp.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    """Guarda la foto de perfil en la ubicación servida por Flask."""
    try:
        if 'file' not in request.files: return jsonify({"success": False}), 400
        file = request.files['file']
        user_id = request.form.get('user_id')
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
        filename = secure_filename(f"profile_{user_id}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # URL relativa para el navegador
        relative_path = f"/static/uploads/{filename}"
        with get_db() as conn:
            conn.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (relative_path, user_id))
            conn.commit()
        
        return jsonify({"success": True, "profile_pic": relative_path})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
