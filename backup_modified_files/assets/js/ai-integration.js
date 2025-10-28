// NeuroTranslator AI Integration Module
// Sistema central de integração de todos os módulos de IA
// Coordena voz, visão, avatares e tradução inteligente

class NeuroAIIntegration {
    constructor() {
        this.isInitialized = false;
        this.isActive = false;
        
        // Módulos de IA
        this.modules = {
            voiceVision: null,
            languageDetector: null,
            advancedTTS: null,
            genderDetection: null
        };
        
        // Estado global do sistema
        this.state = {
            currentLanguage: 'pt-BR',
            detectedGender: 'neutral',
            isListening: false,
            isSpeaking: false,
            isTranslating: false,
            confidence: {
                language: 0,
                gender: 0,
                voice: 0
            }
        };
        
        // Configurações de integração
        this.config = {
            autoDetectGender: true,
            autoSwitchLanguage: true,
            voiceActivationCommand: 'neuro traduza',
            genderDetectionInterval: 2000,
            confidenceThreshold: 0.7,
            maxRetries: 3,
            debugMode: false
        };
        
        // Filas de processamento
        this.processingQueue = {
            translation: [],
            speech: [],
            detection: []
        };
        
        // Callbacks e eventos
        this.eventHandlers = new Map();
        
        // Métricas de performance
        this.metrics = {
            translationsCount: 0,
            speechSynthesisCount: 0,
            genderDetectionsCount: 0,
            averageResponseTime: 0,
            errorCount: 0,
            successRate: 0
        };
        
        this.init();
    }
    
    async init() {
        console.log('🤖 Inicializando NeuroAI Integration...');
        
        try {
            await this.initializeModules();
            await this.setupEventListeners();
            await this.configureIntegration();
            await this.startAIServices();
            
            this.isInitialized = true;
            console.log('✅ NeuroAI Integration inicializado com sucesso!');
            
            this.dispatchEvent('ai-integration-ready', {
                modules: Object.keys(this.modules).length,
                state: this.state
            });
            
        } catch (error) {
            console.error('❌ Erro ao inicializar integração de IA:', error);
            this.handleInitializationError(error);
        }
    }
    
    async initializeModules() {
        console.log('📦 Inicializando módulos de IA...');
        
        // Inicializar módulos em ordem de dependência
        const initPromises = [];
        
        // 1. Detecção de idioma (independente)
        if (window.NeuroLanguageDetector) {
            initPromises.push(this.initModule('languageDetector', NeuroLanguageDetector));
        }
        
        // 2. TTS avançado (independente)
        if (window.NeuroAdvancedTTS) {
            initPromises.push(this.initModule('advancedTTS', NeuroAdvancedTTS));
        }
        
        // 3. Detecção de gênero (independente)
        if (window.NeuroGenderDetection) {
            initPromises.push(this.initModule('genderDetection', NeuroGenderDetection));
        }
        
        // Aguardar módulos independentes
        await Promise.all(initPromises);
        
        // 4. Sistema de avatares (depende de outros módulos)

        // 5. Voz e visão (integra com outros módulos)
        if (window.NeuroAIVoiceVision) {
            await this.initModule('voiceVision', NeuroAIVoiceVision);
        }
        
        console.log('✅ Módulos inicializados:', Object.keys(this.modules).filter(key => this.modules[key]));
    }
    
    async initModule(name, ModuleClass) {
        try {
            console.log(`🔧 Inicializando ${name}...`);
            this.modules[name] = new ModuleClass();
            
            // Aguardar inicialização se necessário
            if (this.modules[name].init && typeof this.modules[name].init === 'function') {
                await this.modules[name].init();
            }
            
            console.log(`✅ ${name} inicializado`);
            
        } catch (error) {
            console.error(`❌ Erro ao inicializar ${name}:`, error);
            this.modules[name] = null;
        }
    }
    
