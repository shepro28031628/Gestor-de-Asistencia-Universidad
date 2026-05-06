# Requerimientos de Datos - Integración Universidad

Este documento define la estructura de las 12 tablas necesarias para el funcionamiento del Gestor de Asistencia. La universidad debe suministrar la información siguiendo estos tipos de datos y relaciones.

## 1. Diagrama de Flujo de Datos (Sincronización)

```text
+-----------------------+       +-------------------------+
|   SISTEMA ACADÉMICO   | ----> |   GESTOR DE ASISTENCIA  |
|      (Origen)         |       |      (Destino)          |
+-----------+-----------+       +------------+------------+
            |                                |
            | 1. Carga Tablas Maestras       | 2. Generación de Datos
            | (Programas, Usuarios, etc.)    | (Sesiones, Asistencias)
            v                                v
    [DB Universidad] ---------------> [asistencia.db]
```

## 2. Especificación de Tablas

### A. Tablas Maestras (Suministradas por la Universidad)

| Tabla | Campo | Tipo | Descripción |
| :--- | :--- | :--- | :--- |
| **academic_programs** | id | INTEGER | PK Única |
| | name | TEXT | Nombre del programa (Ej: Ingeniería) |
| | code | TEXT | Código interno del programa |
| **users** | id | INTEGER | PK Única |
| | username | TEXT | Código institucional (Login) |
| | password | TEXT | Hash de contraseña |
| | full_name | TEXT | Nombre completo |
| | email | TEXT | Correo institucional |
| | profile_pic | TEXT | Ruta a imagen de perfil |
| | role | TEXT | 'estudiante', 'profesor' o 'admin' |
| | program_id | INTEGER | FK -> academic_programs |
| **campuses** | id | INTEGER | PK Única |
| | name | TEXT | Nombre de la sede |
| | latitude | REAL | Coordenada GPS Latitud |
| | longitude | REAL | Coordenada GPS Longitud |
| | radius_meters | INTEGER | Radio de geocerca (m) |
| **rooms** | id | INTEGER | PK Única |
| | code | TEXT | Código del salón |
| | campus_id | INTEGER | FK -> campuses |
| **subjects** | id | INTEGER | PK Única |
| | code | TEXT | Código de la materia |
| | name | TEXT | Nombre de la asignatura |
| **groups** | id | INTEGER | PK Única |
| | group_number| TEXT | Número de grupo/sección |
| | subject_id | INTEGER | FK -> subjects |
| | teacher_id | INTEGER | FK -> users (Docente) |
| | start_date | TEXT | Fecha inicio (YYYY-MM-DD) |
| | end_date | TEXT | Fecha fin (YYYY-MM-DD) |
| | jornada | TEXT | Diurna, Nocturna, etc. |
| **schedules** | id | INTEGER | PK Única |
| | group_id | INTEGER | FK -> groups |
| | room_id | INTEGER | FK -> rooms |
| | day | TEXT | Día (M, T, W, R, F, S, U) |
| | start_time | TEXT | Hora inicio (HH:MM) |
| | end_time | TEXT | Hora fin (HH:MM) |
| **enrollments** | id | INTEGER | PK Única |
| | student_id | INTEGER | FK -> users (Estudiante) |
| | group_id | INTEGER | FK -> groups |

### B. Tablas Transaccionales (Generadas por la App)

| Tabla | Campo | Tipo | Descripción |
| :--- | :--- | :--- | :--- |
| **class_sessions** | id | INTEGER | PK Única |
| | schedule_id | INTEGER | FK -> schedules |
| | qr_token | TEXT | Token UUID único para validación |
| | expires_at | TEXT | Fecha/Hora límite de validez |
| | is_active | INTEGER | 1: Activo, 0: Sesión cerrada |
| **attendances** | id | INTEGER | PK Única |
| | student_id | INTEGER | FK -> users (Estudiante) |
| | session_id | INTEGER | FK -> class_sessions |
| | timestamp | DATETIME | Momento de la marcación |
| | lat | REAL | Latitud capturada |
| | lng | REAL | Longitud capturada |
| | distance_to_campus| REAL | Distancia calculada a sede |
| | status | TEXT | 'Presente', 'Manual', 'Justificado' |
| **citations** | id | INTEGER | PK Única |
| | teacher_id | INTEGER | FK -> users (Docente) |
| | student_id | INTEGER | FK -> users (Estudiante) |
| | message | TEXT | Motivo de la citación |
| | status | TEXT | 'activa' o 'resuelta' |
| **justifications** | id | INTEGER | PK Única |
| | student_id | INTEGER | FK -> users (Estudiante) |
| | schedule_id | INTEGER | FK -> schedules |
| | file_path | TEXT | Ruta al archivo PDF/Imagen |
| | status | TEXT | 'pendiente', 'aprobada', 'rechazada' |

## 3. Notas Técnicas
- **Formato de Fechas**: ISO 8601 (`YYYY-MM-DD`).
- **Codificación**: UTF-8.
- **Integridad**: Todas las llaves foráneas (FK) deben existir previamente en sus tablas maestras.
