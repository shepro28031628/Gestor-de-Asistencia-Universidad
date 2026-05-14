# Diagramas Técnicos Full-Stack - UNINPAHU Asistencia 📊🌐

Este documento detalla la arquitectura desacoplada entre el **Frontend (Cliente PWA)** y el **Backend (Servidor Flask)**.

---

## 1. Arquitectura de Componentes (Front vs Back)
Muestra la separación de responsabilidades y las tecnologías en cada capa.

```mermaid
graph LR
    subgraph Frontend_PWA[Capa de Cliente - PWA]
        UI[UI/UX - Jinja2 & CSS]
        JS[Lógica JS - Fetch API]
        CAM[Módulo de Cámara/QR]
        GPS[Módulo Geolocalización]
    end

    subgraph Backend_Flask[Capa de Servidor - API REST]
        AUTH[Rutas de Auth - auth.py]
        ATT[Rutas de Asistencia - attendance.py]
        CORE[Lógica de Negocio - Python]
        IMG[Gestión de Archivos - OS/FileSystem]
    end

    subgraph Database_Layer[Capa de Datos]
        DB[(SQLite - asistencia.db)]
    end

    JS -->|Request JSON/Form-Data| AUTH
    JS -->|Request JSON/Form-Data| ATT
    AUTH -->|Queries| DB
    ATT -->|Queries| DB
    ATT -->|Guardar Fotos/Justificaciones| IMG
```

---

## 2. Diagrama de Secuencia Detallado (Comunicación API)
Muestra el flujo exacto de una marcación de asistencia exitosa.

```mermaid
sequenceDiagram
    autonumber
    participant E as Estudiante (QR)
    participant P as Profesor (Escáner)
    participant B as Backend (Flask API)
    participant DB as SQLite DB

    Note over E, P: Flujo Alternativo: Docente Escanea a Alumno
    E->>E: Mostrar QR Personal (Username/ID)
    P->>P: Abrir Cámara (Html5Qrcode)
    P->>P: Capturar QR de Alumno
    P->>B: POST /api/attendance/mark {username, schedule_id, status: 'manual_prof'}
    B->>B: Validar sesión activa del Docente
    B->>DB: INSERT INTO attendances (status='manual_prof')
    DB-->>B: Confirmación
    B-->>P: 200 OK {success: true}
    P->>P: Feedback Sensorial (Sonido/Vibración)
    Note right of P: Lista "En Vivo" actualizada
```

---

## 3. Flujo de Activación de Clase (Vista Docente)
Cómo el profesor habilita el sistema para sus alumnos.

```mermaid
flowchart TD
    subgraph UI_Docente[Interfaz del Profesor]
        A[Seleccionar Materia] --> B[Clic en Activar Sesión]
    end

    subgraph Servidor[Backend Flask]
        B --> C[POST /api/attendance/activar-sesion]
        C --> D[Generar UUID / Token Único]
        D --> E[INSERT INTO class_sessions]
    end

    subgraph Tiempo_Real[Sincronización]
        E --> F[Retornar Token al Front]
        F --> G[Generar Imagen QR con QRCode.js]
        G --> H[Iniciar Polling cada 3s]
        H --> I[GET /api/attendance/estudiantes-sesion/id]
    end

    I -->|JSON Estudiantes| UI_Docente
```

---

## 4. Estructura de Datos y Flujo de Archivos
Cómo viajan las Justificaciones y Fotos de Perfil.

```mermaid
graph TD
    subgraph Front
        U[Usuario selecciona archivo]
        F[Input Multipart/Form-Data]
    end

    subgraph Back
        P[Endpoint /api/auth/update-profile-pic]
        V[Validar Extensión .jpg/.png/.pdf]
        S[Guardar en static/uploads]
    end

    subgraph Persistence
        DB[(Actualizar ruta en DB)]
    end

    U --> F
    F -->|Upload File| P
    P --> V
    V --> S
    S --> DB
```

---

## 5. Resumen de Roles y Permisos
| Característica | Frontend (Estudiante) | Frontend (Profesor) | Backend (Validación) |
| :--- | :--- | :--- | :--- |
| **Asistencia** | Escanear / Ver Progreso | Activar / Ver Lista en Vivo | Verificar GPS & Token |
| **Perfiles** | Ver / Subir Foto | Ver / Subir Foto | Guardar Ruta en DB |
| **Justificaciones** | Subir Soportes | Revisar / Descargar | Mapear a Student_ID |
| **Citaciones** | Recibir Alerta Roja | Generar Alerta (Citar) | Notificar vía API |
