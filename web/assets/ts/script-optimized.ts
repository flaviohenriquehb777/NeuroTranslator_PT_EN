interface ISpeechRecognition {
    lang: string;
    continuous: boolean;
    interimResults: boolean;
    onresult: (ev: Event) => void;
    onerror: (ev: Event) => void;
    start: () => void;
    stop: () => void;
}
type SpeechState = { recognition: ISpeechRecognition | null; active: boolean; supported: boolean };
type TranslationState = { history: Array<Record<string, unknown>>; autoTranslate: boolean };
type AppElements = Record<string, HTMLElement | HTMLTextAreaElement | HTMLSelectElement | HTMLButtonElement | HTMLInputElement>;

class NeuroTranslatorWeb {
    speech: SpeechState;
    translation: TranslationState;
    elements: AppElements;
    lastTranslation: { text: string; language: string } | null;
    constructor() {
        this.speech = { recognition: null, active: false, supported: false };
        this.translation = { history: [], autoTranslate: true };
        this.elements = {};
        this.lastTranslation = null;
        this.init();
    }
    init() {
        this.initElements();
        this.initEventListeners();
        this.checkMobileCompatibility();
        this.checkBrowserSupport();
        // carregar configurações futuramente (stub)
    }
    initElements() {
        this.elements.sourceLanguage = document.getElementById('sourceLanguage') as HTMLSelectElement;
        this.elements.targetLanguage = document.getElementById('targetLanguage') as HTMLSelectElement;
        this.elements.sourceText = document.getElementById('sourceText') as HTMLTextAreaElement;
        this.elements.targetText = document.getElementById('targetText') as HTMLTextAreaElement;
        this.elements.translateBtn = document.getElementById('translateBtn') as HTMLButtonElement;
        this.elements.swapLanguages = document.getElementById('swapLanguages') as HTMLButtonElement;
        this.elements.toggleSpeech = document.getElementById('toggleSpeech') as HTMLButtonElement;
        this.elements.speechStatus = document.getElementById('speechStatus') as HTMLElement;
        this.elements.clearText = document.getElementById('clearText') as HTMLButtonElement;
        this.elements.copyTranslation = document.getElementById('copyTranslation') as HTMLButtonElement;
        this.elements.speakTranslation = document.getElementById('speakTranslation') as HTMLButtonElement;
        this.elements.autoTranslate = document.getElementById('autoTranslate') as HTMLInputElement;
        this.elements.historyContainer = document.getElementById('historyContainer') as HTMLElement;
        this.elements.clearHistory = document.getElementById('clearHistory') as HTMLButtonElement;
        this.elements.translationStatus = document.getElementById('translationStatus') as HTMLElement;
        this.elements.processingTime = document.getElementById('translationTime') as HTMLElement;
    }
    initEventListeners() {
        (this.elements.translateBtn as HTMLButtonElement).addEventListener('click', () => this.translateText());
        (this.elements.swapLanguages as HTMLButtonElement).addEventListener('click', () => this.swapLanguages());
        (this.elements.sourceText as HTMLTextAreaElement).addEventListener('input', () => this.onTextInput());
        (this.elements.toggleSpeech as HTMLButtonElement).addEventListener('click', () => this.toggleSpeech());
        (this.elements.clearText as HTMLButtonElement).addEventListener('click', () => this.clearText());
        (this.elements.copyTranslation as HTMLButtonElement).addEventListener('click', () => this.copyTranslation());
        (this.elements.speakTranslation as HTMLButtonElement).addEventListener('click', () => this.speakOutTranslation());
        (this.elements.clearHistory as HTMLButtonElement).addEventListener('click', () => this.clearHistory());
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }
    isMobileDevice() { return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent); }
    checkMobileCompatibility() { return true; }
    checkBrowserSupport() { this.speech.supported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window; }
    initSpeechRecognition() {
        type SRCons = new () => ISpeechRecognition;
        const w = window as unknown as { SpeechRecognition?: SRCons; webkitSpeechRecognition?: SRCons };
        const Cons = w.SpeechRecognition || w.webkitSpeechRecognition;
        if (!Cons) { this.speech.supported = false; return; }
        const rec = new Cons();
        const srcLang = (this.elements.sourceLanguage as HTMLSelectElement).value;
        rec.lang = srcLang === 'pt' ? 'pt-BR' : srcLang === 'en' ? 'en-US' : srcLang;
        rec.continuous = false;
        rec.interimResults = false;
        rec.onresult = (e: Event) => {
            const r = e as unknown as { results: Array<{ 0: { transcript: string } }> };
            const text = r.results[0][0].transcript;
            (this.elements.sourceText as HTMLTextAreaElement).value = text;
            this.onTextInput();
        };
        rec.onerror = () => { this.stopSpeech(); };
        this.speech.recognition = rec;
    }
    toggleSpeech() {
        if (!this.speech.recognition) this.initSpeechRecognition();
        if (!this.speech.recognition) return;
        this.speech.active ? this.stopSpeech() : this.startSpeech();
    }
    startSpeech() {
        try {
            this.speech.active = true;
            (this.elements.speechStatus as HTMLElement).textContent = '🎤 Reconhecimento: Ativado';
            (this.elements.toggleSpeech as HTMLButtonElement).classList.add('active');
            this.speech.recognition?.start();
        } catch { this.speech.active = false; }
    }
    stopSpeech() {
        try {
            this.speech.recognition?.stop();
        } finally {
            this.speech.active = false;
            (this.elements.speechStatus as HTMLElement).textContent = '🎤 Reconhecimento: Desativado';
            (this.elements.toggleSpeech as HTMLButtonElement).classList.remove('active');
        }
    }
    async translateText() {
        const src = (this.elements.sourceText as HTMLTextAreaElement).value.trim();
        const tgt = this.elements.targetText as HTMLTextAreaElement;
        const status = this.elements.translationStatus as HTMLElement;
        const sourceLang = (this.elements.sourceLanguage as HTMLSelectElement).value;
        const targetLang = (this.elements.targetLanguage as HTMLSelectElement).value;
        if (!src) { status.textContent = 'Nada para traduzir'; tgt.value = ''; return; }
        status.textContent = 'Traduzindo...';
        (this.elements.translateBtn as HTMLButtonElement)?.setAttribute('disabled', 'true');
        (this.elements.translateBtn as HTMLButtonElement)?.setAttribute('aria-busy', 'true');
        const started = performance.now();
        try {
            const first = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(src)}&langpair=${sourceLang}|${targetLang}`;
            let translated = '';
            const r0 = await fetch(first, { headers: { 'Accept': 'application/json' }, cache: 'no-store' }).catch(err => { console.warn('MyMemory erro', err); return null; });
            if (r0 && r0.ok) {
                const j0 = await r0.json() as { responseData?: { translatedText?: string } };
                translated = j0.responseData?.translatedText || '';
            }
            if (!translated) {
                const proxy = (location.hostname === 'localhost' || location.hostname === '127.0.0.1') ? 'http://localhost:3000/translate' : null;
                const endpoints = [
                    proxy,
                    'https://translate.astian.org/translate',
                    'https://libretranslate.de/translate',
                    'https://libretranslate.com/translate',
                    'https://translate.argosopentech.com/translate'
                ].filter(Boolean) as string[];
                for (const url of endpoints) {
                    const r = await fetch(url, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        referrerPolicy: 'no-referrer',
                        body: JSON.stringify({ q: src, source: sourceLang === targetLang ? 'auto' : sourceLang, target: targetLang, format: 'text' })
                    }).catch(err => { console.warn('Endpoint erro', url, err); return null; });
                    if (r && r.ok) {
                        const d = await r.json() as { translatedText?: string };
                        translated = d.translatedText || '';
                        if (translated) { console.log('Traduzido por', url); break; }
                    } else {
                        console.warn('Falha endpoint', url, r?.status);
                    }
                }
            }
            translated = this.preserveCasing(src, translated || src);
            tgt.value = translated;
            status.textContent = 'Pronto para traduzir';
        } catch {
            tgt.value = src;
            status.textContent = 'Falha na tradução';
        } finally {
            const ms = Math.round(performance.now() - started);
            (this.elements.processingTime as HTMLElement).textContent = `${ms} ms`;
            (this.elements.translateBtn as HTMLButtonElement)?.removeAttribute('disabled');
            (this.elements.translateBtn as HTMLButtonElement)?.setAttribute('aria-busy', 'false');
        }
    }

    preserveCasing(src: string, dst: string): string {
        const hasLetter = /[A-Za-zÀ-ÖØ-öø-ÿ]/.test(src);
        if (!hasLetter) return dst;
        const letters = src.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ]/g, '');
        const isLower = letters.length > 0 && letters === letters.toLowerCase();
        const isUpper = letters.length > 0 && letters === letters.toUpperCase();
        if (isLower) return dst.toLowerCase();
        if (isUpper) return dst.toUpperCase();
        const srcTokens = this.tokenize(src);
        const dstTokens = this.tokenize(dst);
        const pattern = this.wordUpperPattern(srcTokens);
        const ratio = pattern.length ? pattern.filter(Boolean).length / pattern.length : 0;
        if (ratio >= 0.6) {
            const applied = this.applyWordPattern(dstTokens, pattern);
            return applied;
        }
        const srcSent = src.match(/[^.!?]+[.!?]*/g) || [src];
        const dstSent = dst.match(/[^.!?]+[.!?]*/g) || [dst];
        const n = Math.min(srcSent.length, dstSent.length);
        const adjusted: string[] = [];
        for (let i = 0; i < n; i++) {
            const s = srcSent[i];
            const d = dstSent[i];
            const upper = this.isFirstAlphaUpper(s);
            adjusted.push(this.adjustFirstAlpha(d, upper));
        }
        for (let i = n; i < dstSent.length; i++) adjusted.push(dstSent[i]);
        return adjusted.join('');
    }

    isFirstAlphaUpper(text: string): boolean {
        for (const ch of Array.from(text)) {
            if (/[A-Za-zÀ-ÖØ-öø-ÿ]/.test(ch)) return ch === ch.toUpperCase();
        }
        return false;
    }

    adjustFirstAlpha(text: string, upper: boolean): string {
        const arr = Array.from(text);
        for (let i = 0; i < arr.length; i++) {
            const ch = arr[i];
            if (/[A-Za-zÀ-ÖØ-öø-ÿ]/.test(ch)) { arr[i] = upper ? ch.toUpperCase() : ch.toLowerCase(); break; }
        }
        return arr.join('');
    }

    tokenize(text: string): { t: string; w: boolean }[] {
        const parts = text.match(/[A-Za-zÀ-ÖØ-öø-ÿ]+|[^A-Za-zÀ-ÖØ-öø-ÿ]+/g) || [text];
        return parts.map(p => ({ t: p, w: /[A-Za-zÀ-ÖØ-öø-ÿ]/.test(p) }));
    }

    wordUpperPattern(tokens: { t: string; w: boolean }[]): boolean[] {
        const pattern: boolean[] = [];
        for (const tok of tokens) {
            if (!tok.w) continue;
            pattern.push(this.isFirstAlphaUpper(tok.t));
        }
        return pattern;
    }

    applyWordPattern(tokens: { t: string; w: boolean }[], pattern: boolean[]): string {
        const out: string[] = [];
        let wi = 0;
        for (const tok of tokens) {
            if (!tok.w) { out.push(tok.t); continue; }
            const p = wi < pattern.length ? pattern[wi] : false;
            wi++;
            out.push(this.adjustFirstAlpha(tok.t, p));
        }
        return out.join('');
    }
    swapLanguages() {
        const s = this.elements.sourceLanguage as HTMLSelectElement;
        const t = this.elements.targetLanguage as HTMLSelectElement;
        [s.value, t.value] = [t.value, s.value];
        const srcText = this.elements.sourceText as HTMLTextAreaElement;
        const tgtText = this.elements.targetText as HTMLTextAreaElement;
        [srcText.value, tgtText.value] = [tgtText.value, srcText.value];
        this.onTextInput();
    }
    clearText() {
        (this.elements.sourceText as HTMLTextAreaElement).value = '';
        this.onTextInput();
    }
    async copyTranslation() {
        const txt = (this.elements.targetText as HTMLTextAreaElement).value;
        try { await navigator.clipboard.writeText(txt); } catch { void 0 }
    }
    speakOutTranslation() {
        const txt = (this.elements.targetText as HTMLTextAreaElement).value.trim();
        if (!txt) return;
        const utter = new SpeechSynthesisUtterance(txt);
        const lang = (this.elements.targetLanguage as HTMLSelectElement).value;
        utter.lang = lang === 'pt' ? 'pt-BR' : lang === 'en' ? 'en-US' : lang;
        speechSynthesis.cancel();
        speechSynthesis.speak(utter);
    }
    onTextInput() {
        const src = (this.elements.sourceText as HTMLTextAreaElement).value;
        const count = document.getElementById('charCount');
        if (count) count.textContent = `${src.length} caracteres`;
        const auto = (this.elements.autoTranslate as HTMLInputElement)?.checked;
        if (auto) this.translateText();
    }
    updateHistoryDisplay() { /* render history later */ }
    clearHistory() {}
    handleKeyboard(event: KeyboardEvent) { void event; }
}
document.addEventListener('DOMContentLoaded', () => {
    (window as unknown as { neuroTranslator: NeuroTranslatorWeb }).neuroTranslator = new NeuroTranslatorWeb();
    if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
        const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        if (isLocal) {
            navigator.serviceWorker.getRegistrations().then(regs => { regs.forEach(reg => reg.unregister()); });
        } else {
            navigator.serviceWorker.register('/sw.js').catch(() => {});
        }
    }
});