export type PunctuationEngine = 'local-rules' | 'claude-refine' | 'local-fallback-after-claude-failure';

export type PunctuationPipelineResult = {
    rawText: string;
    normalizedText: string;
    punctuatedText: string;
    engine: PunctuationEngine;
    latencyMs: number;
    changesApplied: number;
};

export type FetchWithTimeout = (url: string, init: RequestInit, timeoutMs: number) => Promise<Response>;

