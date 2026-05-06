# 📖 Manual de Usuario Institucional
> **UNINPAHU Asistencia** | Sistema de Gestión Académica Digital

Bienvenido a la guía oficial de uso. El sistema está diseñado para ser intuitivo, seguro y rápido. Sigue las instrucciones según tu rol.

---

## 👨‍🎓 Rol: Estudiante
*Tu asistencia en la palma de tu mano.*

### 1. Registro de Asistencia (Flujo Rápido)
1.  **Selección**: Elige la materia actual en el menú desplegable.
2.  **Escaneo**: Toca el botón **"INICIAR ESCANEO QR"**.
3.  **Captura**: Apunta al QR que proyecta tu profesor.

> [!WARNING]
> **SEGURIDAD QR**: El código rota cada 15 segundos. Si tardas mucho, la app te pedirá escanear el nuevo código en pantalla.

### 2. Validación Geográfica (GPS)
Debes estar en el campus universitario. Si el GPS detecta que estás fuera del radio permitido, el marcado será rechazado automáticamente por integridad académica.

### 3. Justificaciones Médicas/Laborales
¿Faltaste? No te preocupes. Ve a la pestaña **"Justificaciones"**, sube tu evidencia (PDF/JPG) y tu profesor podrá validarla desde su panel.

---

## 👨‍🏫 Rol: Docente (Panel de Control)
*Control total y reportes automatizados.*

### 1. Activar una Clase
Al iniciar tu cátedra, selecciona la materia y toca **"ACTIVAR SESIÓN"**.
*   **QR Dinámico**: Se proyectará un código que cambia constantemente, impidiendo que alumnos ausentes marquen mediante fotos enviadas por WhatsApp.

### 2. Cierre Inteligente y Reportes
*   **Cierre Manual**: Toca **"Finalizar y Enviar Reporte"**.
*   **Cierre Automático**: Si olvidas cerrar la sesión, el **Monitor de Horarios** la clausurará exactamente al terminar la hora de clase.

> [!TIP]
> **Reporte PDF/HTML**: Al finalizar, el sistema envía automáticamente un consolidado con los asistentes a tu correo institucional.

### 3. Marcado de Contingencia
Si un alumno tiene un fallo técnico real (ej: cámara dañada), puedes marcarlo manualmente usando el botón **"Marcar"** que aparece junto a su nombre en tu lista de asistentes en vivo.

---

## ⚙️ Sección Técnica (Administración)

### Inicialización de Base de Datos
Si necesitas restaurar los datos de prueba y sedes:
```bash
# Ejecutar desde la raíz del proyecto
python Backend/seed.py
```

### Ejecución del Servidor Unificado
```bash
python Backend/app.py
```
> **Acceso**: [http://localhost:5001](http://localhost:5001)

---

## ❓ Preguntas Frecuentes (FAQ)

| Problema | Solución |
| :--- | :--- |
| **"Error de GPS"** | Asegúrate de tener activa la ubicación en tu móvil y haber dado permiso al navegador. |
| **"Token Expirado"** | Escanea nuevamente; el profesor proyectará el nuevo código en segundos. |
| **"No veo mi materia"** | Verifica con administración que estés matriculado en el grupo correcto. |

> [!NOTE]
> **Diseñado para UNINPAHU.** Soporte técnico disponible en la oficina de sistemas.
