// Trazo criterIA. SPDX-License-Identifier: GPL-3.0-or-later
// Guarda la app para que abra sin conexión. Al cambiar archivos, sube el número de versión.
const CACHE = 'trazo-v2';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png'];
// Tipografías y lectores de .docx y .pdf: se guardan la primera vez que se usan
const EXTERNOS = ['fonts.googleapis.com', 'fonts.gstatic.com', 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  // Solo borra versiones antiguas de Trazo; no toca las cachés de las otras apps del sitio
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('trazo-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    if (!url.pathname.startsWith(new URL('./', self.registration.scope).pathname)) return;
    e.respondWith(
      fetch(e.request).then(r => { if (r.ok) { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); } return r; })
        .catch(() => caches.match(e.request).then(m => m || caches.match('index.html')))
    );
  } else if (EXTERNOS.includes(url.hostname)) {
    e.respondWith(
      caches.match(e.request).then(m => m || fetch(e.request).then(r => { if (r.ok || r.type === 'opaque') { const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); } return r; }))
    );
  }
});
