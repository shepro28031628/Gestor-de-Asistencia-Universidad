# Manual de Usuario - UNINPAHU Asistencia 📖

Bienvenido al sistema de asistencia. Esta guía te ayudará a navegar por las funciones principales de la aplicación.

## 👨‍🎓 Para el Estudiante

### 1. Registro de Asistencia
- Selecciona tu materia en el menú desplegable.
- Haz clic en **"INICIAR ESCANEO QR"**.
- Apunta la cámara al código QR que proyecta el profesor.
- **Importante:** El código QR cambia cada 15 segundos por seguridad. Si el escaneo falla, intenta nuevamente con el nuevo código en pantalla.
- **GPS:** Debes estar físicamente en la sede de la universidad; de lo contrario, el sistema rechazará el marcado.

### 2. Justificar Inasistencia
- Si faltaste a clase, ve a la pestaña **"Justificaciones"**.
- Selecciona la materia, adjunta tu documento (PDF o Imagen) y envíalo.
- El profesor revisará tu excusa desde su panel.

### 3. Personalizar Perfil
- Haz clic en el círculo de iniciales (arriba) para subir tu propia foto de perfil.

---

## 👨‍🏫 Para el Profesor

### 1. Iniciar Clase
- En la pestaña **"Sesión Actual"**, selecciona la materia correspondiente.
- Haz clic en **"ACTIVAR SESIÓN"**.
- El sistema generará un código QR dinámico que rota constantemente para evitar fraudes (fotos compartidas).

### 2. Finalización y Reportes
- **Cierre Manual**: Puedes presionar **"Finalizar y Enviar Reporte"** al terminar tu cátedra.
- **Cierre Automático**: Si olvidas cerrar la sesión, el sistema la cerrará automáticamente al finalizar la hora académica.
- **Reporte por Email**: En ambos casos, recibirás un correo electrónico automático con el listado consolidado de asistentes en formato HTML.

### 3. Monitoreo en Tiempo Real
- Debajo del QR verás la lista de alumnos que van marcando.
- Si un alumno tiene problemas técnicos demostrables, puedes usar el botón **"Marcar"** al lado de su nombre.

---

## ⚙️ Administración y Despliegue
Para personal de TI o administradores del sistema:

### 1. Inicialización de Datos
Para restaurar la base de datos a su estado original con sedes y usuarios de prueba:
```bash
python Backend/seed.py
```

### 2. Lanzamiento del Servidor
El sistema está unificado. No requiere servidores front-end separados:
```bash
python Backend/app.py
```
Acceso local: `http://localhost:5001`

### 3. Monitoreo
- Verifica que la consola muestre **"Monitor de Horarios Iniciado"**. Este proceso es el que garantiza los cierres automáticos.
