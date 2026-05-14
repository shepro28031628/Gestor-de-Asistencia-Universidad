# Especificación de la API REST - UNINPAHU Asistencia

El sistema utiliza una arquitectura basada en micro-servicios internos comunicados mediante JSON sobre HTTP. Todas las rutas están bajo el prefijo `/api`.

---

## 🔐 Autenticación (`/api/auth`)

### 1. Iniciar Sesión
- **Ruta:** `POST /login`
- **Payload:**
  ```json
  { "username": "...", "password": "...", "role": "estudiante|profesor" }
  ```
- **Respuesta:** Perfil completo del usuario (ID, Nombre, Rol, Foto).

### 3. Sincronizar Sesión (Servidor)
- **Ruta:** `POST /set-session`
- **Descripción:** Sincroniza la sesión del navegador con el servidor Flask tras un login exitoso.
- **Payload:** `{ "id": 0, "username": "...", "role": "...", "full_name": "..." }`

### 4. Cerrar Sesión
- **Ruta:** `GET /logout`
- **Descripción:** Limpia la sesión del servidor y redirige a la raíz.

---

## 📝 Asistencia (`/api/attendance`)

### 1. Marcar Asistencia (Estudiante)
- **Ruta:** `POST /marcar`
- **Payload:**
  ```json
  { "token": "...", "lat": 0.0, "lng": 0.0, "student_id": 0 }
  ```
- **Validaciones:** Token activo, Geofencing (radio campus), Unicidad.

### 2. Registro Manual/Docente
- **Ruta:** `POST /mark` (o `/marcar-manual`)
- **Payload:**
  ```json
  { "username": "...", "schedule_id": 0, "status": "manual_prof" }
  ```
- **Descripción:** Permite al profesor registrar a un alumno escaneando su QR personal.

### 3. Activar Sesión (Docente)
- **Ruta:** `POST /activar`
- **Payload:** `{ "schedule_id": 0 }`
- **Respuesta:** Token inicial y tiempo de expiración.

### 4. Rotación de Token (Polling)
- **Ruta:** `GET /token-vivo/<schedule_id>`
- **Descripción:** Devuelve un nuevo token cada 15s con ventana de gracia de 60s.

### 5. Finalizar Clase
- **Ruta:** `POST /finalizar`
- **Descripción:** Cierra la sesión e inicia el envío del reporte SMTP al docente.

---

## 📊 Consultas y Reportes

### 1. Progreso Estudiante
- **Ruta:** `GET /progreso/<username>`
- **Respuesta:** Listado de materias con % de asistencia calculado.

### 2. Historial Docente
- **Ruta:** `GET /historial-docente/<username>`
- **Respuesta:** Resumen de sesiones pasadas con métricas de asistencia.

### 3. Alertas de Riesgo
- **Ruta:** `GET /riesgo-docente/<username>`
- **Descripción:** Estudiantes con menos del 80% de asistencia.

### 4. Citaciones
- **Ruta:** `POST /crear-citacion` | `GET /get-citaciones/<student_id>`

---

## 📁 Justificaciones
- **Ruta:** `POST /subir-justificacion` (Multipart)
- **Ruta:** `GET /get-justificaciones-docente` (Listado de archivos adjuntos).
