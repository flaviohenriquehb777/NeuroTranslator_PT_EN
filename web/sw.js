/* NeuroTranslator v4.0 — Service Worker */
const CACHE_NAME = 'neurotranslator-v4.0';
const TRANSLATION_CACHE = 'nt4-translations';
const MAX_TRANSLATION_ENTRIES = 100;

const PRECACHE = [
    '/',
    '/index.html',
    '/assets/css/styles.css',
    '/assets/js/script-optimized.js',
    '/assets/images/logo_original.png',
    '/manifest.json'
];

// Install: precache static assets
self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE))
    );
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys.map((k) => {
                    if (k !== CACHE_NAME && k !== TRANSLATION_CACHE) {
                        return caches.delete(k);
                    }
                    return Promise.resolve();
                })
            )
        ).then(() => self.clients.claim())
    );
});

// Fetch: stale-while-revalidate for static assets, cache translations
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET for static assets
    if (request.method === 'GET') {
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
        return;
    }

    // Cache translation POST responses
    if (request.method === 'POST' && (url.pathname.includes('/translate') || url.hostname.includes('mymemory'))) {
        event.respondWith(
            request.clone().text().then((body) => {
                const cacheKey = new Request(url.href + '?body=' + encodeURIComponent(body));
                return caches.match(cacheKey).then((cached) => {
                    if (cached) return cached;
                    return fetch(request).then((response) => {
                        if (response && response.ok) {
                            const clone = response.clone();
                            caches.open(TRANSLATION_CACHE).then(async (cache) => {
                                await cache.put(cacheKey, clone);
                                // Limit cache size
                                const keys = await cache.keys();
                                if (keys.length > MAX_TRANSLATION_ENTRIES) {
                                    const excess = keys.length - MAX_TRANSLATION_ENTRIES;
                                    for (let i = 0; i < excess; i++) {
                                        await cache.delete(keys[i]);
                                    }
                                }
                            });
                        }
                        return response;
                    });
                });
            })
        );
    }
});