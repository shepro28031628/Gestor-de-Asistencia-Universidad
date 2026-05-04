// Nombre del contenedor de caché (versión)
const CACHE_NAME = 'uninpahu-v1';

// Lista de archivos estáticos que se guardarán para uso offline
const ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/img/logo.png',
  '/static/img/uninpahu_bg.png'
];

/**
 * Evento de instalación: Se ejecuta la primera vez que se abre la app.
 * Descarga y guarda los activos en el almacenamiento local.
 */
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

/**
 * Interceptor de peticiones: Si el archivo está en caché, lo sirve instantáneamente.
 * Si no (como las peticiones API), intenta descargarlo de la red.
 */
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});