    async setupEventListeners() {
        console.log('🎧 Configurando event listeners integrados...');
        
        // Eventos de reconhecimento de voz
        document.addEventListener('voice-command-detected', (event) => {
            this.handleVoiceCommand(event.detail);
        });
        
        // Eventos de detecção de gênero
        document.addEventListener('gender-detected', (event) => {
            this.handleGenderDetection(event.detail);
        });
        
        // Eventos de detecção de idioma
        document.addEventListener('language-detected', (event) => {
            this.handleLanguageDetection(event.detail);
        });
        
        // Eventos de TTS
        document.addEventListener('tts-start', (event) => {
            this.handleTTSStart(event.detail);
        });
        
        document.addEventListener('tts-end', (event) => {
            this.handleTTSEnd(event.detail);
        });
        
        // Eventos de avatar

        // Eventos de tradução (do sistema principal)
        document.addEventListener('translation-complete', (event) => {
            this.handleTranslationComplete(event.detail);
        });
        
        console.log('✅ Event listeners configurados');
    }
    
    async configureIntegration() {
        console.log('⚙️ Configurando integração entre módulos...');
        
        // Configurar detecção automática de gênero
        if (this.config.autoDetectGender && this.modules.genderDetection) {
            this.startGenderDetection();
        }
        
        // Configurar ativação por voz
        if (this.modules.voiceVision) {
            this.setupVoiceActivation();
        }
        
        // Configurar sincronização de avatar

    // Manipuladores de eventos
    handleVoiceCommand(detail) {
        console.log('🎤 Comando de voz detectado:', detail);
        
        const { command, text, confidence } = detail;
        
        if (command === 'translate' && confidence > this.config.confidenceThreshold) {
            this.processVoiceTranslation(text);
        }
        
        this.updateMetrics('voice', confidence);
    }
    
    handleGenderDetection(detail) {
        const { smoothed } = detail;
        
        if (smoothed.confidence > this.config.confidenceThreshold) {
            console.log(`👤 Gênero detectado: ${smoothed.gender} (${(smoothed.confidence * 100).toFixed(1)}%)`);
            
            this.state.detectedGender = smoothed.gender;
            this.state.confidence.gender = smoothed.confidence;
            
            // Atualizar avatar se ativo

            // Configurar TTS para o gênero detectado
            if (this.modules.advancedTTS) {
                this.modules.advancedTTS.setGender(smoothed.gender);
            }
            
            this.updateMetrics('gender', smoothed.confidence);
            
            this.dispatchEvent('ai-gender-updated', {
                gender: smoothed.gender,
                confidence: smoothed.confidence
            });
        }
    }
    
    handleLanguageDetection(detail) {
        const { language, confidence } = detail;
        
        if (confidence > this.config.confidenceThreshold && this.config.autoSwitchLanguage) {
            console.log(`🌍 Idioma detectado: ${language} (${(confidence * 100).toFixed(1)}%)`);
            
            this.state.currentLanguage = language;
            this.state.confidence.language = confidence;
            
            // Atualizar TTS para o idioma detectado
            if (this.modules.advancedTTS) {
                this.modules.advancedTTS.setLanguage(language);
            }
            
            this.updateMetrics('language', confidence);
            
            this.dispatchEvent('ai-language-updated', {
                language: language,
                confidence: confidence
            });
        }
    }
    
    handleTTSStart(detail) {
        console.log('🔊 TTS iniciado');
        this.state.isSpeaking = true;
        
        // Ativar avatar se disponível

        this.dispatchEvent('ai-speaking-start', detail);
    }
    
    handleTTSEnd(detail) {
        console.log('🔇 TTS finalizado');
        this.state.isSpeaking = false;
        
        // Desativar avatar

        this.updateMetrics('speech');
        
        this.dispatchEvent('ai-speaking-end', detail);
    }

    }
    
    handleTranslationComplete(detail) {
        console.log('🔄 Tradução completa:', detail);
        
        const { originalText, translatedText, sourceLang, targetLang } = detail;
        
        // Processar com TTS se configurado
        if (this.modules.advancedTTS && translatedText) {
            this.speakTranslation(translatedText, targetLang);
        }
        
        this.updateMetrics('translation');
        
        this.dispatchEvent('ai-translation-processed', detail);
    }
    
