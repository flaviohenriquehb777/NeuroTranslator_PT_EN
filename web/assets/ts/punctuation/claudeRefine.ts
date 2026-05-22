import type { FetchWithTimeout } from './types';

export async function refinePunctuationWithClaude(params: {
    text: string;
    langHint: string;
    apiBase: string;
    fetchWithTimeout: FetchWithTimeout;
    timeoutMs: number;
}): Promise<string> {
    const url = `${params.apiBase}/punctuate`;
    const res = await params.fetchWithTimeout(
        url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({ text: params.text, lang: params.langHint }),
            cache: 'no-store',
        },
        params.timeoutMs,
    );

    if (!res.ok) {
        const body = await res.text().catch(() => '');
        throw new Error(`claude_punctuate_failed_${res.status}_${body.slice(0, 80)}`);
    }
    const data = await res.json() as { punctuated_text?: string };
    const out = (data.punctuated_text || '').toString();
    if (!out.trim()) throw new Error('claude_empty_result');
    return out;
}

