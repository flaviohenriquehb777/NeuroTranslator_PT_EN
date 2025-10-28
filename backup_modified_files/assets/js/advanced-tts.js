// NeuroTranslator Advanced Text-to-Speech Module
// Sistema avançado de síntese de voz com vozes adaptativas por gênero
// Implementa tecnologias de processamento de áudio e IA

class NeuroAdvancedTTS {
    constructor() {
        this.isInitialized = false;
        this.synthesis = null;
        this.voices = {
            available: [],
            male: [],
            female: [],
            neutral: [],
            current: null
        };
        
        this.settings = {
            rate: 0.9,
            pitch: 1.0,
            volume: 1.0,
            language: 'pt-BR',
            preferredGender: 'neutral',
            emotionalTone: 'neutral'
        };
        
        this.audioContext = null;
        this.audioAnalyzer = null;
        this.isPlaying = false;
        this.currentUtterance = null;
        
        // Configurações específicas por idioma e gênero
        this.voiceProfiles = {
            'pt-BR': {
                male: {
                    pitch: 0.8,
                    rate: 0.85,
                    preferredNames: ['Google português (Brasil)', 'Microsoft Daniel', 'Luciana'],
                    fallbackNames: ['pt-BR', 'portuguese', 'brasil']
                },
                female: {
                    pitch: 1.2,
                    rate: 0.9,
                    preferredNames: ['Google português (Brasil)', 'Microsoft Maria', 'Fernanda'],
                    fallbackNames: ['pt-BR', 'portuguese', 'brasil']
                }
            },
            'en-US': {
                male: {
                    pitch: 0.7,
                    rate: 0.9,
                    preferredNames: ['Google US English', 'Microsoft David', 'Alex'],
                    fallbackNames: ['en-US', 'english', 'american']
                },
                female: {
                    pitch: 1.1,
                    rate: 0.95,
                    preferredNames: ['Google US English', 'Microsoft Zira', 'Samantha'],
                    fallbackNames: ['en-US', 'english', 'american']
                }
            }
        };
        
        this.emotionalProfiles = {
            neutral: { pitchModifier: 0, rateModifier: 0, volumeModifier: 0 },
            happy: { pitchModifier: 0.2, rateModifier: 0.1, volumeModifier: 0.1 },
            sad: { pitchModifier: -0.2, rateModifier: -0.1, volumeModifier: -0.1 },
            excited: { pitchModifier: 0.3, rateModifier: 0.2, volumeModifier: 0.2 },
            calm: { pitchModifier: -0.1, rateModifier: -0.05, volumeModifier: -0.05 }
        };
        
        this.speakingQueue = [];
        this.isProcessingQueue = false;
        
        this.init();
    }
    
    async init() {
        console.log('🔊 Inicializando NeuroAdvancedTTS...');
        
        try {
            await this.initSpeechSynthesis();
            await this.loadVoices();
            await this.initAudioContext();
            await this.setupVoiceAnalysis();
            
            this.isInitialized = true;
            console.log('✅ NeuroAdvancedTTS inicializado com sucesso!');
            
            // Notificar inicialização
            this.dispatchEvent('tts-initialized', { 
                voicesCount: this.voices.available.length,
                maleVoices: this.voices.male.length,
                femaleVoices: this.voices.female.length
            });
            
        } catch (error) {
            console.error('❌ Erro ao inicializar TTS:', error);
        }
    }
    
    async initSpeechSynthesis() {
        if (!('speechSynthesis' in window)) {
            throw new Error('Speech Synthesis não suportada');
        }
        
        this.synthesis = window.speechSynthesis;
        
        // Aguardar carregamento das vozes
        return new Promise((resolve) => {
            if (this.synthesis.getVoices().length > 0) {
                resolve();
            } else {
                this.synthesis.addEventListener('voiceschanged', resolve, { once: true });
            }
        });
    }
    
