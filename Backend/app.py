import os
from flask import Flask, jsonify, render_template, session, redirect, url_for, request
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.attendance import attendance_bp, iniciar_monitor

def create_app():
    """
    Fábrica de la aplicación Flask. Configura rutas de interfaz, 
    registra blueprints de la API y maneja errores globales.
    """
    # Configuración de rutas para plantillas HTML y archivos estáticos (CSS, JS, Imágenes)
    template_dir = os.path.abspath('Frontend/templates')
    static_dir = os.path.abspath('Frontend/static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Habilitar CORS para permitir peticiones desde diferentes orígenes si es necesario
    CORS(app)
    app.secret_key = "uninpahu_secret_key_2026" # Clave para cifrado de sesiones

    # --- 1. RUTAS DE NAVEGACIÓN (Renderizado de Vistas Jinja2) ---
    @app.route('/')
    def index():
        """Página de inicio (Login)"""
        return render_template('index.html')

    @app.route('/profesor')
    def profesor_view():
        """Panel de control docente"""
        if not session.get('logged_in') or session.get('role') != 'profesor':
            return redirect(url_for('index'))
        return render_template('profesor.html', full_name=session.get('full_name'))

    @app.route('/estudiante')
    def estudiante_view():
        """Dashboard del estudiante"""
        if not session.get('logged_in') or session.get('role') != 'estudiante':
            return redirect(url_for('index'))
        return render_template('estudiante.html', full_name=session.get('full_name'))

    @app.route('/set-session', methods=['POST'])
    def set_session():
        """Establece la sesión del lado del servidor tras login exitoso en JS"""
        data = request.json
        session['logged_in'] = True
        session['user_id'] = data.get('id')
        session['role'] = data.get('role')
        session['username'] = data.get('username')
        session['full_name'] = data.get('full_name')
        return jsonify({"success": True})

    @app.route('/logout')
    def logout():
        """Limpia la sesión y redirige al login"""
        session.clear()
        return redirect(url_for('index'))

    # --- 2. REGISTRO DE MÓDULOS API (Lógica de Negocio) ---
    # Módulo de Autenticación y Perfiles
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # Módulo de Asistencia, QR y Reportes
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    # Manejador global para rutas inexistentes
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Ruta no encontrada"}), 404

    return app

if __name__ == '__main__':
    # Creación de la instancia de la app
    app = create_app()
    
    # --- PROCESOS EN SEGUNDO PLANO ---
    # Inicia el hilo que cierra clases automáticamente al terminar el horario académico
    iniciar_monitor(app)
    
    # Lanzamiento del servidor en el puerto 5001 (Modo Debug activo para desarrollo)
    app.run(debug=True, port=5001)
