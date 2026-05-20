import { expect, test } from '@playwright/test';

const HF_BASE = 'https://flaviohenriquehb777-neurotranslator-api.hf.space';

async function setAutoTranslate(page: any, enabled: boolean): Promise<void> {
  await page.evaluate((value) => {
    const el = document.getElementById('autoTranslateToggle') as HTMLInputElement | null;
    if (!el) return;
    el.checked = value;
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, enabled);
}

function normalizeText(value: string | null): string {
  return (value || '').replace(/\s+/g, '').trim();
}

test('página carrega sem erros', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (err) => errors.push(err.message));

  await page.route(`${HF_BASE}/health`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', uptime_s: 3600 }),
    });
  });

  await page.goto('/');
  await expect(page.locator('#translateBtn')).toBeVisible();
  expect(errors).toEqual([]);
});

test('tradução PT→EN retorna em menos de 10s (neural)', async ({ page }) => {
  await page.route(`${HF_BASE}/health`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', uptime_s: 3600 }),
    });
  });

  await page.route(`${HF_BASE}/metrics`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ bleu_score: 42.3 }),
    });
  });

  await page.route(`${HF_BASE}/translate`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        translated_text: 'Hello world',
        model_used: 'Helsinki-NLP/opus-mt-pt-en',
        confidence: 0.9,
        latency_ms: 120,
      }),
    });
  });

  await page.goto('/');
  await setAutoTranslate(page, false);
  await page.locator('#sourceText').fill('Olá mundo');
  await page.locator('#translateBtn').click();

  await expect(page.locator('#targetText')).toHaveValue('Hello world');
  await expect(page.locator('#engineBadge')).toBeVisible();
  await expect(page.locator('#engineBadge')).toContainText('Neural');
  await expect(page.locator('#engineBadge')).toHaveAttribute('title', /Helsinki-NLP\/opus-mt-pt-en/);
});

test('swap de idiomas funciona', async ({ page }) => {
  await page.route(`${HF_BASE}/health`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', uptime_s: 3600 }),
    });
  });

  await page.goto('/');
  const srcBefore = normalizeText(await page.locator('#sourceDropdownCurrent').textContent());
  const tgtBefore = normalizeText(await page.locator('#targetDropdownCurrent').textContent());

  await page.locator('#swapLanguages').click();

  await expect
    .poll(async () => normalizeText(await page.locator('#sourceDropdownCurrent').textContent()))
    .toBe(tgtBefore);
  await expect
    .poll(async () => normalizeText(await page.locator('#targetDropdownCurrent').textContent()))
    .toBe(srcBefore);
});

test('histórico salva a última tradução', async ({ page }) => {
  await page.route(`${HF_BASE}/health`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', uptime_s: 3600 }),
    });
  });

  await page.route(`${HF_BASE}/translate`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        translated_text: 'Good morning',
        model_used: 'Helsinki-NLP/opus-mt-pt-en',
        confidence: 0.9,
        latency_ms: 120,
      }),
    });
  });

  await page.goto('/');
  await setAutoTranslate(page, false);
  await page.locator('#sourceText').fill('Bom dia');
  await page.locator('#translateBtn').click();
  await expect(page.locator('#targetText')).toHaveValue('Good morning');

  await page.locator('#openHistoryBtn').click();
  await expect(page.locator('#historyContainer')).toContainText('Bom dia');
  await expect(page.locator('#historyContainer')).toContainText('Good morning');
});

test('fallback para MyMemory funciona quando API neural está offline', async ({ page }) => {
  await page.route(`${HF_BASE}/health`, async (route) => {
    await route.abort();
  });
  await page.route(`${HF_BASE}/translate`, async (route) => {
    await route.abort();
  });

  await page.route('https://api.mymemory.translated.net/get*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ responseData: { translatedText: 'MyMemory ok', match: 0.7 } }),
    });
  });

  await page.goto('/');
  await setAutoTranslate(page, false);
  await page.locator('#sourceText').fill('Teste');
  await page.locator('#translateBtn').click();

  await expect(page.locator('#targetText')).toHaveValue('MyMemory ok');
  await expect(page.locator('#engineBadge')).toBeVisible();
  await expect(page.locator('#engineBadge')).toContainText('MyMemory');
});