    async loadVoices() {
        console.log('🎤 Carregando vozes disponíveis...');
        
        this.voices.available = this.synthesis.getVoices();
        
        // Classificar vozes por gênero e idioma
        this.voices.available.forEach(voice => {
            const voiceName = voice.name.toLowerCase();
            const voiceLang = voice.lang.toLowerCase();
            
            // Classificação por gênero baseada no nome
            if (this.isMaleVoice(voiceName)) {
                this.voices.male.push(voice);
            } else if (this.isFemaleVoice(voiceName)) {
                this.voices.female.push(voice);
            } else {
                this.voices.neutral.push(voice);
            }
        });
        
        console.log(`✅ Vozes carregadas: ${this.voices.available.length} total`);
        console.log(`   👨 Masculinas: ${this.voices.male.length}`);
        console.log(`   👩 Femininas: ${this.voices.female.length}`);
        console.log(`   ⚪ Neutras: ${this.voices.neutral.length}`);
    }
    
    isMaleVoice(voiceName) {
        const maleIndicators = [
            'male', 'man', 'masculine', 'masculino', 'homem',
            'david', 'daniel', 'alex', 'mark', 'paul', 'john',
            'carlos', 'joão', 'pedro', 'antonio', 'ricardo'
        ];
        
        return maleIndicators.some(indicator => voiceName.includes(indicator));
    }
    
    isFemaleVoice(voiceName) {
        const femaleIndicators = [
            'female', 'woman', 'feminine', 'feminina', 'mulher',
            'maria', 'ana', 'samantha', 'zira', 'susan', 'karen',
            'fernanda', 'luciana', 'patricia', 'sandra', 'monica'
        ];
        
        return femaleIndicators.some(indicator => voiceName.includes(indicator));
    }
    
    async initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.audioAnalyzer = this.audioContext.createAnalyser();
            this.audioAnalyzer.fftSize = 256;
            
