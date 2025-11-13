const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

const app = express();
const CACHE_TTL_MS = Number(process.env.CACHE_TTL_MS || 30000);
const cache = new Map();
const limiter = rateLimit({ windowMs: 60_000, max: Number(process.env.RATE_LIMIT_MAX || 60) });
app.use(cors());
app.use(express.json());
app.use(limiter);

const LIBRE_ENDPOINTS = [
  'https://translate.astian.org/translate',
  'https://libretranslate.de/translate',
  'https://libretranslate.com/translate',
  'https://translate.argosopentech.com/translate'
];

app.post('/translate', async (req, res) => {
  try {
    const { q, source, target, format = 'text' } = req.body || {};
    if (!q || !target) {
      return res.status(400).json({ error: 'Parâmetros inválidos' });
    }

    const src = source && source !== target ? source : 'auto';

    const key = `${src}|${target}|${q}`;
    const now = Date.now();
    const hit = cache.get(key);
    if (hit && now - hit.time < CACHE_TTL_MS) {
      return res.json({ translatedText: hit.text, provider: hit.provider, cached: true });
    }

    // Tentativa MyMemory primeiro (GET)
    try {
      const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(q)}&langpair=${src}|${target}`;
      const r0 = await fetch(url, { headers: { Accept: 'application/json' }, cache: 'no-store' });
      if (r0.ok) {
        const j0 = await r0.json();
        const translatedText = j0?.responseData?.translatedText || '';
        if (translatedText) {
          cache.set(key, { text: translatedText, provider: 'mymemory', time: now });
          return res.json({ translatedText, provider: 'mymemory' });
        }
      }
    } catch (_) {}

    // Fallback LibreTranslate
    for (const url of LIBRE_ENDPOINTS) {
      try {
        const r = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ q, source: src, target, format })
        });
        if (r.ok) {
          const d = await r.json();
          const translatedText = d?.translatedText || '';
          if (translatedText) {
            cache.set(key, { text: translatedText, provider: url, time: now });
            return res.json({ translatedText, provider: url });
          }
        }
      } catch (_) {}
    }

    return res.status(502).json({ error: 'Falha em todos endpoints' });
  } catch (err) {
    return res.status(500).json({ error: 'Erro interno', detail: String(err) });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Proxy de tradução ativo em http://localhost:${port}`));