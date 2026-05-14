# Guía de Despliegue en Render

Este documento detalla los pasos para desplegar el **Gestor de Asistencia Universidad** en la plataforma Render.

## 1. Preparativos
El proyecto ya incluye los archivos necesarios:
- `requirements.txt`: Incluye `gunicorn`.
- `build.sh`: Script de instalación automática.
- `render.yaml`: Configuración de Infraestructura como Código (IaC).

## 2. Pasos en Render
1. Inicie sesión en [Render](https://render.com/).
2. Haga clic en **New +** y seleccione **Blueprint**.
3. Conecte su repositorio de GitHub.
4. Render detectará automáticamente el archivo `render.yaml`.
5. Confirme los cambios y haga clic en **Apply**.

## 3. Configuración Manual (Alternativa)
Si no desea usar Blueprints, cree un **Web Service** con los siguientes datos:
- **Runtime**: `Python 3`
- **Build Command**: `bash build.sh`
- **Start Command**: `PYTHONPATH=Backend gunicorn 'app:create_app()'`

## 4. Notas Técnicas sobre Base de Datos
- Actualmente se usa **SQLite**.
- **Importante**: Los datos guardados en SQLite se perderán cada vez que el servicio se reinicie (a menos que se configure un *Render Disk*).
- Se recomienda migrar a **PostgreSQL** para persistencia real en producción.

## Diagrama de Flujo de Despliegue
```ascii
[ Repositorio Git ] 
       |
       v
[ Render Blueprint ] ---> [ Ejecuta build.sh ]
       |                         |
       |                  (Instala dependencias)
       v
[ Render Web Service ] <--- [ Ejecuta Start Command ]
       |                         |
       v                  (PYTHONPATH=Backend gunicorn...)
[ App Online ]
```

---
*Mantenimiento: Ingeniero Senior Conservador*
