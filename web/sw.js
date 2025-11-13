const CACHE_NAME = 'neurotranslator-cache-v6';
const PRECACHE = [
  '/',
  '/index.html',
  '/assets/css/styles.css',
  '/assets/js/script-optimized.js',
  '/assets/images/logo_original.png'
];
const ASSETS = ['/', '/index.html', '/assets/css/styles.css', '/assets/js/script-optimized.js', '/assets/images/preview.svg', '/favicon.png', '/manifest.json'];
self.addEventListener('install', (event) => { self.skipWaiting(); event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE))); });
self.addEventListener('activate', (event) => { event.waitUntil(caches.keys().then((keys) => Promise.all(keys.map((k) => (k !== CACHE_NAME ? caches.delete(k) : Promise.resolve())))).then(() => self.clients.claim())); });
self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.pathname.startsWith('/translate')) return;
  event.respondWith(
    caches.match(request).then((cached) => {
      const fetchPromise = fetch(request).then((network) => {
        if (network && network.status === 200) {
          const copy = network.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        }
        return network;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
self.addEventListener('fetch', (event) => { const { request } = event; if (request.method !== 'GET') return; event.respondWith(caches.match(request).then((cached) => { const fetchPromise = fetch(request).then((response) => { const clone = response.clone(); caches.open(CACHE_NAME).then((cache) => cache.put(request, clone)); return response; }).catch(() => cached); return cached || fetchPromise; })); });