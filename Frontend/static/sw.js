const CACHE_NAME = 'uninpahu-v2';
const ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/img/uninpahu_bg.png',
  'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap',
  'https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  // Para APIs, intentamos red primero, luego nada (el frontend manejará el error con IndexedDB/LocalStorage)
  if (e.request.url.includes('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() => {
        return new Response(JSON.stringify({ success: false, offline: true }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // Para archivos estáticos, cache-first
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
