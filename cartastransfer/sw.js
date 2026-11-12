// Hablemos: cartas conversacionales. SPDX-License-Identifier: GPL-3.0-or-later
// Guarda la app para que abra sin conexion. Al actualizar archivos, sube el numero de version.
const CACHE = 'hablemos-v2';
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "img/familia.png", "img/financiacion.png", "img/q06.png", "img/q08.png", "img/q12.png", "img/q15.png", "img/q17.png", "img/q21.png", "img/q26.png", "img/q30.png", "img/q32.png", "img/q35.png", "img/q41.png", "img/q44.png", "img/q48.png", "img/q51.png", "img/q53.png", "img/q57.png", "img/s08.png", "img/s10.png", "img/s19.png", "img/s24.png", "img/s26.png", "img/s28.png", "img/s30.png", "img/s32.png", "img/s35.png", "img/s37.png", "img/s39.png", "img/s41.png", "img/s46.png", "img/s48.png", "img/s51.png", "img/s53.png", "img/s55.png", "img/s57.png", "fonts/atkinson-hyperlegible-latin-400-normal.woff2", "fonts/atkinson-hyperlegible-latin-700-normal.woff2", "fonts/baloo-2-latin-600-normal.woff2", "fonts/baloo-2-latin-800-normal.woff2"];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  // Solo borra versiones antiguas de esta app; no toca las caches de las otras apps del sitio.
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('hablemos-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(r => { if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); } return r; })
      .catch(() => caches.open(CACHE).then(c => c.match(e.request).then(m => m || c.match('index.html'))))
  );
});
