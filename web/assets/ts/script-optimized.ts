/* ═══════════════════════════════════════════════════════════════
   NeuroTranslator v4.0 — Advanced Neural Translation Engine
   © 2025 Flávio Henrique Barbosa — MIT License
   ═══════════════════════════════════════════════════════════════ */

// ─── Types & Interfaces ────────────────────────────────────────

interface ISpeechRecognition {
    lang: string;
    continuous: boolean;
    interimResults: boolean;
    onresult: (ev: Event) => void;
    onerror: (ev: Event) => void;
    onend: () => void;
    start: () => void;
    stop: () => void;
}

interface LangConfig {
    code: string;       // short code used in API
    bcp47: string;      // BCP 47 tag for speech
    label: string;      // display name
    flag: string;       // emoji flag
    voiceKeywords: string[];  // preferred voice name fragments
}

interface TranslationEntry {
    id: string;
    source: string;
    target: string;
    sourceLang: string;
    targetLang: string;
    confidence: number;
    timestamp: number;
}

interface VoiceScore {
    voice: SpeechSynthesisVoice;
    score: number;
}

// ─── Language Configuration ────────────────────────────────────

const LANGUAGES: Record<string, LangConfig> = {
    pt: { code: 'pt', bcp47: 'pt-BR', label: 'Português', flag: '🇧🇷', voiceKeywords: ['Brazilian', 'Brasil', 'Luciana', 'Daniel'] },
    en: { code: 'en', bcp47: 'en-US', label: 'Inglês', flag: '🇺🇸', voiceKeywords: ['US', 'American', 'Samantha', 'Alex'] },
    es: { code: 'es', bcp47: 'es-ES', label: 'Espanhol', flag: '🇪🇸', voiceKeywords: ['Spain', 'España', 'Monica', 'Jorge'] },
    fr: { code: 'fr', bcp47: 'fr-FR', label: 'Francês', flag: '🇫🇷', voiceKeywords: ['France', 'Thomas', 'Amelie'] },
    de: { code: 'de', bcp47: 'de-DE', label: 'Alemão', flag: '🇩🇪', voiceKeywords: ['Germany', 'Deutschland', 'Anna', 'Markus'] },
    zh: { code: 'zh', bcp47: 'zh-CN', label: 'Chinês', flag: '🇨🇳', voiceKeywords: ['China', 'Mandarin', 'Ting-Ting'] },
    ja: { code: 'ja', bcp47: 'ja-JP', label: 'Japonês', flag: '🇯🇵', voiceKeywords: ['Japan', 'Kyoko', 'Otoya'] },
    it: { code: 'it', bcp47: 'it-IT', label: 'Italiano', flag: '🇮🇹', voiceKeywords: ['Italy', 'Italia', 'Alice', 'Luca'] },
    ru: { code: 'ru', bcp47: 'ru-RU', label: 'Russo', flag: '🇷🇺', voiceKeywords: ['Russia', 'Milena', 'Yuri'] },
    da: { code: 'da', bcp47: 'da-DK', label: 'Dinamarquês', flag: '🇩🇰', voiceKeywords: ['Danish', 'Danmark', 'Sara'] },
    fi: { code: 'fi', bcp47: 'fi-FI', label: 'Finlandês', flag: '🇫🇮', voiceKeywords: ['Finnish', 'Suomi', 'Satu'] },
    nb: { code: 'nb', bcp47: 'nb-NO', label: 'Norueguês', flag: '🇳🇴', voiceKeywords: ['Norwegian', 'Norge', 'Nora'] },
    el: { code: 'el', bcp47: 'el-GR', label: 'Grego', flag: '🇬🇷', voiceKeywords: ['Greek', 'Melina'] },
};

const LANG_ORDER = ['pt', 'en', 'es', 'fr', 'de', 'it', 'ru', 'zh', 'ja', 'da', 'fi', 'nb', 'el'];

// ─── Trigram Language Detection ────────────────────────────────

