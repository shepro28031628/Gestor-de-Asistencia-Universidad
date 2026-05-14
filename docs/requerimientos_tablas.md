# Requerimientos de Integración - UNINPAHU

Este documento detalla las especificaciones de datos necesarias para que el sistema de asistencia se integre correctamente con los sistemas centrales de la Universidad UNINPAHU.

## 1. Perfiles de Usuario (Tabla `users`)
| Requisito | Descripción |
| :--- | :--- |
| **Identificador** | Debe ser el código institucional único (username). |
| **Email** | Debe proporcionarse el correo institucional para el envío de reportes. |
| **Rol** | El sistema distingue estrictamente entre `estudiante` y `profesor`. |

## 2. Definición de Sedes (Tabla `campuses`)
Para el correcto funcionamiento del **Geofencing**, la universidad debe proporcionar:
- Coordenadas GPS exactas (Latitud/Longitud) de cada sede.
- Un radio de tolerancia en metros (recomendado: 100m).

## 3. Estructura Académica
- **Horarios:** Deben seguir el formato de 24 horas (`HH:MM`).
- **Días:** Mapeados como códigos de una letra (`M, T, W, R, F, S, U`).
- **Inscripciones:** Es vital contar con el mapeo de qué estudiantes pertenecen a qué grupos para evitar el "robo de asistencia" de estudiantes externos.

## 4. Requerimientos de Infraestructura
- **Servidor:** Capacidad para ejecutar Python 3.10+.
- **Almacenamiento:** Espacio en disco para el crecimiento de la carpeta `/static/uploads` (Evidencias de inasistencia).
- **Red:** Acceso al puerto 587 (SMTP) si se requiere el envío real de reportes de asistencia por email.
