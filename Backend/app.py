import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.attendance import attendance_bp

def create_app():
    # Configuramos Flask para que encuentre tus carpetas de Frontend
    template_dir = os.path.abspath('Frontend/templates')
    static_dir = os.path.abspath('Frontend/static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    CORS(app)

    # 1. Rutas de Navegación (Interfaz)
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/estudiante')
    def estudiante_view():
        return render_template('estudiante.html')

    @app.route('/profesor')
    def profesor_view():
        return render_template('profesor.html')

    # 2. Registrar Módulos de API
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Ruta no encontrada"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    # Ejecutamos en el puerto 5001 para que coincida con tu configuración
    app.run(debug=True, port=5001)
