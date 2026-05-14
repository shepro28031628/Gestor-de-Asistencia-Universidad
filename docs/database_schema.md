# Esquema de Base de Datos - UNINPAHU Asistencia

La base de datos utiliza **SQLite3** con el modo **WAL (Write-Ahead Logging)** activado para soportar múltiples lecturas y escrituras simultáneas de forma eficiente.

## 📊 Diccionario de Datos

### 👥 Usuarios (`users`)
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER (PK) | Identificador único interno. |
| `username` | TEXT (Unique) | Código institucional del usuario. |
| `password` | TEXT | Contraseña (texto plano para pruebas). |
| `full_name` | TEXT | Nombre completo del usuario. |
| `role` | TEXT | `estudiante`, `profesor` o `admin`. |
| `profile_pic` | TEXT | Ruta relativa a la foto de perfil. |

### 🏛️ Infraestructura (`campuses` & `rooms`)
- **`campuses`**: Almacena las sedes físicas con sus coordenadas `latitude` y `longitude` para la validación de **Geofencing**.
- **`rooms`**: Salones de clase vinculados a cada sede.

### 📅 Académico (`subjects`, `groups`, `schedules`)
- **`subjects`**: Catálogo de materias institucionales.
- **`groups`**: Instancias de materias en un semestre (ej: Grupo 750).
- **`schedules`**: Horarios definidos por día (`M, T, W, R, F, S, U`) y bloques de tiempo (`HH:MM`).

### 📱 Sesiones y Asistencia (`class_sessions`, `attendances`)
- **`class_sessions`**: Almacena los tokens UUID dinámicos generados cada 15 segundos para evitar el fraude por captura de pantalla.
- **`attendances`**: Registro de marcaciones.
  - **`status`**: `Presente` (QR Estudiante), `manual` (Validación Docente manual), `manual_prof` (Escaneo Bidireccional).
  - **`distance_to_campus`**: Distancia en metros calculada mediante Haversine.

### 📣 Gestión de Riesgo (`citations`, `justifications`)
- **`citations`**: Alertas generadas por el docente para estudiantes con asistencia crítica.
- **`justifications`**: Almacena las rutas a archivos de soporte (médicos/laborales) subidos por los alumnos.

---

## 🛠️ Configuración de Motor
```sql
PRAGMA journal_mode=WAL;      -- Alta concurrencia
PRAGMA foreign_keys=ON;       -- Integridad referencial
```
