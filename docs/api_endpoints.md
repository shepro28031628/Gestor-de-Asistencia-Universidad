# 🌐 Especificación Técnica de la API - UNINPAHU
> **Base URL**: `http://localhost:5001/api` | **Formato**: `application/json`

Esta API RESTful es el corazón del sistema de asistencia, gestionando desde la autenticación biométrica (fotos) hasta la rotación de seguridad de grado bancario para los códigos QR.

---

> [!IMPORTANT]
> **SEGURIDAD DINÁMICA (ANTI-SPOOFING)**
> La API implementa una ventana de validación temporal estricta. Los tokens generados expiran cada 15 segundos, invalidando cualquier intento de uso de capturas de pantalla o fotos compartidas.

---

## 🔐 1. Módulo: Autenticación (`/auth`)

### `POST /login`
Punto de entrada principal para el acceso al sistema.

```json
// Request
{
  "username": "20231001",
  "password": "hashed_password",
  "role": "estudiante"
}

// Response (Success)
{
  "status": "success",
  "user": {
    "id": 1,
    "full_name": "Edinsson ...",
    "role": "estudiante",
    "profile_pic": "/static/uploads/p1.jpg"
  }
}
```

---

## 📋 2. Módulo: Gestión de Asistencia (`/attendance`)

### `POST /activar` (Docente)
Inicia el ciclo de vida de una clase y activa el monitor de cierre.

> [!TIP]
> Al activar una clase, el backend reserva los recursos y comienza el proceso de rotación en `token-vivo`.

### `POST /marcar` (Estudiante)
El endpoint más crítico. Realiza validaciones cruzadas.

**Validaciones Realizadas:**
1. **Token Vivo**: Verifica que el QR escaneado sea el actual o esté en la ventana de gracia.
2. **Geofencing**: Compara `lat/lng` vs coordenadas de la sede (Haversine).
3. **Unicidad**: Impide doble marcado para la misma sesión.

```json
// Request Payload
{
  "token": "uuid-v4-rotativo",
  "student_id": 12,
  "lat": 4.6543,
  "lng": -74.0892
}
```

---

## 🕒 3. Ciclo de Vida de una Sesión (Trazabilidad)

```ascii
[ DOCENTE ] --( /activar )--> [ SESIÓN ABIERTA ]
                                     |
                                     v (Cada 15s)
[ CLIENTE ] <--( /token-vivo )-- [ ROTACIÓN QR ]
       |                             |
       +------( /marcar )------> [ VALIDACIÓN ]
                                     |
[ MONITOR ] --( /finalizar )---> [ CIERRE & REPORTE SMTP ]
```

---

## 📨 4. Notificaciones y Citaciones

### `POST /crear-citacion`
Permite al docente generar alertas preventivas para estudiantes con baja asistencia.

### `POST /subir-justificacion`
Gestión de documentos (Multipart/Form-Data). Los archivos se almacenan con hashing de nombre para evitar colisiones.

---

## 🛡️ Protocolos de Resiliencia

1.  **Sincronización Offline**: La API está diseñada para recibir marcaciones en lote si el estudiante perdió conexión momentáneamente.
2.  **Auto-Cierre**: Un daemon en segundo plano audita cada 60s las sesiones abiertas. Si la hora actual > hora de fin académica, la sesión se clausura y se envía el reporte al docente.