const TRIGRAM_PROFILES: Record<string, string[]> = {
    pt: [' de', 'de ', ' a ', 'ão ', ' co', 'os ', 'ent', ' o ', 'nte', 'do ', ' da', 'es ', 'da ', 'as ', ' qu', 'que', 'ade', ' se', 'con', ' e ', 'ção', 'com', ' pa', 'ra ', ' em', 'te ', 'ar ', 'em ', 'par', 'ão', 'to ', 'sta', 'men', 'nto', 'pro', ' pr', 'ões', ' es', 'ist', 'ma ', 'er ', 'est', 'tra', 'or ', 'ica'],
    en: [' th', 'the', 'he ', 'ed ', ' to', ' an', 'nd ', 'ion', ' of', 'of ', 'ing', 'ng ', 'an ', 'er ', ' in', ' a ', 'in ', 'tio', 'on ', 'is ', 'ati', 'it ', ' is', 'al ', 'es ', 're ', 'hat', 'at ', 'tha', ' ha', 'as ', 'en ', ' co', ' re', 'or ', 'nt ', 'ent', 'and', 'to ', 'st ', ' be', ' fo', 'for', 'ons', 'men'],
    es: [' de', 'de ', ' la', 'la ', 'ón ', 'os ', ' el', 'en ', 'ión', 'es ', ' en', 'el ', 'ció', 'ent', 'as ', 'con', ' co', ' lo', ' un', ' se', 'los', ' y ', 'nte', 'aci', ' qu', 'do ', 'que', 'ar ', 'del', ' pa', 'ra ', 'al ', 'ado', 'par', 'nes', 'sta', 'est', 'res', 'co ', 'un ', 'ero', 'ida', 'ter', 'io ', 'tra'],
    fr: [' de', 'de ', ' le', 'es ', 'ent', 'le ', 'les', 'ion', 'la ', ' la', ' et', ' pa', 'nt ', 'tio', 'on ', 'en ', ' co', 'et ', 'ne ', ' un', 'ons', 'ns ', 're ', 'que', ' en', 'par', 'ati', 'un ', 'des', ' le', 'ur ', 'men', 'con', 'ait', 'er ', 'est', 'ou ', 'eur', 'it ', 'uis', ' qu', 'ant', ' se', 'al ', ' pr'],
    de: [' de', 'en ', 'er ', 'der', 'die', 'ie ', 'ein', 'che', 'sch', 'den', 'ich', 'ch ', 'und', 'nd ', 'in ', 'ten', ' di', 'te ', ' un', 'ung', 'gen', 'eit', 'ber', 'ver', 'ine', 'es ', ' da', 'ne ', 'ede', ' au', 'auf', 'ach', 'lic', 'hen', ' ei', 'das', ' be', 'ren', 'ist', 'ter', 'nte', ' ge', 'ges', 'ste', 'and'],
    zh: ['的 ', ' 的', '是 ', ' 是', '在 ', ' 在', '了 ', ' 了', '不 ', ' 不', '一 ', ' 一', '有 ', ' 有', '大 ', '国 ', '人 ', ' 人', '中 ', ' 中', '为 ', '来 ', '和 ', ' 和', '上 ', ' 上', '个 ', '以 ', '我 ', '这 ', '到 ', ' 到', '们 ', '地 ', '说 ', '年 ', '会 ', '他 ', '时 ', '对 ', '出 ', '也 ', '要 ', '就 ', '可 '],
    ja: ['の ', 'した', 'して', 'いる', 'ない', 'ている', 'ます', 'です', 'った', 'れた', 'には', 'から', 'ての', 'った', 'tion', 'する', 'ment', 'ting', 'ated', 'ness', 'able', 'ible', 'ence', 'ance', 'ment', 'ical', 'ious', 'eous', 'った', 'って', 'った', 'ース', 'ション', 'ment', 'ered', 'tion', 'ated', 'ness', 'ment', 'able', 'tion', 'ness', 'ment', 'ical', 'tion'],
    it: [' di', 'di ', ' la', 'la ', 'ion', ' de', 'ent', 'to ', 'ne ', 'one', ' in', 'zio', 'in ', ' co', ' un', 'del', 'ell', 'lla', 'ato', 'azi', 'le ', 'per', 'ta ', 'nte', 'con', 'ono', 'no ', 'che', ' il', 'il ', 'na ', 'ri ', 'eri', 'li ', 'tta', 'lo ', 'ti ', 'sta', ' pe', 'ter', 'non', 're ', 'un ', 'men', 'al '],
    ru: ['ов ', 'ть ', 'ени', 'ост', ' по', ' на', 'ние', ' не', 'ани', ' пр', 'ста', ' ко', 'на ', 'ных', 'ого', ' в ', ' и ', 'ии ', ' ка', 'ать', 'ной', 'ого', 'ать', 'его', 'по ', 'ти ', 'и п', 'и с', 'про', 'ера', 'ие ', 'ной', 'но ', 'ель', 'сти', 'тел', 'ает', 'нны', 'оль', 'ого', 'ват', 'при', 'пре', 'ной', 'кон'],
    da: ['er ', 'en ', 'de ', 'det', 'et ', ' de', ' og', 'og ', 'der', 'den', ' en', 'for', 'at ', ' at', 'nde', 'gen', 'til', 'ing', ' fo', 'r e', 'ige', ' i ', 'ed ', 'ede', ' ti', 'ung', 'ge ', 'af ', ' af', ' me', 'med', 'ter', 'ste', 'and', 'ern', ' ha', 'har', 'ere', 'on ', 'nd ', ' er', 'som', 'lig', 'ell', 'lse'],
    fi: ['en ', 'in ', 'ise', 'an ', 'ist', 'tä ', 'ja ', ' ja', 'ta ', 'sen', 'iin', 'sta', 'ssa', ' on', 'on ', 'lla', 'lle', 'een', 'ais', 'den', 'tta', 'lta', 'nen', 'ksi', 'uus', 'nne', 'ine', ' ka', 'ise', 'mis', 'tti', 'oit', 'un ', 'tee', 'isi', 'tte', 'ään', 'ssä', 'stä', 'llä', 'llé', 'sti', 'tte', 'uut', 'sel'],
    nb: ['er ', 'en ', 'et ', 'for', 'det', 'de ', 'og ', ' og', 'den', ' de', ' en', 'til', ' fo', 'ing', 'ter', 'som', 'at ', ' at', 'med', ' me', ' ti', 'nde', ' i ', ' ha', 'har', 'ige', 'gen', 'ste', 'ere', 'and', 'ern', ' så', 'der', 'lle', 'ell', 'ene', 'lig', ' vi', 'ver', 'ger', ' er', 'om ', ' so', 'isk', 'av '],
    el: ['ων ', 'ται', 'της', 'ης ', 'και', 'αι ', 'ον ', 'τη ', ' κα', ' τη', 'ερι', 'ου ', 'ν τ', 'ικο', 'ένα', 'στη', 'για', 'ια ', ' στ', 'ρισ', 'ρος', 'από', 'πό ', 'ος ', 'ισμ', 'νικ', 'σμό', 'ντα', 'μέν', 'ένο', 'ατα', 'δια', 'ελλ', 'λλη', 'ληθ', 'λσε', 'ική', 'ικά', 'ένη', 'ησε', 'ηση', 'ητα', 'θεί', 'εία', 'ίας'],
};

