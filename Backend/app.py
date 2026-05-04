import os
from flask import Flask, jsonify, render_template
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

    # --- 1. RUTAS DE NAVEGACIÓN (Renderizado de Vistas Jinja2) ---
    @app.route('/')
    def index():
        """Página de inicio (Login)"""
        return render_template('index.html')

    @app.route('/estudiante')
    def estudiante_view():
        """Dashboard del estudiante"""
        return render_template('estudiante.html')

    @app.route('/profesor')
    def profesor_view():
        """Panel de control docente"""
        return render_template('profesor.html')

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
