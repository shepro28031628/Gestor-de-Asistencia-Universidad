# Documentación de API - UNINPAHU Asistencia

Este documento detalla los puntos de entrada (endpoints) del servidor Flask. La API está dividida en dos módulos principales: Autenticación y Gestión de Asistencia.

**URL Base:** `http://localhost:5001/api`

---

## 🔐 Módulo: Autenticación (`/auth`)

### 1. `POST /login`
Valida las credenciales del usuario y devuelve su perfil completo.
*   **Body (JSON):** `{ "username", "password", "role" }`
*   **Retorna:** Perfil del usuario incluyendo nombre, rol y foto de perfil.

### 2. `POST /update-profile-pic`
Actualiza la foto de perfil del usuario.
*   **Body (Multipart):** `file` (Imagen), `user_id`
*   **Retorna:** Ruta de la nueva imagen en el servidor.

---

## 📋 Módulo: Asistencia (`/attendance`)

### 3. `GET /horario/<username>`
Obtiene el horario de clases programadas para un estudiante o profesor.
*   **Retorna:** Lista de materias con salón, sede y horas.

### 4. `GET /sesiones-activas/<username>`
Busca si hay clases activas en este momento para el estudiante.
*   **Retorna:** Lista de sesiones con token QR vigente y ubicación.

### 5. `POST /marcar`
Registra la asistencia mediante escaneo de QR y validación GPS.
*   **Body (JSON):** `{ "token", "student_id", "lat", "lng" }`
*   **Retorna:** Mensaje de éxito o error (ej: "Fuera de rango").

### 6. `GET /progreso/<username>`
Calcula el porcentaje de asistencia por materia para el estudiante.
*   **Retorna:** Lista de materias con porcentaje (ej: 85%).

### 7. `GET /historial`
Obtiene todos los registros de asistencia globales.
*   **Retorna:** Lista cronológica de marcas.

### 8. `POST /activar-sesion`
(Docente) Genera un nuevo código QR y activa la sesión de clase.
*   **Body (JSON):** `{ "schedule_id" }`
*   **Retorna:** Token QR generado.

### 9. `GET /estudiantes-sesion/<session_id>`
(Docente) Obtiene la lista de alumnos inscritos y quiénes ya marcaron.
*   **Retorna:** Lista con estado en tiempo real.

### 10. `POST /marcar-manual`
(Docente) Registra la asistencia de un alumno que tuvo problemas con el QR.
*   **Body (JSON):** `{ "session_id", "student_id" }`

### 11. `POST /subir-justificacion`
(Estudiante) Envía un soporte médico o laboral para una falta.
*   **Body (Multipart):** `file`, `student_id`, `schedule_id`

### 12. `GET /get-justificaciones-docente`
(Docente) Obtiene la lista de todas las excusas pendientes por revisar.

### 13. `GET /historial-docente/<username>`
(Docente) Resumen histórico de todas sus sesiones dictadas y quórum obtenido.

### 14. `POST /crear-citacion`
(Docente) Registra una nueva citación formal para un estudiante en riesgo.
*   **Body (JSON):** `{ "teacher_id", "student_id" }`

### 15. `GET /get-citaciones/<student_id>`
(Estudiante) Recupera todas las alertas de citación activas para el alumno.