function detectLanguage(text: string): { lang: string; confidence: number } | null {
    if (text.length < 10) return null;

    const sample = text.toLowerCase().slice(0, 500);
    const textTrigrams = new Map<string, number>();
    for (let i = 0; i < sample.length - 2; i++) {
        const tri = sample.substring(i, i + 3);
        textTrigrams.set(tri, (textTrigrams.get(tri) || 0) + 1);
    }

    let bestLang = '';
    let bestScore = 0;
    let secondScore = 0;

    for (const [lang, profile] of Object.entries(TRIGRAM_PROFILES)) {
        let score = 0;
        for (const tri of profile) {
            score += textTrigrams.get(tri) || 0;
        }
        if (score > bestScore) {
            secondScore = bestScore;
            bestScore = score;
            bestLang = lang;
        } else if (score > secondScore) {
            secondScore = score;
        }
    }

    if (bestScore === 0) return null;
    const confidence = Math.min(((bestScore - secondScore) / bestScore) * 100, 99);
    if (confidence < 15) return null;
    return { lang: bestLang, confidence: Math.round(confidence) };
}

// ─── Voice Engine ──────────────────────────────────────────────

class VoiceEngine {
    private voiceCache = new Map<string, SpeechSynthesisVoice>();
    private voicesLoaded = false;

    constructor() {
        this.loadVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = () => this.loadVoices();
        }
    }

    private loadVoices(): void {
        const voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            this.voicesLoaded = true;
            this.voiceCache.clear();
        }
    }

    scoreVoice(voice: SpeechSynthesisVoice, langConfig: LangConfig): number {
        let score = 0;
        const name = voice.name.toLowerCase();
        const lang = voice.lang.toLowerCase();

        // Neural / premium quality keywords
        if (name.includes('neural')) score += 20;
        if (name.includes('premium')) score += 16;
        if (name.includes('enhanced')) score += 12;
        if (name.includes('natural')) score += 10;
        if (name.includes('wavenet')) score += 18;
        if (name.includes('online')) score += 4;

        // Language-specific preferred voice names
        for (const kw of langConfig.voiceKeywords) {
            if (name.includes(kw.toLowerCase())) score += 6;
        }

        // Prefer cloud voices (usually higher quality)
        if (!voice.localService) score += 3;

        // Prefer exact lang match
        const targetBcp = langConfig.bcp47.toLowerCase();
        if (lang === targetBcp) score += 5;
        else if (lang.startsWith(langConfig.code)) score += 2;

        return score;
    }

    getBestVoice(langCode: string): SpeechSynthesisVoice | null {
        if (this.voiceCache.has(langCode)) {
            return this.voiceCache.get(langCode)!;
        }

        const config = LANGUAGES[langCode];
        if (!config) return null;

        const voices = speechSynthesis.getVoices();
        const candidates: VoiceScore[] = [];

        for (const voice of voices) {
            const vLang = voice.lang.toLowerCase();
            const targetLang = config.bcp47.toLowerCase();
            if (vLang.startsWith(config.code) || vLang === targetLang) {
                candidates.push({ voice, score: this.scoreVoice(voice, config) });
            }
        }

        if (candidates.length === 0) return null;
        candidates.sort((a, b) => b.score - a.score);
        const best = candidates[0].voice;
        this.voiceCache.set(langCode, best);
        return best;
    }

    warmUp(langCode: string): void {
        const voice = this.getBestVoice(langCode);
        if (!voice) return;
        const utter = new SpeechSynthesisUtterance('');
        utter.voice = voice;
        utter.volume = 0;
        utter.lang = LANGUAGES[langCode]?.bcp47 || langCode;
        try { speechSynthesis.speak(utter); } catch { /* silent */ }
    }

    speakText(text: string, langCode: string, onStart?: () => void, onEnd?: () => void): void {
        if (!text.trim()) return;
        speechSynthesis.cancel();

        const sentences = text.match(/[^.!?。！？]+[.!?。！？]*/g) || [text];
        const config = LANGUAGES[langCode];
        const bcp47 = config?.bcp47 || langCode;
        const voice = this.getBestVoice(langCode);

        let index = 0;
        const speakNext = () => {
            if (index >= sentences.length) {
                onEnd?.();
                return;
            }
            const sentence = sentences[index].trim();
            if (!sentence) { index++; speakNext(); return; }

            const utter = new SpeechSynthesisUtterance(sentence);
            utter.lang = bcp47;
            if (voice) utter.voice = voice;
            utter.rate = 0.95;
            utter.pitch = 1.0;
            utter.volume = 1.0;

            if (index === 0) {
                utter.onstart = () => onStart?.();
            }
            utter.onend = () => {
                index++;
                if (index < sentences.length) {
                    setTimeout(speakNext, 280);
                } else {
                    onEnd?.();
                }
            };
            utter.onerror = () => {
                index++;
                speakNext();
            };
            speechSynthesis.speak(utter);
        };
        speakNext();
    }
}

