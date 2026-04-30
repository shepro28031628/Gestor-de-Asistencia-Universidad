# Documentación de API - UNINPAHU Asistencia 🚀

Este documento detalla los puntos de entrada (endpoints) del servidor Flask. La API está diseñada para soportar una aplicación web progresiva (PWA) con actualizaciones en tiempo real.

**URL Base:** `http://localhost:5001/api`

---

## 🔐 Módulo: Autenticación (`/auth`)

### 1. `POST /login`
Valida las credenciales del usuario.
*   **Body (JSON):** `{ "username", "password", "role" }`
*   **Retorna:** Perfil del usuario (`id`, `username`, `full_name`, `role`, `profile_pic`).

### 2. `POST /update-profile-pic`
Actualiza la foto de perfil del usuario y la guarda en el servidor.
*   **Body (Multipart):** `file` (Imagen), `user_id`
*   **Retorna:** `{ "success": true, "profile_pic": "/static/uploads/..." }`

---

## 📋 Módulo: Asistencia (`/attendance`)

### 3. `GET /horario/<username>`
Obtiene el horario de clases programadas según el rol.
*   **Docente:** Retorna materias con conteo de inscritos.
*   **Estudiante:** Retorna materias con salón y sede.

### 4. `GET /sesiones-activas/<username>`
Busca sesiones de clase con QR vigente para un estudiante.
*   **Retorna:** Lista de sesiones con token, ubicación y tiempo restante.

### 5. `POST /marcar`
Registra la asistencia mediante escaneo de QR y validación GPS.
*   **Body (JSON):** `{ "token", "student_id", "lat", "lng" }`
*   **Validaciones:** Día de la semana, hora de expiración, geofencing (radio de sede).

### 6. `GET /progreso/<username>`
Calcula el porcentaje de asistencia acumulado por materia.
*   **Retorna:** `{ "materia", "porcentaje", "asistencias", "total" }`

### 7. `GET /historial`
Obtiene todos los registros de asistencia globales (Uso administrativo/auditoría).

### 8. `POST /activar`
(Docente) Genera un nuevo código QR y activa la sesión de clase por 15 minutos.
*   **Body (JSON):** `{ "schedule_id" }`
*   **Retorna:** `token`, `expires_at_ms`.

### 9. `GET /estudiantes-sesion/<schedule_id>`
(Docente) Obtiene la lista de alumnos inscritos y su estado de asistencia hoy.
*   **Retorna:** Lista de alumnos con indicador `asistio` (0 o 1).

### 10. `POST /marcar-manual`
(Docente) Registra la asistencia forzada de un alumno.
*   **Body (JSON):** `{ "schedule_id", "student_id" }`

### 11. `POST /subir-justificacion`
(Estudiante) Carga un soporte (PDF/JPG) para justificar una falta.
*   **Body (Multipart):** `file`, `student_id`, `schedule_id`

### 12. `GET /get-justificaciones-docente`
(Docente) Lista todas las excusas enviadas por sus estudiantes.

### 13. `GET /historial-docente/<username>`
(Docente) Resumen histórico de sus sesiones dictadas y quórum obtenido.

### 14. `POST /crear-citacion`
(Docente) Genera una alerta formal para un estudiante con baja asistencia.
*   **Body (JSON):** `{ "teacher_id", "student_id" }`

### 15. `GET /get-citaciones/<student_id>`
(Estudiante) Recupera las alertas de citación activas.
