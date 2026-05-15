// Nombre del contenedor de caché (versión)
const CACHE_NAME = 'uninpahu-v2';

// Lista de archivos estáticos que se guardarán para uso offline
const ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/img/LOGO.png',
  '/static/img/uninpahu_bg.png',
  '/static/img/Icono-1.webp'
];

/**
 * Evento de instalación: Se ejecuta la primera vez que se abre la app.
 * Descarga y guarda los activos en el almacenamiento local.
 */
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

/**
 * Evento de activación: Limpia versiones antiguas de caché para evitar conflictos.
 */
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)));
    })
  );
});

/**
 * Interceptor de peticiones: Si el archivo está en caché, lo sirve instantáneamente.
 * Si no (como las peticiones API), intenta descargarlo de la red.
 */
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});
