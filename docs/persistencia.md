# Documentación de Persistencia - UNINPAHU 🛡️

Este módulo garantiza que los datos de asistencia no se pierdan, incluso en condiciones de conectividad inestable o concurrencia alta.

## 🛠️ Arquitectura de Persistencia

### 1. Backend (SQLite WAL)
Se ha configurado la base de datos central `asistencia.db` con el modo **Write-Ahead Logging (WAL)**.
- **Técnica**: Permite que múltiples lectores y un escritor operen simultáneamente sin bloquearse.
- **Seguridad**: Se habilitó `PRAGMA foreign_keys = ON` para garantizar la integridad referencial.

### 2. Frontend (Cola Offline)
El portal del estudiante implementa una cola de persistencia local en `localStorage`.

#### Diagrama de Flujo: Registro de Asistencia
```ascii
+----------------+       +------------------+       +-------------------+
| Estudiante     |       | ¿Hay Conexión?   |  NO   | Guardar en Cola   |
| Escanea QR     |------>| (Fetch API)      |------>| localStorage      |
+----------------+       +------------------+       +-------------------+
                                 | SI                       |
                                 v                          | Al detectar
                         +------------------+               | red (online)
                         | Registrar en     |<--------------+
                         | Servidor (SQL)   |
                         +------------------+
```

## 🔧 Mantenimiento
- **Sincronización**: El cliente intenta vaciar la cola cada vez que se detecta el evento `online` del navegador.
- **Depuración**: Se puede inspeccionar `localStorage.getItem('attendance_queue')` en la consola del desarrollador.
- **Idempotencia**: El backend valida el `token` para evitar registros duplicados si la sincronización se dispara varias veces.
