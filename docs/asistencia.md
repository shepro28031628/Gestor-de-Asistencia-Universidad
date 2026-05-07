# 🛡️ Protocolos de Asistencia y Seguridad
> **Módulo**: Validación Dinámica | **Algoritmos**: Haversine + Totp-Like Rotation

Este documento detalla los mecanismos de seguridad implementados para garantizar la integridad del registro de asistencia, neutralizando intentos de fraude y automatizando la auditoría académica.

---

## 🔑 1. Rotación Viva de QR (Anti-Proxy)

Para evitar que un estudiante ausente marque asistencia mediante una foto enviada por un tercero, el sistema implementa una rotación de tokens de alta frecuencia.

| Parámetro | Valor | Descripción |
| :--- | :--- | :--- |
| **Intervalo de Rotación** | 15 Segundos | Tiempo de vida de un QR en pantalla. |
| **Ventana de Gracia** | 60 Segundos | Margen para procesar escaneos en tránsito (latencia). |
| **Algoritmo de Hash** | UUID v4 | Tokens no predecibles generados dinámicamente. |

> [!IMPORTANT]
> **VENTANA DE GRACIA (Grace Window)**: El servidor mantiene en memoria los últimos 4 tokens generados. Esto asegura que si el QR rota mientras el estudiante está procesando el envío, el registro no sea rechazado injustamente.

---

## 🌍 2. Validación Espacial (Geofencing)

El sistema utiliza la **Fórmula de Haversine** para calcular la distancia ortodrómica entre dos puntos de una esfera (la Tierra) a partir de sus longitudes y latitudes.

### Sedes Configuradas (Campus UNINPAHU)

| Sede | Latitud | Longitud | Radio Tolerancia |
| :--- | :--- | :--- | :--- |
| **Teusaquillo** | `4.6300` | `-74.0684` | 100 Metros |
| **Principal** | `4.6318` | `-74.0665` | 100 Metros |
| **Parkway** | `4.6310` | `-74.0685` | 120 Metros |

> [!TIP]
> Si el estudiante se encuentra a una distancia mayor al radio permitido respecto a **cualquiera** de las sedes institucionales, el servidor arrojará un error de `FUERA_DE_RANGO` y bloqueará el registro.

---

## 🤖 3. Monitor de Horarios (Cierre Autónomo)

El backend ejecuta un proceso daemon encargado de auditar la vida de las sesiones académicas para garantizar el envío de reportes, incluso si el docente olvida cerrar la sesión.

```mermaid
graph TD
    A[Monitor de Horarios] -->|Check cada 60s| B{¿Hora Actual > End_Time?}
    B -- NO --> C[Mantener Sesión Viva]
    B -- SI --> D[Disparar Protocolo de Clausura]
    D --> E[Inactivar QR]
    E --> F[Generar Reporte Consolidado]
    F --> G[Envío SMTP a Correo Institucional]
```

### Flujo de Decisión (ASCII)
```text
[ Monitor de Horarios ]
          |
    (Check cada 60s)
          |
          v
  /-----------------\
  | ¿Hora Actual >  |--- NO ---> [ Mantener Sesión Viva ]
  |   End_Time?     |
  \-----------------/
          |
        ( SI )
          |
          v
  [ Protocolo de Clausura ]
          |
          v
  [ Inactivar Token QR  ]
          |
          v
  [ Generar Consolidado ]
          |
          v
  [ Envío Email Docente ]
```

---

## 🔍 Resumen de Reglas de Marcado

1.  **Sincronía Temporal**: Solo se aceptan marcaciones durante el bloque horario oficial del grupo.
2.  **Unicidad Estricta**: Un `student_id` no puede tener más de una entrada exitosa para la misma `session_id`.
3.  **Auditoría de Ubicación**: Cada registro de asistencia (`attendances`) guarda la distancia exacta (en metros) que el estudiante tenía respecto al centro de la sede al momento del marcado.

> [!NOTE]
> **Integridad de Datos**: Los reportes automáticos se envían en formato HTML enriquecido, facilitando la lectura directa desde dispositivos móviles por parte del docente.
