SCHEMA = '''
-- Catálogo de programas académicos (Ingeniería, Derecho, etc.)
CREATE TABLE IF NOT EXISTS academic_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE
);

-- Usuarios del sistema: Estudiantes, Profesores y Administradores
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, -- Código institucional
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT, -- Campo vital para reportes automáticos al docente
    profile_pic TEXT, -- Ruta a la imagen de perfil en /static/uploads
    role TEXT CHECK(role IN ('estudiante', 'profesor', 'admin')) NOT NULL,
    program_id INTEGER,
    FOREIGN KEY (program_id) REFERENCES academic_programs(id)
);

-- Sedes de la Universidad (Ej: Hernando Santos, Calle 68) con geolocalización
CREATE TABLE IF NOT EXISTS campuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL, -- Latitud para Geofencing
    longitude REAL, -- Longitud para Geofencing
    radius_meters INTEGER DEFAULT 100 -- Radio permitido alrededor de la sede
);

-- Salones de clase vinculados a una sede
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    campus_id INTEGER,
    FOREIGN KEY (campus_id) REFERENCES campuses(id)
);

-- Materias académicas
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

-- Grupos académicos: Vinculan una materia con un docente y fechas de semestre
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_number TEXT NOT NULL,
    subject_id INTEGER,
    teacher_id INTEGER,
    start_date TEXT, -- Fecha de inicio (YYYY-MM-DD)
    end_date TEXT,   -- Fecha de fin (YYYY-MM-DD)
    jornada TEXT,    -- Diurna, Nocturna, Sabatina
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- Horarios específicos de cada grupo (Día y Bloque horario)
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    room_id INTEGER,
    day TEXT NOT NULL, -- M, T, W, R, F, S, U
    start_time TEXT NOT NULL, -- HH:MM
    end_time TEXT NOT NULL,   -- HH:MM
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

-- Relación de estudiantes matriculados en cada grupo
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    group_id INTEGER,
    UNIQUE(student_id, group_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Sesiones de clase activadas: Almacenan el Token QR dinámico
CREATE TABLE IF NOT EXISTS class_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER,
    qr_token TEXT UNIQUE, -- Token UUID para validación
    expires_at TEXT, -- Límite de vida del QR
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1, -- Indica si el QR sigue aceptando marcas
    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);

-- Registros oficiales de asistencia (Marcaciones)
CREATE TABLE IF NOT EXISTS attendances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    session_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lat REAL, -- Latitud capturada al marcar
    lng REAL, -- Longitud capturada al marcar
    distance_to_campus REAL, -- Distancia calculada en metros respecto a la sede
    status TEXT DEFAULT 'Presente', -- Presente, Manual, Justificado
    UNIQUE(student_id, session_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES class_sessions(id)
);

-- Alertas y citaciones de profesores a estudiantes
CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    student_id INTEGER,
    message TEXT,
    status TEXT DEFAULT 'activa',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- Justificaciones de inasistencia (Incapacidades/Certificados)
CREATE TABLE IF NOT EXISTS justifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    schedule_id INTEGER,
    file_path TEXT, -- Ruta al archivo PDF/JPG en el servidor
    status TEXT DEFAULT 'pendiente',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);
'''
