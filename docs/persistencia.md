# Modelo de Persistencia y Sincronización

El sistema implementa una arquitectura de persistencia multinivel para garantizar la integridad de los datos en entornos universitarios con conectividad variable.

## 1. Persistencia en Servidor (SQLite WAL)
Para soportar el tráfico masivo durante los cambios de clase (ej: 800 estudiantes marcando en 5 minutos):
- **Modo WAL:** El motor SQLite permite lecturas simultáneas mientras se escribe la asistencia, eliminando los errores de "Database is locked".
- **Integridad Referencial:** Garantizada mediante `foreign_keys=ON`, evitando que se pierdan vínculos entre estudiantes y sesiones.

## 2. Persistencia en Cliente (LocalStorage & Offline)
La PWA utiliza `localStorage` para:
- **Sesión Persistente:** Mantiene al usuario logueado incluso si cierra el navegador.
- **Cola de Sincronización:** Si el estudiante marca asistencia sin internet:
  1. El registro se guarda en una cola local JSON.
  2. Un `Interval` en JS monitorea la conexión (`navigator.onLine`).
  3. Al recuperar la señal, se vacía la cola enviando las peticiones pendientes al backend.

## 3. Persistencia de Archivos
- Las fotos de perfil y justificaciones médicas se almacenan en el sistema de archivos del servidor (`Frontend/static/uploads`).
- La base de datos solo guarda la **URL relativa**, facilitando la migración del almacenamiento a la nube (ej: AWS S3) en el futuro.

## 4. Auditoría de Tiempo Real
- **Polling Activo:** El panel docente consulta cada 3 segundos el estado de la base de datos para mostrar los asistentes en vivo.
- **Monitor de Horarios:** Un hilo independiente (`Thread`) audita constantemente la base de datos para forzar el cierre de sesiones que hayan superado su tiempo límite.
