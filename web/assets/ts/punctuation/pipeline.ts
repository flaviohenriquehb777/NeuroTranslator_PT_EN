import type { FetchWithTimeout, PunctuationEngine, PunctuationPipelineResult } from './types';
import { applyLocalPunctuation, buildLocalOnlyResult, isSafePunctuationRefinement } from './localRules';
import { refinePunctuationWithClaude } from './claudeRefine';

export type PunctuationPipelineConfig = {
    apiBase: string;
    enableClaudeRefine: boolean;
    fetchWithTimeout: FetchWithTimeout;
    isOnline: boolean;
    minCharsForClaude: number;
    minIntervalMs: number;
};

export class PunctuationPipeline {
    private lastClaudeAttemptAt = 0;

    async punctuateSpeechFinal(rawText: string, langHint: string, cfg: PunctuationPipelineConfig): Promise<PunctuationPipelineResult> {
        const started = performance.now();
        const local = applyLocalPunctuation(rawText, langHint);
        const baseResult: PunctuationPipelineResult = {
            rawText,
            normalizedText: local.normalizedText,
            punctuatedText: local.punctuatedText,
            engine: 'local-rules',
            latencyMs: 0,
            changesApplied: local.changesApplied,
        };

        const allowClaude = cfg.enableClaudeRefine
            && cfg.isOnline
            && baseResult.punctuatedText.length >= cfg.minCharsForClaude
            && (performance.now() - this.lastClaudeAttemptAt) >= cfg.minIntervalMs;

        if (!allowClaude) {
            baseResult.latencyMs = Math.max(0, Math.round(performance.now() - started));
            return baseResult;
        }

        this.lastClaudeAttemptAt = performance.now();
        let engine: PunctuationEngine = 'claude-refine';
        let punctuatedText = baseResult.punctuatedText;

        try {
            const refined = await refinePunctuationWithClaude({
                text: punctuatedText,
                langHint,
                apiBase: cfg.apiBase,
                fetchWithTimeout: cfg.fetchWithTimeout,
                timeoutMs: 6500,
            });

            if (isSafePunctuationRefinement(punctuatedText, refined)) {
                punctuatedText = refined;
                engine = 'claude-refine';
            } else {
                engine = 'local-fallback-after-claude-failure';
            }
        } catch {
            engine = 'local-fallback-after-claude-failure';
        }

        const latencyMs = Math.max(0, Math.round(performance.now() - started));
        const extraChanges = punctuatedText && punctuatedText !== baseResult.punctuatedText ? 1 : 0;
        return {
            ...baseResult,
            punctuatedText: punctuatedText || baseResult.punctuatedText,
            engine,
            latencyMs,
            changesApplied: baseResult.changesApplied + extraChanges,
        };
    }
}

export function punctuateLocalOnly(rawText: string, langHint: string): PunctuationPipelineResult {
    return buildLocalOnlyResult(rawText, langHint);
}

