# Gestión de Asistencia Dinámica 🚀

Este módulo describe la lógica de generación, validación y reporte final de asistencia, enfocándose en la prevención de fraude y automatización.

## 📱 Rotación Viva de QR (Anti-Fraude)

Para neutralizar el fraude por compartición de fotografías o capturas de pantalla por servicios de mensajería (WhatsApp/Telegram), el sistema implementa una **Rotación Viva**:

1.  **Generación Continua**: El token QR cambia automáticamente cada **15 segundos** mientras la sesión esté activa.
2.  **Ventana de Gracia**: El servidor mantiene una validez histórica de **60 segundos**. Esto permite que si un estudiante escaneó un código justo antes de rotar, el registro sea aceptado exitosamente a pesar del retraso de red.
3.  **Inutilidad de la Foto**: Una foto enviada a un tercero será inválida en menos de un minuto, obligando la presencia física frente a la pantalla del docente.

### 2. Validación Espacial (Geofencing)
El sistema restringe el marcado de asistencia a perímetros físicos configurados (Campus).
- **Radio de Tolerancia**: 100 metros (ajustable por sede).
- **Sedes Reales (Bogotá/Teusaquillo)**:
    - **Sede Teusaquillo (Dg. 40a)**: `4.6300, -74.0684`
    - **Sede Principal (Cra. 16)**: `4.6318, -74.0665`
    - **Sede Parkway (Dg. 40a)**: `4.6310, -74.0685`
- **Algoritmo**: Haversine (calcula distancia circular sobre la superficie terrestre).

## 📧 Finalización y Reporte Automático

El sistema garantiza que cada clase tenga su reporte de asistencia sin depender exclusivamente de la acción manual del docente.

### 1. Cierre Manual
El docente puede presionar **"Finalizar y Enviar Reporte"** en cualquier momento para cerrar la sesión anticipadamente y recibir el reporte inmediato.

### 2. Cierre Automático (Monitor de Horarios)
El backend ejecuta un **Monitor de Horarios** (hilo daemon) que:
1. Verifica cada 60 segundos las sesiones activas.
2. Compara la hora actual con el `end_time` académico de la base de datos.
3. Si la clase ha terminado cronológicamente, el sistema dispara el flujo de clausura:
   - Marca la sesión como inactiva.
   - Genera el reporte consolidado en formato HTML.
   - Envía el correo electrónico al docente automáticamente.

```ascii
[Monitor de Horarios] --- (60s) ---> ¿Clase Terminada Académicamente?
                                             |
                                     +-------+-------+
                                     |               |
                                    NO               SI
                                     |               |
                                 Continuar      1. Inactivar Sesión
                                                2. Consolidar Presentes/Ausentes
                                                3. Enviar Reporte HTML (SMTP)
```

## 🔍 Reglas de Validación de Marcado
- **Token Vivo**: Solo los tokens generados en los últimos 60 segundos son aceptados.
- **Geocerca (Haversine)**: El estudiante debe estar dentro del radio permitido (configurable, defecto 100m) del campus detectado por GPS.
- **Unicidad Estudiantil**: El sistema impide registros duplicados para el mismo estudiante en la misma sesión.
