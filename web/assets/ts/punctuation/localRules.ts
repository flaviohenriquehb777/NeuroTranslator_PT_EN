import { PunctuationPipelineResult } from './types';

function normalizeSpaces(text: string): string {
    return text.replace(/\s+/g, ' ').replace(/\s+([,.;!?])/g, '$1').trim();
}

function capitalizeFirst(text: string): { text: string; changed: boolean } {
    const idx = text.search(/[A-Za-zÀ-ÖØ-öø-ÿ]/);
    if (idx < 0) return { text, changed: false };
    const ch = text[idx];
    const up = ch.toUpperCase();
    if (ch === up) return { text, changed: false };
    return { text: text.slice(0, idx) + up + text.slice(idx + 1), changed: true };
}

function escapeRegExp(value: string): string {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function addCommaAfterLeadingPhrase(text: string, phrase: string): { text: string; changed: boolean } {
    const re = new RegExp(`^(${escapeRegExp(phrase)})(\\s+)`, 'i');
    if (!re.test(text)) return { text, changed: false };
    const out = text.replace(re, (_, p1) => `${p1}, `);
    return { text: out, changed: out !== text };
}

function addCommaBeforePhrase(text: string, phrase: string): { text: string; changed: boolean } {
    const re = new RegExp(`(^|[^,.;!?])\\s+(${escapeRegExp(phrase)})(\\s+)`, 'gi');
    let changed = false;
    const out = text.replace(re, (_m, p1: string, p2: string, p3: string) => {
        changed = true;
        return `${p1}, ${p2}${p3}`;
    });
    return { text: out, changed };
}

function detectQuestion(text: string): boolean {
    const t = text.toLowerCase().trim();
    const patterns = [
        'como', 'quando', 'onde', 'qual', 'quais', 'quem', 'por que', 'por quê', 'o que', 'que horas',
    ];
    for (const p of patterns) {
        if (t.startsWith(p + ' ') || t === p) return true;
    }
    return false;
}

function endsWithTerminalPunctuation(text: string): boolean {
    return /[.!?]$/.test(text.trim());
}

function countPunctuationMarks(text: string): number {
    const m = text.match(/[,.!?;:]/g);
    return m ? m.length : 0;
}

function stripPunctuationAndCase(text: string): string {
    return text
        .toLowerCase()
        .replace(/[,.!?;:()[\]{}"“”'’]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

export function applyLocalPunctuation(rawText: string, langHint: string): { normalizedText: string; punctuatedText: string; changesApplied: number } {
    const normalized = normalizeSpaces(rawText);
    if (!normalized) return { normalizedText: '', punctuatedText: '', changesApplied: 0 };

    let out = normalized;
    let changes = 0;

    const cap = capitalizeFirst(out);
    out = cap.text;
    if (cap.changed) changes += 1;

    const connectors = [
        'então',
        'mas',
        'porém',
        'contudo',
        'porque',
        'por isso',
        'ou seja',
        'aliás',
        'enfim',
        'assim',
        'na verdade',
    ];

    for (const c of connectors) {
        const leading = addCommaAfterLeadingPhrase(out, c);
        out = leading.text;
        if (leading.changed) changes += 1;
    }

    for (const c of connectors) {
        if (c === 'então') continue;
        const middle = addCommaBeforePhrase(out, c);
        out = middle.text;
        if (middle.changed) changes += 1;
    }

    const isPt = (langHint || '').toLowerCase().startsWith('pt');
    const wantsQuestion = isPt && detectQuestion(out);
    if (!endsWithTerminalPunctuation(out)) {
        if (wantsQuestion) {
            out = `${out}?`;
            changes += 1;
        } else {
            const words = out.split(' ').filter(Boolean);
            if (words.length >= 3 && out.length >= 12) {
                out = `${out}.`;
                changes += 1;
            }
        }
    }

    const pDelta = Math.max(0, countPunctuationMarks(out) - countPunctuationMarks(normalized));
    const rawComparable = stripPunctuationAndCase(normalized);
    const outComparable = stripPunctuationAndCase(out);
    if (rawComparable !== outComparable) changes = Math.max(changes, 1);

    return { normalizedText: normalized, punctuatedText: out, changesApplied: Math.max(changes, pDelta) };
}

export function isSafePunctuationRefinement(baseText: string, refinedText: string): boolean {
    return stripPunctuationAndCase(baseText) === stripPunctuationAndCase(refinedText);
}

export function buildLocalOnlyResult(rawText: string, langHint: string): PunctuationPipelineResult {
    const started = performance.now();
    const local = applyLocalPunctuation(rawText, langHint);
    const latencyMs = Math.max(0, Math.round(performance.now() - started));
    return {
        rawText,
        normalizedText: local.normalizedText,
        punctuatedText: local.punctuatedText,
        engine: 'local-rules',
        latencyMs,
        changesApplied: local.changesApplied,
    };
}