    // Métodos principais de integração
    async processVoiceTranslation(text) {
        console.log('🎯 Processando tradução por voz:', text);
        
        this.state.isTranslating = true;
        
        try {
            // 1. Detectar idioma do texto
            let sourceLang = this.state.currentLanguage;
            
            if (this.modules.languageDetector) {
                const detection = await this.modules.languageDetector.detectLanguage(text);
                if (detection.confidence > this.config.confidenceThreshold) {
                    sourceLang = detection.language;
                }
            }
            
            // 2. Determinar idioma de destino
            const targetLang = sourceLang === 'pt-BR' ? 'en-US' : 'pt-BR';
            
            // 3. Realizar tradução (integrar com sistema principal)
            const translationResult = await this.performTranslation(text, sourceLang, targetLang);
            
            // 4. Falar resultado
            if (translationResult && this.modules.advancedTTS) {
                await this.speakTranslation(translationResult.text, targetLang);
            }
            
            this.state.isTranslating = false;
            
            return translationResult;
            
        } catch (error) {
            console.error('❌ Erro na tradução por voz:', error);
            this.state.isTranslating = false;
            this.updateMetrics('error');
            throw error;
        }
    }
    
    async performTranslation(text, sourceLang, targetLang) {
        // Integrar com o sistema de tradução principal
        // Este método deve ser conectado ao NeuroTranslatorWeb existente
        
        console.log(`🔄 Traduzindo: "${text}" (${sourceLang} → ${targetLang})`);
        
        // Simular tradução por enquanto - deve ser substituído pela integração real
        const mockTranslation = {
            text: `[Tradução de: ${text}]`,
            sourceLang: sourceLang,
            targetLang: targetLang,
            confidence: 0.95
        };
        
        return mockTranslation;
    }
    
    async speakTranslation(text, language) {
        if (!this.modules.advancedTTS) {
            console.warn('⚠️ TTS não disponível');
            return;
        }
        
        console.log(`🗣️ Falando tradução: "${text}" (${language})`);
        
        const speakOptions = {
            language: language,
            gender: this.state.detectedGender,
            priority: 'high'
        };
        
        await this.modules.advancedTTS.speak(text, speakOptions);
    }
    
    // Controles do sistema

        console.log('🎭 Ativando avatar');

        // Definir gênero atual
        if (this.state.detectedGender !== 'neutral') {}
        
