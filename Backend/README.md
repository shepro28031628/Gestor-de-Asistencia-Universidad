# 🎓 Gestor de Asistencia Universitaria - UNINPAHU

Este proyecto es una aplicación web moderna diseñada para la gestión y control de asistencia de estudiantes en la institución universitaria UNINPAHU. Utiliza tecnologías de geolocalización y códigos QR para garantizar la presencia física de los estudiantes en el campus y optimizar el proceso de registro.

## 🚀 Características Principales

### 👨‍🏫 Panel del Docente
- **Activación de Clase**: El docente puede iniciar una sesión de clase seleccionando la materia correspondiente.
- **Generación de QR Dinámico**: Crea un código QR temporal que los estudiantes deben escanear para registrar su asistencia.
- **Validación de Ubicación**: El sistema verifica que el docente esté dentro del perímetro permitido de la universidad.
- **Gestión de Excusas**: Revisión y aprobación de justificaciones médicas o laborales cargadas por los estudiantes.
- **Alertas de Deserción**: Sistema inteligente que detecta estudiantes con un alto número de inasistencias.
- **Carga de Listados**: Importación de listas de estudiantes mediante archivos CSV.
- **Estadísticas de Feedback**: Visualización de la calificación promedio dada por los estudiantes sobre la clase.

### 👨‍🎓 Panel del Estudiante
- **Registro por QR**: Escaneo del código QR generado por el docente para marcar asistencia.
- **Doble Validación**: Verificación de geolocalización (estar en la universidad) y pertenencia a la materia.
- **Historial de Asistencia**: Consulta detallada de las clases asistidas.
- **Carga de Justificaciones**: Subida de evidencias (fotos/documentos) para justificar inasistencias.
- **Feedback de Clase**: Posibilidad de calificar la calidad de la sesión recibida.

## 🛠️ Stack Tecnológico

- **Backend**: Python 3 con [Flask](https://flask.palletsprojects.com/)
- **Frontend**: HTML5, CSS3 (Diseño Premium/Responsivo), JavaScript (Vanilla)
- **Geolocalización**: API de Geolocalización del Navegador
- **Generación de QR**: [Segno](https://pypi.org/project/segno/)
- **Persistencia**: Archivos JSON para almacenamiento ligero de datos.

## 📂 Estructura del Proyecto

```text
Gestor de Asistencia Universidad/
├── Frontend/                 # Aplicación principal (Flask + Activos)
│   ├── asistencia.py         # Punto de entrada y lógica de rutas
│   ├── config.py             # Parámetros de geolocalización y horarios
│   ├── static/               # CSS, JS, Imágenes y QRs generados
│   ├── templates/            # Plantillas HTML (Jinja2)
│   ├── data/                 # Almacenamiento JSON (asistencia, estudiantes, feedback)
│   ├── models/               # Gestores de lógica de negocio
│   ├── services/             # Servicios auxiliares (Geo, etc.)
│   └── routes/               # Modularización de rutas (opcional)
└── Backend/                  # (Reservado para futuras expansiones API)
```

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone [URL-del-repositorio]
   ```

2. **Instalar dependencias**:
   ```bash
   pip install flask segno werkzeug
   ```

3. **Ejecutar la aplicación**:
   ```bash
   cd "Frontend"
   python asistencia.py
   ```

4. **Acceso**:
   Abrir en el navegador: `http://localhost:5000`

## 🔐 Credenciales de Prueba (Demo)

| Rol | Usuario | Contraseña |
| :--- | :--- | :--- |
| **Estudiante** | `estudiante` | `123` |
| **Docente** | `docente` | `123` |

## 📍 Configuración de Geolocalización
El sistema está configurado para validar la ubicación contra las coordenadas de UNINPAHU (definidas en `config.py`). El radio de tolerancia actual es de **600 metros**.

---
*Desarrollado para la Institución Universitaria UNINPAHU - 2024*
