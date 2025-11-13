import { describe, it, expect, vi } from 'vitest'

async function translate(src: string, sourceLang: string, targetLang: string) {
  const first = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(src)}&langpair=${sourceLang}|${targetLang}`
  let translated = ''
  let r0: any
  try { r0 = await fetch(first) } catch {}
  if (r0 && r0.ok) { const j0 = await r0.json(); translated = j0?.responseData?.translatedText || '' }
  const endpoints = ['https://translate.astian.org/translate','https://libretranslate.de/translate','https://libretranslate.com/translate','https://translate.argosopentech.com/translate']
  for (const url of endpoints) {
    if (translated) break
    let r: any
    try { r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ q: src, source: sourceLang, target: targetLang, format: 'text' }) }) } catch {}
    if (r && r.ok) { const d = await r.json(); translated = d?.translatedText || '' }
  }
  return translated || src
}

describe('translation fallback', () => {
  it('uses fallback when first fails', async () => {
    const mymemory = vi.fn().mockResolvedValue({ ok: false })
    const libre1 = vi.fn().mockResolvedValue({ ok: false })
    const libre2 = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ translatedText: 'Good night!' }) })
    const originalFetch = global.fetch as any
    global.fetch = vi.fn((url: string) => {
      if (url.includes('mymemory')) return mymemory()
      if (url.includes('libretranslate.de')) return libre2()
      return libre1()
    }) as any
    const result = await translate('Boa noite!', 'pt', 'en')
    expect(result).toBe('Good night!')
    global.fetch = originalFetch
  })
})