        this.dispatchEvent('ai-avatar-activated');
    }
    
    deactivateAvatar() {
        console.log('🎭 Desativando avatar');
        
        this.dispatchEvent('ai-avatar-deactivated');
    }
    
    startGenderDetection() {
        if (!this.modules.genderDetection) {
            console.warn('⚠️ Detecção de gênero não disponível');
            return;
        }
        
        console.log('👁️ Iniciando detecção de gênero');
        
        this.modules.genderDetection.startDetection({
            onGenderDetected: (result) => {
                this.handleGenderDetection({ smoothed: result });
            }
        });
    }
    
    stopGenderDetection() {
        if (this.modules.genderDetection) {
            this.modules.genderDetection.stopDetection();
        }
    }
    
    startContinuousDetection() {
        console.log('🔄 Iniciando detecção contínua');
        
        // Iniciar detecção de gênero
        this.startGenderDetection();
        
        // Configurar intervalos de detecção
        setInterval(() => {
            if (this.isActive && !this.state.isSpeaking) {
                // Executar detecções periódicas
                this.performPeriodicDetections();
            }
        }, this.config.genderDetectionInterval);
    }
    
    async performPeriodicDetections() {
        // Executar detecções em background quando não estiver falando
        if (this.modules.genderDetection && !this.state.isSpeaking) {
            // A detecção já está rodando continuamente
        }
    }
    
    setupVoiceActivation() {
        console.log('🎤 Configurando ativação por voz');
        
        if (this.modules.voiceVision) {
            // Configurar comando de ativação
            this.modules.voiceVision.setActivationCommand(this.config.voiceActivationCommand);
        }
    }

    }
    
    // Métodos de configuração
    setConfig(key, value) {
        if (this.config.hasOwnProperty(key)) {
            this.config[key] = value;
            console.log(`⚙️ Configuração atualizada: ${key} = ${value}`);
            
            this.dispatchEvent('ai-config-updated', { key, value });
        }
    }
    
    getConfig(key) {
        return key ? this.config[key] : { ...this.config };
    }
    
    // Métodos de análise
    getState() {
        return { ...this.state };
    }
    
    getMetrics() {
        // Calcular taxa de sucesso
        const totalOperations = this.metrics.translationsCount + 
                               this.metrics.speechSynthesisCount + 
                               this.metrics.genderDetectionsCount;
        
        this.metrics.successRate = totalOperations > 0 ? 
            ((totalOperations - this.metrics.errorCount) / totalOperations) * 100 : 0;
        
        return { ...this.metrics };
    }
    
    getModuleStatus() {
        const status = {};
        
        Object.keys(this.modules).forEach(key => {
            status[key] = {
                loaded: !!this.modules[key],
                initialized: this.modules[key] && this.modules[key].isInitialized !== false
            };
        });
        
        return status;
    }
    
    updateMetrics(type, confidence = 1) {
        switch (type) {
            case 'translation':
                this.metrics.translationsCount++;
                break;
            case 'speech':
                this.metrics.speechSynthesisCount++;
                break;
            case 'gender':
                this.metrics.genderDetectionsCount++;
                break;
            case 'voice':
                // Atualizar confiança de voz
                this.state.confidence.voice = confidence;
                break;
            case 'language':
                // Atualizar confiança de idioma
                this.state.confidence.language = confidence;
                break;
            case 'error':
                this.metrics.errorCount++;
                break;
        }
    }
    
    // Métodos de teste
    async testIntegration() {
        console.log('🧪 Testando integração de IA...');
        
        const results = {
            modules: this.getModuleStatus(),
            state: this.getState(),
            metrics: this.getMetrics()
        };
        
        // Testar cada módulo
        if (this.modules.advancedTTS) {
            try {
                await this.modules.advancedTTS.testVoice('female', 'pt-BR');
                results.ttsTest = 'success';
            } catch (error) {
                results.ttsTest = 'failed';
            }
        }
        
        if (this.modules.genderDetection) {
            results.genderDetectionTest = this.modules.genderDetection.isInitialized ? 'success' : 'failed';
        }

        console.log('🧪 Resultados do teste:', results);
        
        this.dispatchEvent('ai-integration-test-complete', results);
        
        return results;
    }
    
    // Tratamento de erros
    handleInitializationError(error) {
        console.error('❌ Erro na inicialização:', error);
        
        this.dispatchEvent('ai-integration-error', {
            type: 'initialization',
            error: error.message,
            timestamp: Date.now()
        });
    }
    
    // Limpeza
    cleanup() {
        console.log('🧹 Limpando integração de IA...');
        
        this.isActive = false;
        
        // Limpar módulos
        Object.values(this.modules).forEach(module => {
            if (module && module.cleanup) {
                module.cleanup();
            }
        });
        
        // Limpar event listeners
        this.eventHandlers.clear();
        
        console.log('✅ Limpeza concluída');
    }
    
    dispatchEvent(eventName, data = {}) {
        const event = new CustomEvent(eventName, { 
            detail: { 
                ...data, 
                timestamp: Date.now(),
                source: 'NeuroAIIntegration'
            } 
        });
        document.dispatchEvent(event);
        
        if (this.config.debugMode) {
            console.log(`📡 Evento disparado: ${eventName}`, data);
        }
    }
}

// Exportar para uso global
window.NeuroAIIntegration = NeuroAIIntegration;

// Auto-inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('🤖 Inicializando NeuroAI Integration automaticamente...');
    window.neuroAI = new NeuroAIIntegration();
});

console.log('🤖 Módulo NeuroAI Integration carregado!');