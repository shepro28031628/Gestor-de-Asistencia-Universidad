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
    participant E as Estudiante (Front)
    participant B as Backend (Flask API)
    participant DB as SQLite DB

    Note over E, B: Proceso de Marcación QR + GPS
    E->>E: Capturar Coordenadas (GPS API)
    E->>E: Escanear QR (QR Scanner)
    E->>B: POST /api/attendance/marcar {token, lat, lng, student_id}
    B->>B: Validar Token contra class_sessions
    B->>B: Calcular Distancia (Fórmula Haversine)
    alt Es Válido (Distancia < 50m)
        B->>DB: INSERT INTO attendances (...)
        DB-->>B: ID_Confirmación
        B-->>E: 200 OK {success: true, message: "¡Presente!"}
    else Fuera de Rango / Token Inválido
        B-->>E: 400 Error {success: false, message: "Ubicación Incorrecta"}
    end
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
