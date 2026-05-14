# Configuración de PWA (Progressive Web App)

La plataforma UNINPAHU Asistencia está diseñada para ser instalada en dispositivos móviles sin pasar por las tiendas oficiales (App Store / Play Store), permitiendo acceso rápido y funcionamiento offline parcial.

## 📋 Requisitos para Instalación
1. Acceder mediante **HTTPS** (o `localhost` para pruebas).
2. Navegador compatible (Chrome en Android, Safari en iOS).

## 🚀 Pasos de Instalación

### En Android (Chrome)
1. Abre la URL del sistema.
2. Haz clic en el banner emergente "Instalar UNINPAHU Asistencia" o en los tres puntos de la esquina superior derecha.
3. Selecciona **"Instalar aplicación"**.

### En iOS (Safari)
1. Abre la URL en Safari.
2. Haz clic en el icono de **"Compartir"** (cuadrado con flecha hacia arriba).
3. Busca y selecciona **"Añadir a la pantalla de inicio"**.

---

## 🛠️ Componentes Técnicos

### 1. Web Manifest (`manifest.json`)
Define el icono institucional (`Icono-1.webp`), el color de la barra de estado (`#FFCCBC`) y el modo de visualización `standalone` (sin barras de navegación del navegador).

### 2. Service Worker (`sw.js`)
- **Cache-First Strategy:** Almacena los recursos estáticos (CSS, JS, Logos) localmente para que la app cargue instantáneamente incluso con conexión lenta.
- **Offline Mode:** Permite que la interfaz de inicio se muestre siempre, aunque no haya internet.

### 3. Cola de Sincronización
Cuando un estudiante intenta marcar asistencia sin internet:
- El registro se guarda en la memoria local (`LocalStorage`).
- Al recuperar la señal, el sistema sincroniza automáticamente los registros pendientes con el servidor.
