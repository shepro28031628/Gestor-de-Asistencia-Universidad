const CACHE_NAME = 'uninpahu-v1';
const ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/img/logo.png',
  '/static/img/uninpahu_bg.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});
