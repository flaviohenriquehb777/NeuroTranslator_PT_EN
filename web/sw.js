/* NeuroTranslator v5.0.7 — Service Worker */
const CACHE_VERSION = '5.0.7';
const STATIC_CACHE = `nt-static-${CACHE_VERSION}`;

const scope = new URL(self.registration.scope);
const inScope = (url) => url.origin === scope.origin && url.pathname.startsWith(scope.pathname);
const scopeUrl = (path) => new URL(path, scope).toString();

const PRECACHE = [
    scopeUrl('./'),
    scopeUrl('index.html'),
    scopeUrl('assets/css/styles.css?v=5.0.7'),
    scopeUrl('assets/js/script-optimized.js?v=5.0.7'),
    scopeUrl('assets/images/logo_original.png'),
    scopeUrl('manifest.json'),
];

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => cache.addAll(PRECACHE))
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys.map((k) => {
                    if (k.startsWith('nt-static-') && k !== STATIC_CACHE) return caches.delete(k);
                    return Promise.resolve();
                })
            )
        ).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const { request } = event;
    if (request.method !== 'GET') return;

    const url = new URL(request.url);
    if (!inScope(url)) return;

    const accept = request.headers.get('accept') || '';
    const isHtml = request.mode === 'navigate' || accept.includes('text/html');

    if (isHtml) {
        const cacheKey = new Request(scopeUrl('index.html'));
        event.respondWith(
            fetch(request).then((res) => {
                if (res && res.ok) {
                    const copy = res.clone();
                    caches.open(STATIC_CACHE).then((cache) => cache.put(cacheKey, copy));
                }
                return res;
            }).catch(() => caches.match(cacheKey))
        );
        return;
    }

    const isAsset = url.pathname.includes('/assets/') || url.pathname.endsWith('.js') || url.pathname.endsWith('.css');
    if (isAsset) {
        event.respondWith(
            caches.match(request).then((cached) => {
                const fetchPromise = fetch(request).then((network) => {
                    if (network && network.ok) {
                        const copy = network.clone();
                        caches.open(STATIC_CACHE).then((cache) => cache.put(request, copy));
                    }
                    return network;
                });
                return cached || fetchPromise;
            })
        );
    }
});