// ─── Main Application ──────────────────────────────────────────

class NeuroTranslatorWeb {
    private voiceEngine: VoiceEngine;
    private recognition: ISpeechRecognition | null = null;
    private speechActive = false;
    private speechSupported = false;
    private voiceInputTriggered = false;

    private autoTranslateEnabled = true;
    private debounceTimer: ReturnType<typeof setTimeout> | null = null;

    private history: TranslationEntry[] = [];
    private contextMemory: TranslationEntry[] = [];
    private readonly MAX_CONTEXT = 5;
    private readonly MAX_HISTORY = 50;

    private drawerOpen = false;
    private openDropdown: 'source' | 'target' | null = null;

    // DOM references
    private els: Record<string, HTMLElement> = {};

    constructor() {
        this.voiceEngine = new VoiceEngine();
        this.init();
    }

    // ─── Initialisation ─────────────────────────────────────

    private init(): void {
        this.cacheElements();
        this.buildLanguageDropdowns();
        this.bindEvents();
        this.checkBrowserSupport();
        this.loadHistory();
        this.loadContextMemory();
        this.warmUpTargetVoice();
    }

    private cacheElements(): void {
        const ids = [
            'sourceText', 'targetText', 'translateBtn', 'swapLanguages',
            'toggleSpeech', 'speechStatus', 'clearText', 'copyTranslation',
            'speakTranslation', 'autoTranslate', 'historyContainer',
            'clearHistory', 'translationStatus', 'translationTime',
            'charCount', 'sourceDropdown', 'targetDropdown', 'sourceDropdownTrigger',
            'targetDropdownTrigger', 'sourceDropdownMenu', 'targetDropdownMenu',
            'sourceDropdownCurrent', 'targetDropdownCurrent', 'confidenceBar',
            'confidenceText', 'detectedLangBadge', 'historyDrawer',
            'historyDrawerOverlay', 'openHistoryBtn', 'closeHistoryBtn',
            'historyFilter', 'shortcutsModal', 'shortcutsBtn',
            'closeShortcuts', 'autoTranslateToggle',
        ];
        for (const id of ids) {
            const el = document.getElementById(id);
            if (el) this.els[id] = el;
        }
    }

