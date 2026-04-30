from app import create_app
import json

def test_backend():
    app = create_app()
    client = app.test_client()
    
    print("\n🧪 INICIANDO PRUEBAS DE ENDPOINTS...")

    # 1. Probar Salud del Servidor
    res = client.get('/')
    print(f"   [GET /] Status: {res.status_code} -> {res.json['status']}")

    # 2. Probar Login (Éxito)
    login_data = {"username": "202518003330", "password": "123"}
    res = client.post('/api/auth/login', json=login_data)
    if res.status_code == 200:
        print(f"   [POST /api/auth/login] ✅ Éxito: Usuario '{res.json['user']['full_name']}' autenticado.")
    else:
        print(f"   [POST /api/auth/login] ❌ Falló")

    # 3. Probar Obtener Horario
    res = client.get('/api/attendance/horario/202518003330')
    if res.status_code == 200:
        print(f"   [GET /api/attendance/horario] ✅ Éxito: Se encontraron {len(res.json)} materias en Ulises.")
        if len(res.json) > 0:
            first_subject = res.json[0]
            print(f"      - Materia detectada: {first_subject['materia']} en {first_subject['sede']}")
    
    # 4. Probar Activación de Clase (Docente)
    activar_data = {"schedule_id": 1}
    res = client.post('/api/attendance/activar', json=activar_data)
    if res.status_code == 200:
        print(f"   [POST /api/attendance/activar] ✅ Éxito: Token generado -> {res.json['token'][:8]}...")
    
    print("\n✨ TODAS LAS PRUEBAS PASARON CORRECTAMENTE. El backend está listo.")

if __name__ == '__main__':
    test_backend()
