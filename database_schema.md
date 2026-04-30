# Estructura de Base de Datos Final - UNINPAHU Asistencia

Este documento detalla la arquitectura completa de la base de datos SQLite (`asistencia.db`). Se ha actualizado para incluir la lógica de ubicación física (Salones y Sedes).

---

## 1. Tabla: `campuses` (Sedes)
Define las sedes físicas de la universidad.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `name` | TEXT | Nombre de la sede (ej: Sede Principal, Sede Norte). |
| `lat` / `lng`| REAL | Coordenadas GPS centrales de la sede para validación. |

---

## 2. Tabla: `rooms` (Salones)
Catálogo de aulas físicas vinculadas a una sede.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `campus_id` | INTEGER | Llave foránea vinculada a `campuses`. |
| `code` | TEXT | Código o nombre del salón (ej: Salón 301, Aula 102). |

---

## 3. Tabla: `users`
Usuarios del sistema (Estudiantes y Profesores).

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `username` | TEXT | Código o ID de acceso. |
| `password` | TEXT | Contraseña de acceso. |
| `full_name` | TEXT | Nombre completo. |
| `role` | TEXT | `estudiante` o `profesor`. |
| `profile_pic`| TEXT | Ruta de la foto de perfil personalizada. |

---

## 4. Tabla: `subjects` (Asignaturas)
Materias que dicta la universidad.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `name` | TEXT | Nombre de la materia. |

---

## 5. Tabla: `groups` (Grupos)
Instancia de una materia con un profesor asignado.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `subject_id`| INTEGER | Vínculo con `subjects`. |
| `teacher_id`| INTEGER | Vínculo con `users` (profesor). |

---

## 6. Tabla: `schedules` (Horarios)
Define cuándo y dónde se dicta un grupo.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `group_id`  | INTEGER | Vínculo con `groups`. |
| `room_id`   | INTEGER | Vínculo con `rooms` (Ubicación física). |
| `day`       | TEXT | Día de la semana (M, T, W, R, F, S, U). |
| `start_time`| TEXT | Hora de inicio. |
| `end_time`  | TEXT | Hora de fin. |

---

## 7. Tabla: `class_sessions` (Sesiones Activas)
Generadas por el profesor para el marcado QR.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `schedule_id`| INTEGER | Vínculo con el horario. |
| `qr_token`  | TEXT | Token de validación del QR. |
| `is_active` | INTEGER | 1 si la clase está abierta, 0 si cerró. |

---

## 8. Tabla: `attendances` (Registro de Asistencia)
Marcas finales de los estudiantes.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `student_id`| INTEGER | Vínculo con `users`. |
| `session_id`| INTEGER | Vínculo con `class_sessions`. |
| `status`    | TEXT | `qr`, `manual` o `justificada`. |
| `timestamp` | TEXT | Fecha y hora del registro. |

---

## 9. Tabla: `justifications` (Soportes)
Documentos de excusa cargados por el estudiante.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER | Llave primaria. |
| `student_id`| INTEGER | Vínculo con `users`. |
| `file_path` | TEXT | Ruta del archivo en `static/uploads`. |
| `status`    | TEXT | Estado de aprobación. |
