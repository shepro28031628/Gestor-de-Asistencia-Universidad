from models import get_db_connection

def revisar():
    conn = get_db_connection()
    
    print("\n=== 📂 RESUMEN DE LA BASE DE DATOS UNINPAHU ===")
    
    # 1. Sedes
    sedes = conn.execute('SELECT * FROM campuses').fetchall()
    print(f"\n📍 SEDES ({len(sedes)}):")
    for s in sedes: print(f"   - {s['name']} (Lat: {s['latitude']}, Lng: {s['longitude']})")

    # 2. Usuarios
    users = conn.execute('SELECT * FROM users').fetchall()
    print(f"\n👤 USUARIOS ({len(users)}):")
    for u in users: print(f"   - {u['full_name']} [{u['role']}] - Código: {u['username']}")

    # 3. Materias
    materias = conn.execute('SELECT * FROM subjects').fetchall()
    print(f"\n📚 MATERIAS ({len(materias)}):")
    for m in materias: print(f"   - {m['code']}: {m['name']}")

    # 4. Inscripciones
    inscritos = conn.execute('SELECT u.full_name, s.name FROM enrollments e JOIN users u ON e.student_id = u.id JOIN groups g ON e.group_id = g.id JOIN subjects s ON g.subject_id = s.id').fetchall()
    print(f"\n📝 INSCRIPCIONES ({len(inscritos)}):")
    for i in inscritos: print(f"   - {i['full_name']} está en {i['name']}")

    conn.close()

if __name__ == '__main__':
    revisar()
