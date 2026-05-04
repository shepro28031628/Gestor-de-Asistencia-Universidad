# Documentación de API - UNINPAHU Asistencia 🚀

Este documento detalla los puntos de entrada (endpoints) del servidor Flask. La API está diseñada para soportar una aplicación web progresiva (PWA) con actualizaciones en tiempo real y seguridad anti-fraude.

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

### 4. `POST /activar`
(Docente) Inicia una sesión de asistencia.
*   **Body (JSON):** `{ "schedule_id" }`
*   **Retorna:** `token` (UUID), `expires_at`.

### 5. `GET /token-vivo/<schedule_id>`
(Docente/Seguridad) **Rotación de Seguridad**. Genera un nuevo token QR cada 15 segundos si la sesión sigue activa.
*   **Importante**: Mantiene una "ventana de gracia" de 60s en el servidor para el token anterior.

### 6. `POST /marcar`
(Estudiante) Registra la asistencia mediante escaneo de QR y validación GPS.
*   **Body (JSON):** `{ "token", "student_id", "lat", "lng" }`
*   **Lógica**: Valida Geofencing (100m) y vigencia del Token Vivo.

### 7. `POST /finalizar`
(Docente) Cierra manualmente la sesión.
*   **Acción**: Inactiva el token y dispara el envío del **Reporte por Email** (SMTP) al correo del profesor.
*   **Body (JSON):** `{ "schedule_id" }`

### 8. `GET /progreso/<username>`
Calcula el porcentaje de asistencia acumulado por materia para el estudiante.

### 9. `GET /estudiantes-sesion/<schedule_id>`
(Docente) Lista en tiempo real de asistentes durante una clase activa.

### 10. `POST /marcar-manual`
(Docente) Fuerza el marcado de un alumno presente físicamente pero con fallos técnicos.

### 11. `POST /subir-justificacion`
(Estudiante) Carga soporte PDF/JPG para inasistencias pasadas.

### 12. `POST /crear-citacion`
(Docente) Alerta formal para estudiantes con asistencia crítica (<80%).

---

## 🕒 Procesos de Fondo (Daemon)

### 16. `Monitor de Horarios` (Interno)
No es un endpoint accesible por el cliente, pero es parte vital de la API:
- **Frecuencia**: Cada 60 segundos.
- **Acción**: Ejecuta automáticamente `/finalizar` para cualquier sesión cuyo `end_time` académico haya sido superado.
