# Protocolos de Asistencia UNINPAHU

El sistema implementa un modelo de validación híbrido para garantizar el registro de asistencia incluso en condiciones técnicas adversas.

## 1. Escaneo de Estudiante (Modelo Principal)
1. **Activación:** El profesor inicia la sesión en el panel docente.
2. **Generación:** Se proyecta un código QR dinámico (cambia cada 15s).
3. **Validación:** El estudiante escanea el QR desde su dispositivo.
4. **Seguridad:** El servidor valida el **Token QR** y la **Geolocalización** (debe estar dentro del radio del campus).

## 2. Escaneo de Docente (Modelo de Contingencia)
Diseñado para estudiantes con problemas de cámara, falta de internet o fallos en el GPS.
1. **Identificación:** El estudiante genera su QR personal desde el botón "Mi QR".
2. **Captura:** El profesor abre el escáner desde su panel ("Escanear QR Alumnos").
3. **Registro:** Al escanear al alumno, se marca la asistencia con estado `manual_prof`.
4. **Efecto:** Se emite un feedback sonoro y vibración en el dispositivo del docente.

## 3. Estados de Asistencia
- **Presente:** Marcación exitosa vía QR Estudiante.
- **Validado:** Marcación realizada por el docente mediante escaneo directo.
- **Justificado:** Inasistencia avalada por el profesor tras revisar soportes.
- **Ausente:** Sin registro al finalizar la sesión cronológica.

## 4. Cierre Automático
El `monitor_de_horarios.py` audita las sesiones activas y las cierra automáticamente al finalizar el bloque de clase definido en el horario institucional, enviando un reporte consolidado al correo del docente.
