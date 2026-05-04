# Documentación de Persistencia - UNINPAHU 🛡️

Garantizar la integridad y disponibilidad de los datos es crítico para el éxito del sistema de asistencia. Este módulo detalla las estrategias implementadas tanto en el servidor como en el cliente.

## 🛠️ Arquitectura de Persistencia

### 1. Backend (SQLite WAL)
La base de datos central `asistencia.db` utiliza el modo **Write-Ahead Logging (WAL)** para optimizar la concurrencia.

- **Alta Concurrencia**: Permite que los procesos de lectura (estudiantes consultando progreso) y escritura (estudiantes marcando asistencia) ocurran simultáneamente sin bloqueos de base de datos (`database is locked`).
- **Integridad**: Se ejecuta `PRAGMA foreign_keys = ON` en cada conexión para evitar inconsistencias entre tablas (ej: borrar un docente con grupos activos).
- **Estabilidad**: El modo WAL genera un archivo `.shm` y `.wal` que protege los datos ante cierres inesperados del servidor.

### 2. Frontend (Resiliencia Offline)
El portal del estudiante está diseñado bajo la filosofía *Offline-First*.

- **LocalStorage Queue**: Si un estudiante escanea un QR en un sótano o zona sin WiFi/Datos, el registro no se pierde. Se almacena en una cola interna.
- **Sincronización Automática**: Al detectar el evento `online` o al reiniciar la aplicación, el sistema intenta vaciar la cola enviando los registros pendientes al servidor.
- **Validación Temporal**: Los registros offline incluyen un `timestamp` para auditoría, aunque deben cumplir con la ventana de validez del token original.

#### Diagrama de Flujo: Resiliencia de Marcado
```ascii
[Escaneo de QR]
      |
      v
¿Servidor Disponible? --(NO)--> [Guardar en Cola Local] --(Esperar Red)---+
      |                                                                   |
     (SI)                                                                 |
      |                                                                   |
[Registro Directo] <------------------------------------------------------+
      |
      v
[Actualizar UI Estudiante]
```

## 🔧 Mantenimiento y Auditoría
- **Cola Local**: Se puede auditar mediante `localStorage.getItem('attendance_queue')`.
- **Modo Idempotente**: El backend rechaza duplicados exactos (`student_id` + `session_id`), permitiendo que el cliente reintente la sincronización sin riesgo de corromper estadísticas.