            console.log('✅ Contexto de áudio inicializado');
        } catch (error) {
            console.warn('⚠️ Contexto de áudio não disponível:', error);
        }
    }
    
    async setupVoiceAnalysis() {
        // Configurar análise de voz em tempo real
        console.log('📊 Configurando análise de voz...');
        
        // Implementar análise de frequência e tom
        this.voiceAnalysisData = {
            frequency: 0,
            amplitude: 0,
            pitch: 0,
            isActive: false
        };
    }
    
    // Método principal para falar texto
    async speak(text, options = {}) {
        if (!this.isInitialized) {
            console.warn('⚠️ TTS não inicializado');
            return;
        }
        
        if (!text || text.trim().length === 0) {
            console.warn('⚠️ Texto vazio para síntese');
            return;
        }
        
        const speakOptions = {
            language: options.language || this.settings.language,
            gender: options.gender || this.settings.preferredGender,
            emotion: options.emotion || this.settings.emotionalTone,
            rate: options.rate || this.settings.rate,
            pitch: options.pitch || this.settings.pitch,
            volume: options.volume || this.settings.volume,
            priority: options.priority || 'normal'
        };
        
        console.log(`🔊 Falando: "${text.substring(0, 50)}..." (${speakOptions.gender}, ${speakOptions.language})`);
        
        // Adicionar à fila se necessário
        if (this.isPlaying && speakOptions.priority !== 'high') {
            this.addToQueue(text, speakOptions);
            return;
        }
        
        // Parar fala atual se prioridade alta
        if (speakOptions.priority === 'high') {
            this.stop();
        }
        
        return this.performSpeech(text, speakOptions);
    }
    
    async performSpeech(text, options) {
        return new Promise((resolve, reject) => {
            try {
                // Selecionar voz apropriada
                const selectedVoice = this.selectBestVoice(options.language, options.gender);
                
                if (!selectedVoice) {
                    console.warn('⚠️ Nenhuma voz adequada encontrada');
                    reject(new Error('Voz não encontrada'));
                    return;
                }
                
                // Criar utterance
                const utterance = new SpeechSynthesisUtterance(text);
                this.currentUtterance = utterance;
                
                // Configurar voz
                utterance.voice = selectedVoice;
                utterance.lang = options.language;
                
                // Aplicar configurações de gênero
                const genderProfile = this.voiceProfiles[options.language]?.[options.gender];
                if (genderProfile) {
                    utterance.pitch = genderProfile.pitch;
                    utterance.rate = genderProfile.rate;
                } else {
                    utterance.pitch = options.pitch;
                    utterance.rate = options.rate;
                }
                
                // Aplicar modificações emocionais
                const emotionalProfile = this.emotionalProfiles[options.emotion];
                if (emotionalProfile) {
                    utterance.pitch += emotionalProfile.pitchModifier;
                    utterance.rate += emotionalProfile.rateModifier;
                    utterance.volume = Math.max(0, Math.min(1, options.volume + emotionalProfile.volumeModifier));
                } else {
                    utterance.volume = options.volume;
                }
                
                // Normalizar valores
                utterance.pitch = Math.max(0, Math.min(2, utterance.pitch));
                utterance.rate = Math.max(0.1, Math.min(10, utterance.rate));
                
                // Event listeners
                utterance.onstart = () => {
                    this.isPlaying = true;
                    console.log('🎤 Iniciando síntese de voz');
                    this.dispatchEvent('tts-start', { text, options });
                };
                
                utterance.onend = () => {
                    this.isPlaying = false;
                    this.currentUtterance = null;
                    console.log('✅ Síntese de voz finalizada');
                    this.dispatchEvent('tts-end', { text, options });
                    this.processQueue();
                    resolve();
                };
                
                utterance.onerror = (event) => {
                    this.isPlaying = false;
                    this.currentUtterance = null;
                    console.error('❌ Erro na síntese:', event.error);
                    this.dispatchEvent('tts-error', { error: event.error, text, options });
                    reject(new Error(event.error));
                };
                
                utterance.onpause = () => {
                    console.log('⏸️ Síntese pausada');
                    this.dispatchEvent('tts-pause', { text, options });
                };
                
                utterance.onresume = () => {
                    console.log('▶️ Síntese retomada');
                    this.dispatchEvent('tts-resume', { text, options });
                };
                
                // Iniciar síntese
                this.synthesis.speak(utterance);
                
            } catch (error) {
                console.error('❌ Erro ao criar síntese:', error);
                reject(error);
            }
        });
    }
    
    selectBestVoice(language, gender) {
        console.log(`🔍 Selecionando melhor voz: ${language}, ${gender}`);
        
        // Obter perfil de voz para idioma e gênero
        const profile = this.voiceProfiles[language]?.[gender];
        
        if (!profile) {
            console.warn(`⚠️ Perfil não encontrado para ${language}/${gender}`);
            return this.voices.available[0]; // Fallback para primeira voz disponível
        }
        
        // Procurar por vozes preferenciais
        for (const preferredName of profile.preferredNames) {
            const voice = this.voices.available.find(v => 
                v.name.toLowerCase().includes(preferredName.toLowerCase()) &&
                v.lang.toLowerCase().includes(language.toLowerCase())
            );
            if (voice) {
                console.log(`✅ Voz selecionada: ${voice.name}`);
                return voice;
            }
        }
        
        // Procurar por vozes do gênero correto
        const genderVoices = gender === 'male' ? this.voices.male : 
                           gender === 'female' ? this.voices.female : 
                           this.voices.neutral;
        
        const languageGenderVoice = genderVoices.find(v => 
            v.lang.toLowerCase().includes(language.toLowerCase())
        );
        
        if (languageGenderVoice) {
            console.log(`✅ Voz de gênero selecionada: ${languageGenderVoice.name}`);
            return languageGenderVoice;
        }
        
        // Fallback para qualquer voz do idioma
        const languageVoice = this.voices.available.find(v => 
            v.lang.toLowerCase().includes(language.toLowerCase())
        );
        
        if (languageVoice) {
            console.log(`✅ Voz de idioma selecionada: ${languageVoice.name}`);
            return languageVoice;
        }
        
        // Último fallback
        console.warn('⚠️ Usando voz padrão');
        return this.voices.available[0];
    }
    
    // Sistema de fila para múltiplas falas
    addToQueue(text, options) {
        this.speakingQueue.push({ text, options });
        console.log(`📋 Adicionado à fila: ${this.speakingQueue.length} itens`);
    }
    
    async processQueue() {
        if (this.isProcessingQueue || this.speakingQueue.length === 0) {
            return;
        }
        
        this.isProcessingQueue = true;
        
        while (this.speakingQueue.length > 0) {
            const { text, options } = this.speakingQueue.shift();
            
            try {
                await this.performSpeech(text, options);
            } catch (error) {
                console.error('❌ Erro ao processar fila:', error);
            }
        }
        
        this.isProcessingQueue = false;
    }
    
    // Controles de reprodução
    stop() {
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
            this.isPlaying = false;
            this.currentUtterance = null;
            console.log('🛑 Síntese interrompida');
        }
        
        // Limpar fila
        this.speakingQueue = [];
    }
    
    pause() {
        if (this.synthesis.speaking) {
            this.synthesis.pause();
            console.log('⏸️ Síntese pausada');
        }
    }
    
    resume() {
        if (this.synthesis.paused) {
            this.synthesis.resume();
            console.log('▶️ Síntese retomada');
        }
    }
    
    // Configurações dinâmicas
    setGender(gender) {
        this.settings.preferredGender = gender;
        console.log(`👤 Gênero definido: ${gender}`);
    }
    
    setLanguage(language) {
        this.settings.language = language;
        console.log(`🌍 Idioma definido: ${language}`);
    }
    
    setEmotion(emotion) {
        this.settings.emotionalTone = emotion;
        console.log(`😊 Tom emocional definido: ${emotion}`);
    }
    
    setRate(rate) {
        this.settings.rate = Math.max(0.1, Math.min(10, rate));
        console.log(`⚡ Velocidade definida: ${this.settings.rate}`);
    }
    
    setPitch(pitch) {
        this.settings.pitch = Math.max(0, Math.min(2, pitch));
        console.log(`🎵 Tom definido: ${this.settings.pitch}`);
    }
    
    setVolume(volume) {
        this.settings.volume = Math.max(0, Math.min(1, volume));
        console.log(`🔊 Volume definido: ${this.settings.volume}`);
    }
    
    // Métodos de análise
    getAvailableVoices() {
        return {
            total: this.voices.available.length,
            male: this.voices.male.map(v => ({ name: v.name, lang: v.lang })),
            female: this.voices.female.map(v => ({ name: v.name, lang: v.lang })),
            neutral: this.voices.neutral.map(v => ({ name: v.name, lang: v.lang }))
        };
    }
    
    getCurrentSettings() {
        return { ...this.settings };
    }
    
    getQueueStatus() {
        return {
            isPlaying: this.isPlaying,
            queueLength: this.speakingQueue.length,
            isProcessingQueue: this.isProcessingQueue,
            currentText: this.currentUtterance?.text?.substring(0, 50) || null
        };
    }
    
    // Método para testar voz
    async testVoice(gender, language = 'pt-BR') {
        const testTexts = {
            'pt-BR': 'Olá, esta é uma demonstração da síntese de voz do NeuroTranslator.',
            'en-US': 'Hello, this is a demonstration of NeuroTranslator voice synthesis.'
        };
        
        const testText = testTexts[language] || testTexts['pt-BR'];
        
        await this.speak(testText, {
            gender: gender,
            language: language,
            priority: 'high'
        });
    }
    
    // Método para síntese com análise de sentimento
    async speakWithSentiment(text, detectedSentiment, options = {}) {
        const emotionMap = {
            'positive': 'happy',
            'negative': 'sad',
            'neutral': 'neutral',
            'excited': 'excited',
            'calm': 'calm'
        };
        
        const emotion = emotionMap[detectedSentiment] || 'neutral';
        
        return this.speak(text, {
            ...options,
            emotion: emotion
        });
    }
    
    dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
    }
}

// Exportar para uso global
window.NeuroAdvancedTTS = NeuroAdvancedTTS;

console.log('🔊 Módulo NeuroAdvancedTTS carregado!');