    private bindEvents(): void {
        this.on('translateBtn', 'click', () => this.translateText());
        this.on('swapLanguages', 'click', () => this.swapLanguages());
        this.on('sourceText', 'input', () => this.onTextInput());
        this.on('toggleSpeech', 'click', () => this.toggleSpeech());
        this.on('clearText', 'click', () => this.clearText());
        this.on('copyTranslation', 'click', () => this.copyTranslation());
        this.on('speakTranslation', 'click', () => this.speakOutTranslation());
        this.on('clearHistory', 'click', () => this.clearHistory());
        this.on('sourceDropdownTrigger', 'click', () => this.toggleDropdown('source'));
        this.on('targetDropdownTrigger', 'click', () => this.toggleDropdown('target'));
        this.on('openHistoryBtn', 'click', () => this.toggleDrawer(true));
        this.on('closeHistoryBtn', 'click', () => this.toggleDrawer(false));
        this.on('historyDrawerOverlay', 'click', () => this.toggleDrawer(false));
        this.on('shortcutsBtn', 'click', () => this.toggleShortcutsModal(true));
        this.on('closeShortcuts', 'click', () => this.toggleShortcutsModal(false));
        this.on('autoTranslateToggle', 'change', () => {
            this.autoTranslateEnabled = (this.els['autoTranslateToggle'] as HTMLInputElement)?.checked ?? true;
        });

        // Language filter for history
        this.on('historyFilter', 'change', () => this.renderHistory());

        document.addEventListener('click', (e) => this.handleOutsideClick(e));
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    private on(id: string, event: string, fn: () => void): void {
        this.els[id]?.addEventListener(event, fn);
    }

    private checkBrowserSupport(): void {
        const w = window as unknown as { SpeechRecognition?: unknown; webkitSpeechRecognition?: unknown };
        this.speechSupported = !!(w.SpeechRecognition || w.webkitSpeechRecognition);
    }

    // ─── Language Custom Dropdowns ──────────────────────────

    private selectedSource = 'pt';
    private selectedTarget = 'en';

    private buildLanguageDropdowns(): void {
        this.renderDropdownOptions('source');
        this.renderDropdownOptions('target');
        this.updateDropdownCurrent('source');
        this.updateDropdownCurrent('target');
    }

    private renderDropdownOptions(which: 'source' | 'target'): void {
        const menu = this.els[which === 'source' ? 'sourceDropdownMenu' : 'targetDropdownMenu'];
        const selected = which === 'source' ? this.selectedSource : this.selectedTarget;
        if (!menu) return;
        menu.innerHTML = '';

        for (const code of LANG_ORDER) {
            const lang = LANGUAGES[code];
            const option = document.createElement('button');
            option.className = `lang-dropdown-option${code === selected ? ' active' : ''}`;
            option.type = 'button';
            option.setAttribute('role', 'option');
            option.setAttribute('aria-selected', String(code === selected));
            option.setAttribute('data-lang', code);
            option.innerHTML = `<span class="dropdown-option-flag">${lang.flag}</span><span class="dropdown-option-label">${lang.label}</span>`;
            option.addEventListener('click', () => {
                this.selectLanguage(which, code);
                this.closeDropdowns();
                this.haptic();
            });
            menu.appendChild(option);
        }
    }

    private updateDropdownCurrent(which: 'source' | 'target'): void {
        const selected = which === 'source' ? this.selectedSource : this.selectedTarget;
        const current = this.els[which === 'source' ? 'sourceDropdownCurrent' : 'targetDropdownCurrent'];
        if (!current) return;
        const lang = LANGUAGES[selected];
        current.innerHTML = `<span class="dropdown-current-flag">${lang.flag}</span><span class="dropdown-current-label">${lang.label}</span>`;
    }

    private toggleDropdown(which: 'source' | 'target'): void {
        const sourceWrap = this.els['sourceDropdown'];
        const targetWrap = this.els['targetDropdown'];
        if (!sourceWrap || !targetWrap) return;

        const willOpen = this.openDropdown !== which;
        this.closeDropdowns();
        if (willOpen) {
            this.openDropdown = which;
            const wrap = which === 'source' ? sourceWrap : targetWrap;
            const trigger = this.els[which === 'source' ? 'sourceDropdownTrigger' : 'targetDropdownTrigger'];
            wrap.classList.add('open');
            trigger?.setAttribute('aria-expanded', 'true');
        }
    }

    private closeDropdowns(): void {
        this.openDropdown = null;
        this.els['sourceDropdown']?.classList.remove('open');
        this.els['targetDropdown']?.classList.remove('open');
        this.els['sourceDropdownTrigger']?.setAttribute('aria-expanded', 'false');
        this.els['targetDropdownTrigger']?.setAttribute('aria-expanded', 'false');
    }

    private handleOutsideClick(e: Event): void {
        const target = e.target as Node | null;
        if (!target) return;
        const sourceWrap = this.els['sourceDropdown'];
        const targetWrap = this.els['targetDropdown'];
        if (sourceWrap?.contains(target) || targetWrap?.contains(target)) return;
        this.closeDropdowns();
    }

    private selectLanguage(which: 'source' | 'target', code: string): void {
        if (which === 'source') {
            if (code === this.selectedSource) return;
            const previousSource = this.selectedSource;
            this.selectedSource = code;
            if (this.selectedSource === this.selectedTarget) {
                this.selectedTarget = previousSource;
            }
            this.onSourceLangChange();
            this.onTargetLangChange();
            return;
        }

        if (code === this.selectedTarget) return;
        this.selectedTarget = code;
        this.onTargetLangChange();
    }

    private onSourceLangChange(): void {
        this.renderDropdownOptions('source');
        this.updateDropdownCurrent('source');
        this.voiceEngine.warmUp(this.selectedSource);
        // Re-detect if needed
        const txt = (this.els['sourceText'] as HTMLTextAreaElement)?.value;
        if (txt && this.autoTranslateEnabled) this.debouncedTranslate();
    }

    private onTargetLangChange(): void {
        this.renderDropdownOptions('target');
        this.updateDropdownCurrent('target');
        this.warmUpTargetVoice();
        const txt = (this.els['sourceText'] as HTMLTextAreaElement)?.value;
        if (txt && this.autoTranslateEnabled) this.debouncedTranslate();
    }

    private warmUpTargetVoice(): void {
        this.voiceEngine.warmUp(this.selectedTarget);
    }

    // ─── Speech Recognition ─────────────────────────────────

    private initSpeechRecognition(): void {
        type SRCons = new () => ISpeechRecognition;
        const w = window as unknown as { SpeechRecognition?: SRCons; webkitSpeechRecognition?: SRCons };
        const Cons = w.SpeechRecognition || w.webkitSpeechRecognition;
        if (!Cons) { this.speechSupported = false; return; }

        const rec = new Cons();
        const config = LANGUAGES[this.selectedSource];
        rec.lang = config?.bcp47 || this.selectedSource;
        rec.continuous = false;
        rec.interimResults = false;

        rec.onresult = (e: Event) => {
            const r = e as unknown as { results: Array<{ 0: { transcript: string } }> };
            const text = r.results[0][0].transcript;
            (this.els['sourceText'] as HTMLTextAreaElement).value = text;
            this.voiceInputTriggered = true;
            this.onTextInput();
        };
        rec.onerror = () => this.stopSpeech();
        rec.onend = () => this.stopSpeech();
        this.recognition = rec;
    }

    private toggleSpeech(): void {
        if (!this.recognition) this.initSpeechRecognition();
        if (!this.recognition) return;
        this.speechActive ? this.stopSpeech() : this.startSpeech();
        this.haptic();
    }

    private startSpeech(): void {
        // Re-init to pick up latest source language
        this.initSpeechRecognition();
        if (!this.recognition) return;
        try {
            this.speechActive = true;
            this.updateSpeechUI(true);
            this.recognition.start();
        } catch { this.speechActive = false; }
    }

    private stopSpeech(): void {
        try { this.recognition?.stop(); } catch { /* ok */ }
        this.speechActive = false;
        this.updateSpeechUI(false);
    }

    private updateSpeechUI(active: boolean): void {
        const btn = this.els['toggleSpeech'];
        const status = this.els['speechStatus'];
        if (btn) {
            btn.classList.toggle('active', active);
            btn.setAttribute('aria-pressed', String(active));
        }
        if (status) {
            status.textContent = active ? '🎤 Ouvindo...' : '🎤 Reconhecimento: Desativado';
        }
    }

    // ─── Translation Engine ─────────────────────────────────

    private translating = false;

    private async translateText(): Promise<void> {
        const srcEl = this.els['sourceText'] as HTMLTextAreaElement;
        const tgtEl = this.els['targetText'] as HTMLTextAreaElement;
        const statusEl = this.els['translationStatus'];
        const src = srcEl?.value.trim();

        if (!src) {
            if (statusEl) statusEl.textContent = 'Nada para traduzir';
            if (tgtEl) tgtEl.value = '';
            this.updateConfidence(0);
            return;
        }

        if (this.translating) return;
        this.translating = true;

        // UI: shimmer state
        const outputArea = tgtEl?.closest('.output-area');
        outputArea?.classList.add('translating');
        if (statusEl) statusEl.textContent = 'Traduzindo...';
        const translateBtn = this.els['translateBtn'] as HTMLButtonElement;
        translateBtn?.setAttribute('disabled', 'true');
        translateBtn?.setAttribute('aria-busy', 'true');

        const started = performance.now();
        const sourceLang = this.selectedSource;
        const targetLang = this.selectedTarget;

        try {
            let translated = '';
            let confidence = 0;

            // Primary: MyMemory
            const mmUrl = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(src)}&langpair=${sourceLang}|${targetLang}`;
            const r0 = await fetch(mmUrl, { headers: { 'Accept': 'application/json' }, cache: 'no-store' }).catch(() => null);
            if (r0 && r0.ok) {
                const j0 = await r0.json() as {
                    responseData?: { translatedText?: string; match?: number };
                    matches?: Array<{ translation: string; match: number }>;
                };
                translated = j0.responseData?.translatedText || '';
                confidence = (j0.responseData?.match ?? 0) * 100;
            }

            // Fallback: LibreTranslate endpoints
            if (!translated) {
                const proxy = (location.hostname === 'localhost' || location.hostname === '127.0.0.1') ? 'http://localhost:3000/translate' : null;
                const endpoints = [proxy, 'https://translate.astian.org/translate', 'https://libretranslate.de/translate', 'https://libretranslate.com/translate', 'https://translate.argosopentech.com/translate'].filter(Boolean) as string[];
                for (const url of endpoints) {
                    const r = await fetch(url, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        referrerPolicy: 'no-referrer',
                        body: JSON.stringify({ q: src, source: sourceLang === targetLang ? 'auto' : sourceLang, target: targetLang, format: 'text' })
                    }).catch(() => null);
                    if (r && r.ok) {
                        const d = await r.json() as { translatedText?: string };
                        translated = d.translatedText || '';
                        if (translated) { confidence = 70; break; }
                    }
                }
            }

            translated = this.preserveCasing(src, translated || src);
            if (tgtEl) tgtEl.value = translated;
            if (statusEl) statusEl.textContent = 'Tradução concluída';

            this.updateConfidence(confidence);

            // Save to history & context memory
            const entry: TranslationEntry = {
                id: Date.now().toString(36),
                source: src,
                target: translated,
                sourceLang,
                targetLang,
                confidence,
                timestamp: Date.now(),
            };
            this.addToHistory(entry);
            this.addToContextMemory(entry);

            // Auto-speak after voice input
            if (this.voiceInputTriggered) {
                this.speakOutTranslation();
                this.voiceInputTriggered = false;
            }
        } catch {
            if (tgtEl) tgtEl.value = src;
            if (statusEl) statusEl.textContent = 'Falha na tradução';
        } finally {
            const ms = Math.round(performance.now() - started);
            const timeEl = this.els['translationTime'];
            if (timeEl) timeEl.textContent = `${ms} ms`;
            translateBtn?.removeAttribute('disabled');
            translateBtn?.setAttribute('aria-busy', 'false');
            outputArea?.classList.remove('translating');
            this.translating = false;
        }
    }

    // ─── Confidence Indicator ───────────────────────────────

    private updateConfidence(value: number): void {
        const bar = this.els['confidenceBar'] as HTMLElement;
        const text = this.els['confidenceText'] as HTMLElement;
        if (!bar || !text) return;

        const clamped = Math.max(0, Math.min(100, Math.round(value)));
        bar.style.width = `${clamped}%`;
        bar.className = 'confidence-fill';
        if (clamped >= 80) bar.classList.add('high');
        else if (clamped >= 50) bar.classList.add('medium');
        else bar.classList.add('low');

        text.textContent = clamped > 0 ? `${clamped}% confiança` : '';
    }

    // ─── Auto-detect Language ───────────────────────────────

    private lastDetectedLang = '';

    private tryDetectLanguage(text: string): void {
        const badge = this.els['detectedLangBadge'];
        if (text.length < 15) {
            if (badge) badge.style.display = 'none';
            return;
        }
        const result = detectLanguage(text);
        if (result && result.lang !== this.selectedSource && result.confidence > 40) {
            if (badge) {
                const langInfo = LANGUAGES[result.lang];
                badge.textContent = `${langInfo?.flag || ''} Detectado: ${langInfo?.label || result.lang} (${result.confidence}%)`;
                badge.style.display = 'inline-flex';
                badge.setAttribute('data-detected', result.lang);
                this.lastDetectedLang = result.lang;
            }
        } else {
            if (badge) badge.style.display = 'none';
            this.lastDetectedLang = '';
        }
    }

    // ─── Text Input Handler with Debounce ───────────────────

    private onTextInput(): void {
        const src = (this.els['sourceText'] as HTMLTextAreaElement)?.value || '';
        const count = this.els['charCount'];
        if (count) count.textContent = `${src.length} caracteres`;

        // Auto-detect
        this.tryDetectLanguage(src);

        if (this.autoTranslateEnabled) {
            this.debouncedTranslate();
        }
    }

    private debouncedTranslate(): void {
        if (this.debounceTimer) clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => this.translateText(), 300);
    }

    // ─── Smart Swap ─────────────────────────────────────────

    private swapLanguages(): void {
        const tmpLang = this.selectedSource;
        this.selectedSource = this.selectedTarget;
        this.selectedTarget = tmpLang;

        // Swap text content
        const srcEl = this.els['sourceText'] as HTMLTextAreaElement;
        const tgtEl = this.els['targetText'] as HTMLTextAreaElement;
        if (srcEl && tgtEl) {
            const tmpText = srcEl.value;
            srcEl.value = tgtEl.value;
            tgtEl.value = tmpText;
        }

        this.onSourceLangChange();
        this.onTargetLangChange();
        this.closeDropdowns();

        this.warmUpTargetVoice();
        this.haptic();

        // Auto-translate swapped text
        if (this.autoTranslateEnabled && srcEl?.value) {
            this.debouncedTranslate();
        }
    }

    // ─── Casing Preservation ────────────────────────────────

    private preserveCasing(src: string, dst: string): string {
        const hasLetter = /[A-Za-zÀ-ÖØ-öø-ÿ]/.test(src);
        if (!hasLetter) return dst;
        const letters = src.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ]/g, '');
        const isLower = letters.length > 0 && letters === letters.toLowerCase();
        const isUpper = letters.length > 0 && letters === letters.toUpperCase();
        if (isLower) return dst.toLowerCase();
        if (isUpper) return dst.toUpperCase();
        // Sentence-level casing preservation
        const srcSent = src.match(/[^.!?]+[.!?]*/g) || [src];
        const dstSent = dst.match(/[^.!?]+[.!?]*/g) || [dst];
        const n = Math.min(srcSent.length, dstSent.length);
        const adjusted: string[] = [];
        for (let i = 0; i < n; i++) {
            adjusted.push(this.adjustFirstAlpha(dstSent[i], this.isFirstAlphaUpper(srcSent[i])));
        }
        for (let i = n; i < dstSent.length; i++) adjusted.push(dstSent[i]);
        return adjusted.join('');
    }

    private isFirstAlphaUpper(text: string): boolean {
        for (const ch of Array.from(text)) {
            if (/[A-Za-zÀ-ÖØ-öø-ÿ]/.test(ch)) return ch === ch.toUpperCase();
        }
        return false;
    }

    private adjustFirstAlpha(text: string, upper: boolean): string {
        const arr = Array.from(text);
        for (let i = 0; i < arr.length; i++) {
            if (/[A-Za-zÀ-ÖØ-öø-ÿ]/.test(arr[i])) {
                arr[i] = upper ? arr[i].toUpperCase() : arr[i].toLowerCase();
                break;
            }
        }
        return arr.join('');
    }

    // ─── Actions ────────────────────────────────────────────

    private clearText(): void {
        const srcEl = this.els['sourceText'] as HTMLTextAreaElement;
        const tgtEl = this.els['targetText'] as HTMLTextAreaElement;
        if (srcEl) srcEl.value = '';
        if (tgtEl) tgtEl.value = '';
        this.updateConfidence(0);
        const badge = this.els['detectedLangBadge'];
        if (badge) badge.style.display = 'none';
        this.onTextInput();
        this.haptic();
    }

    private async copyTranslation(): Promise<void> {
        const txt = (this.els['targetText'] as HTMLTextAreaElement)?.value;
        if (!txt) return;
        try {
            await navigator.clipboard.writeText(txt);
            // Micro-animation feedback
            const btn = this.els['copyTranslation'];
            if (btn) {
                btn.classList.add('copied');
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-check';
                    setTimeout(() => { icon.className = 'fas fa-copy'; btn.classList.remove('copied'); }, 1500);
                }
            }
        } catch { /* clipboard denied */ }
        this.haptic();
    }

    private speakOutTranslation(): void {
        const txt = (this.els['targetText'] as HTMLTextAreaElement)?.value.trim();
        if (!txt) return;
        const btn = this.els['speakTranslation'];
        this.voiceEngine.speakText(
            txt,
            this.selectedTarget,
            () => btn?.classList.add('speaking'),
            () => btn?.classList.remove('speaking')
        );
        this.haptic();
    }

    // ─── History ────────────────────────────────────────────

    private addToHistory(entry: TranslationEntry): void {
        this.history.unshift(entry);
        if (this.history.length > this.MAX_HISTORY) this.history.pop();
        this.saveHistory();
        this.renderHistory();
    }

    private saveHistory(): void {
        try { localStorage.setItem('nt4_history', JSON.stringify(this.history)); } catch { /* full */ }
    }

    private loadHistory(): void {
        try {
            const raw = localStorage.getItem('nt4_history');
            if (raw) this.history = JSON.parse(raw);
        } catch { /* corrupt */ }
    }

    private clearHistory(): void {
        this.history = [];
        this.saveHistory();
        this.renderHistory();
        this.haptic();
    }

    private renderHistory(): void {
        const container = this.els['historyContainer'];
        if (!container) return;

        // Apply filter
        const filterEl = this.els['historyFilter'] as HTMLSelectElement;
        const filter = filterEl?.value || 'all';
        const filtered = filter === 'all'
            ? this.history
            : this.history.filter(h => `${h.sourceLang}-${h.targetLang}` === filter);

        if (filtered.length === 0) {
            container.innerHTML = '<p class="no-history">Nenhuma tradução realizada ainda.</p>';
            return;
        }

        container.innerHTML = filtered.map(entry => {
            const sLang = LANGUAGES[entry.sourceLang];
            const tLang = LANGUAGES[entry.targetLang];
            const time = new Date(entry.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
            return `
                <div class="history-card" data-id="${entry.id}">
                    <div class="history-card-header">
                        <span class="history-lang-badge">${sLang?.flag || ''} ${sLang?.label || entry.sourceLang} → ${tLang?.flag || ''} ${tLang?.label || entry.targetLang}</span>
                        <span class="history-time">${time}</span>
                    </div>
                    <div class="history-card-body">
                        <div class="history-source">${this.escapeHtml(entry.source.slice(0, 120))}</div>
                        <div class="history-arrow"><i class="fas fa-arrow-down"></i></div>
                        <div class="history-target">${this.escapeHtml(entry.target.slice(0, 120))}</div>
                    </div>
                    <div class="history-card-footer">
                        <button class="history-use-btn" onclick="window.neuroTranslator?.useHistoryEntry('${entry.id}')">
                            <i class="fas fa-redo"></i> Usar
                        </button>
                        <span class="history-confidence ${entry.confidence >= 80 ? 'high' : entry.confidence >= 50 ? 'medium' : 'low'}">${Math.round(entry.confidence)}%</span>
                    </div>
                </div>
            `;
        }).join('');
    }

    useHistoryEntry(id: string): void {
        const entry = this.history.find(h => h.id === id);
        if (!entry) return;
        this.selectedSource = entry.sourceLang;
        this.selectedTarget = entry.targetLang;
        (this.els['sourceText'] as HTMLTextAreaElement).value = entry.source;
        (this.els['targetText'] as HTMLTextAreaElement).value = entry.target;
        this.onSourceLangChange();
        this.onTargetLangChange();
        this.toggleDrawer(false);
    }

    private escapeHtml(text: string): string {
        const el = document.createElement('span');
        el.textContent = text;
        return el.innerHTML;
    }

    // ─── Context Memory ─────────────────────────────────────

    private addToContextMemory(entry: TranslationEntry): void {
        this.contextMemory.unshift(entry);
        if (this.contextMemory.length > this.MAX_CONTEXT) this.contextMemory.pop();
        try { sessionStorage.setItem('nt4_context', JSON.stringify(this.contextMemory)); } catch { /* ok */ }
    }

    private loadContextMemory(): void {
        try {
            const raw = sessionStorage.getItem('nt4_context');
            if (raw) this.contextMemory = JSON.parse(raw);
        } catch { /* ok */ }
    }

    // ─── History Drawer ─────────────────────────────────────

    private toggleDrawer(open: boolean): void {
        this.drawerOpen = open;
        const drawer = this.els['historyDrawer'];
        const overlay = this.els['historyDrawerOverlay'];
        if (drawer) drawer.classList.toggle('open', open);
        if (overlay) overlay.classList.toggle('open', open);
        document.body.classList.toggle('drawer-open', open);
        if (open) this.renderHistory();
        this.haptic();
    }

    // ─── Shortcuts Modal ────────────────────────────────────

    private toggleShortcutsModal(open: boolean): void {
        const modal = this.els['shortcutsModal'];
        if (modal) modal.classList.toggle('open', open);
    }

    // ─── Keyboard Shortcuts ─────────────────────────────────

    private handleKeyboard(e: KeyboardEvent): void {
        // Ctrl+Enter → translate
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            this.translateText();
            return;
        }
        // Ctrl+Shift+S → voice input
        if (e.ctrlKey && e.shiftKey && (e.key === 'S' || e.key === 's')) {
            e.preventDefault();
            this.toggleSpeech();
            return;
        }
        // Ctrl+D → swap
        if (e.ctrlKey && (e.key === 'D' || e.key === 'd')) {
            e.preventDefault();
            this.swapLanguages();
            return;
        }
        // Escape → close drawer/modal
        if (e.key === 'Escape') {
            this.closeDropdowns();
            if (this.drawerOpen) this.toggleDrawer(false);
            this.toggleShortcutsModal(false);
        }
    }

    // ─── Micro-interactions ─────────────────────────────────

    private haptic(): void {
        try { navigator.vibrate?.(10); } catch { /* unsupported */ }
    }
}

// ─── Bootstrap ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const app = new NeuroTranslatorWeb();
    (window as unknown as { neuroTranslator: NeuroTranslatorWeb }).neuroTranslator = app;

    // Service Worker
    if ('serviceWorker' in navigator) {
        const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        if (isLocal) {
            navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(reg => reg.unregister()));
        } else {
            navigator.serviceWorker.register('sw.js').catch(() => { /* ok */ });
        }
    }
});
