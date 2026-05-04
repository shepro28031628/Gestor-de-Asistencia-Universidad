# Gestión de Asistencia Dinámica 🚀

Este módulo describe la lógica de generación, validación y reporte final de asistencia.

## 📱 Generación de QR Dinámico

Para evitar el fraude por compartición de capturas de pantalla, el sistema genera un token único cada vez que el profesor activa la clase.

## 📧 Finalización y Reporte Automático

El sistema garantiza que cada clase tenga su reporte de asistencia sin depender exclusivamente de la acción manual del docente.

### 1. Cierre Manual
El docente puede presionar **"Finalizar y Enviar Reporte"** en cualquier momento para cerrar la sesión anticipadamente.

### 2. Cierre Automático (Monitor de Horarios)
El backend ejecuta un **Monitor de Horarios** en segundo plano que:
1. Verifica cada 60 segundos las sesiones activas.
2. Compara la hora actual con el `end_time` definido en el horario (`schedules`).
3. Si la clase ha terminado cronológicamente, el sistema:
   - Marca la sesión como inactiva.
   - Genera el reporte consolidado.
   - Envía el correo electrónico al docente automáticamente.

```ascii
[Monitor de Horarios] --- (60s) ---> ¿Clase Terminada?
                                            |
                                    +-------+-------+
                                    |               |
                                   NO               SI
                                    |               |
                                Continuar      1. Inactivar Token
                                               2. Generar Reporte HTML
                                               3. Enviar a Docente
```

## 🔍 Reglas de Validación
- **Unicidad**: Solo el token más reciente generado por el profesor es válido.
- **Geocerca**: El estudiante debe estar dentro del radio permitido del campus.
- **Tiempo**: El token expira automáticamente tras 15 minutos de su creación, pero la sesión permanece abierta para el reporte hasta el `end_time` de la materia.
