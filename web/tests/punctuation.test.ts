import { describe, it, expect } from 'vitest';
import { applyLocalPunctuation, isSafePunctuationRefinement } from '../assets/ts/punctuation/localRules.ts';
import { PunctuationPipeline } from '../assets/ts/punctuation/pipeline.ts';

describe('pontuação local (offline)', () => {
    it('adiciona interrogação e capitaliza em pergunta simples', () => {
        const r = applyLocalPunctuation('onde fica a estação mais próxima', 'pt');
        expect(r.punctuatedText).toBe('Onde fica a estação mais próxima?');
    });

    it('insere vírgula antes de conector e finaliza com ponto', () => {
        const r = applyLocalPunctuation('eu fui ao mercado mas não encontrei pão', 'pt');
        expect(r.punctuatedText).toContain(', mas ');
        expect(r.punctuatedText.endsWith('.')).toBe(true);
    });

    it('não altera palavras ao validar refinamento', () => {
        expect(isSafePunctuationRefinement('Bom dia', 'Bom dia!')).toBe(true);
        expect(isSafePunctuationRefinement('Bom dia', 'Boa noite')).toBe(false);
    });
});

describe('pipeline de pontuação', () => {
    it('faz fallback local se refinamento remoto falhar', async () => {
        const pipeline = new PunctuationPipeline();
        const out = await pipeline.punctuateSpeechFinal('onde fica a estação mais próxima', 'pt', {
            apiBase: 'https://example.invalid',
            enableClaudeRefine: true,
            fetchWithTimeout: async () => { throw new Error('offline'); },
            isOnline: true,
            minCharsForClaude: 10,
            minIntervalMs: 0,
        });
        expect(out.engine).toBe('local-fallback-after-claude-failure');
        expect(out.punctuatedText).toBe('Onde fica a estação mais próxima?');
    });
});

