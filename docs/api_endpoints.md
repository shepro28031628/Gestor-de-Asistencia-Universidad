# 🌐 Especificación Técnica de la API - UNINPAHU
> **Versión**: 1.2 | **Base URL**: `/api` | **Seguridad**: Session-Based + Token Rotation

Este catálogo detalla la interfaz de comunicación entre el frontend (PWA) y el backend (Flask), garantizando la integridad de los procesos de registro académico.

---

## 🔐 1. Módulo: Autenticación (`/auth`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/login` | Valida credenciales y establece la sesión. Retorna el perfil completo del usuario. |
| `POST` | `/update-profile-pic` | Sube y vincula una foto de perfil (Multipart/FormData). |

---

## 📋 2. Módulo: Operaciones Estudiante (`/attendance`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/progreso/<username>` | Retorna el % de asistencia por materia basado en el calendario académico. |
| `GET` | `/horario/<username>` | Obtiene las clases programadas para el usuario autenticado. |
| `GET` | `/sesiones-activas/<username>` | Lista las clases que tienen un QR activo en el momento del polling. (Consolidado). |
| `POST` | `/marcar` | Registro de asistencia con validación de Token QR y Geofencing (Haversine). |
| `GET` | `/get-citaciones/<id>` | Obtiene alertas de citación activa enviadas por docentes. (Consolidado). |
| `POST` | `/subir-justificacion` | Carga de soportes (PDF/Imagen) para inasistencias. |
| `GET` | `/historial` | Registro histórico de marcaciones realizadas por el estudiante. |

---

## 🎓 3. Módulo: Operaciones Docente (`/attendance`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/activar` | Inicia una sesión de clase y genera el primer token QR. |
| `GET` | `/token-vivo/<id>` | Gestiona la rotación dinámica (cada 15s) con ventana de gracia de 60s. |
| `POST` | `/finalizar` | Cierra la sesión manualmente y dispara el reporte SMTP al correo institucional. |
| `GET` | `/estudiantes-sesion/<id>` | Lista de alumnos inscritos con su estado de marcación en tiempo real. |
| `POST` | `/marcar-manual` | Permite al docente registrar a un alumno (Ej: fallo de dispositivo). |
| `POST` | `/crear-citacion` | Genera una alerta persistente para un estudiante específico. |
| `GET` | `/get-justificaciones-docente` | Bandeja de entrada para revisar soportes cargados por alumnos. |
| `GET` | `/historial-docente/<username>` | Resumen de clases pasadas con métricas de asistencia. |

---

## 🛠️ Lógica de Consolidación (Anti-Spam)

Para evitar la saturación de la UI, los siguientes endpoints aplican filtrado de duplicados en el servidor:

```ascii
[ Cliente ] --( Polling )--> [ API ]
                               |
       /-----------------------+-----------------------\
       |                                               |
 [ Sesiones Activas ]                          [ Citaciones ]
 GROUP BY schedule_id                    GROUP BY teacher_name, message
 (Evita duplicados por                   (Evita duplicados por
  rotación de tokens)                     reincidencia de alertas)
```

---

## 🛡️ Protocolos de Seguridad
1. **Validación de Tiempo**: No se aceptan marcaciones fuera del rango horario del `schedule`.
2. **Validación Espacial**: Bloqueo automático si el estudiante está a >100m del centro del campus.
3. **Unicidad de Marcado**: Se impide el registro de múltiples asistencias de un mismo alumno para una misma sesión (`UNIQUE constraint`).
