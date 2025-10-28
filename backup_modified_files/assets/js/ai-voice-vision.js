// NeuroTranslator AI Voice & Vision Module
// Módulo avançado de IA para reconhecimento de voz, detecção de gênero e avatares 3D
// Desenvolvido com tecnologias de Machine Learning e Computer Vision

class NeuroAIVoiceVision {
    constructor() {
        this.isInitialized = false;
        this.models = {
            faceApi: null,
            genderDetection: null,
            voiceAnalysis: null
        };
        
        // Configuração inicial dos sistemas
        this.setupInitialSystems();
    }
    
    setupInitialSystems() {
        // Configuração dos sistemas será feita aqui
    }
    
    // Correção do reconhecimento de voz
    initVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('⚠️ Reconhecimento de voz não suportado');
            return false;
        }

        try {
            // Limpar instância anterior se existir
            if (this.recognition) {
                this.recognition.abort();
                this.recognition = null;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            // Configurações otimizadas
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = this.currentLanguage || 'pt-BR';
            this.recognition.maxAlternatives = 1;
            
            // Estado de controle
            this.isRecognitionActive = false;
            this.recognitionTimeout = null;
            
            // Event listeners com tratamento de erro
            this.recognition.onstart = () => {
                console.log('🎤 Reconhecimento iniciado');
                this.isRecognitionActive = true;
                this.updateVoiceStatus('listening');
            };
            
            this.recognition.onresult = (event) => {
                try {
                    const result = event.results[0][0];
                    const transcript = result.transcript.trim();
                    const confidence = result.confidence;
                    
                    console.log(`🗣️ Reconhecido: "${transcript}" (${Math.round(confidence * 100)}%)`);
                    
                    if (confidence > 0.5) {
                        this.processVoiceCommand(transcript);
                    }
                } catch (error) {
                    console.error('❌ Erro ao processar resultado:', error);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('❌ Erro no reconhecimento:', event.error);
                this.isRecognitionActive = false;
                this.updateVoiceStatus('error');
                
                // Tratamento específico de erros
                switch (event.error) {
                    case 'aborted':
                        console.log('🔄 Reconhecimento abortado - reiniciando...');
                        setTimeout(() => this.startVoiceRecognition(), 1000);
                        break;
                    case 'network':
                        console.log('🌐 Erro de rede - tentando novamente...');
                        setTimeout(() => this.startVoiceRecognition(), 2000);
                        break;
                    case 'not-allowed':
                        console.error('🚫 Permissão de microfone negada');
                        this.updateVoiceStatus('permission-denied');
                        break;
                    default:
                        setTimeout(() => this.startVoiceRecognition(), 1500);
                }
            };
            
            this.recognition.onend = () => {
                console.log('🔇 Reconhecimento finalizado');
                this.isRecognitionActive = false;
                this.updateVoiceStatus('idle');
                
                // Reiniciar automaticamente se não foi abortado intencionalmente
                if (this.shouldKeepListening) {
                    setTimeout(() => this.startVoiceRecognition(), 500);
                }
            };
            
            return true;
            
        } catch (error) {
            console.error('❌ Erro ao inicializar reconhecimento:', error);
            return false;
        }
    }

    startVoiceRecognition() {
        try {
            // Verificar se já está ativo
            if (this.isRecognitionActive) {
                console.log('⚠️ Reconhecimento já ativo');
                return;
            }
            
            // Verificar se existe instância
            if (!this.recognition) {
                if (!this.initVoiceRecognition()) {
                    return;
                }
            }
            
            // Limpar timeout anterior
            if (this.recognitionTimeout) {
                clearTimeout(this.recognitionTimeout);
            }
            
            // Iniciar com timeout de segurança
            this.recognitionTimeout = setTimeout(() => {
                if (this.isRecognitionActive) {
                    console.log('⏰ Timeout do reconhecimento - reiniciando');
                    this.stopVoiceRecognition();
                    setTimeout(() => this.startVoiceRecognition(), 1000);
                }
            }, 10000);
            
            this.recognition.start();
            
        } catch (error) {
            console.error('❌ Erro ao iniciar reconhecimento:', error);
            this.isRecognitionActive = false;
            
            // Tentar reinicializar
            setTimeout(() => {
                this.initVoiceRecognition();
                this.startVoiceRecognition();
            }, 2000);
        }
    }

    stopVoiceRecognition() {
        try {
            if (this.recognition && this.isRecognitionActive) {
                this.shouldKeepListening = false;
                this.recognition.abort();
            }
            
            if (this.recognitionTimeout) {
                clearTimeout(this.recognitionTimeout);
                this.recognitionTimeout = null;
            }
            
            this.isRecognitionActive = false;
            
        } catch (error) {
            console.error('❌ Erro ao parar reconhecimento:', error);
        }
    }

    updateVoiceStatus(status) {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = this.getStatusText(status);
            statusElement.className = `voice-status ${status}`;
        }
    }

    getStatusText(status) {
        const statusTexts = {
            'idle': '🎤 Pronto para ouvir',
            'listening': '🔴 Ouvindo...',
            'processing': '⚙️ Processando...',
            'error': '❌ Erro no reconhecimento',
            'permission-denied': '🚫 Permissão negada'
        };
        return statusTexts[status] || '🎤 Status desconhecido';
    }

    processVoiceCommand(transcript) {
        const command = transcript.toLowerCase();
        
        // Verificar comando de ativação
        if (command.includes('neuro traduza') || command.includes('neuro translate')) {
            console.log('🚀 Comando de ativação detectado');
            this.activateTranslation();
        } else {
            // Processar como texto para tradução
            this.processTranslation(transcript);
        }
    }

    activateTranslation() {
        // Ativar modo de tradução
        this.shouldKeepListening = true;
        this.updateVoiceStatus('listening');
        
        // Feedback visual
        const button = document.getElementById('voice-btn');
        if (button) {
            button.classList.add('active');
        }
    }

    processTranslation(text) {
        // Processar tradução do texto
        const originalTextArea = document.getElementById('originalText');
        if (originalTextArea) {
            originalTextArea.value = text;
            
            // Disparar evento de tradução
            const event = new Event('input', { bubbles: true });
            originalTextArea.dispatchEvent(event);
        }
    }

        // Sistema de Reconhecimento de Gênero via Câmera
        this.genderRecognition = {
            isActive: false,
            currentGender: 'unknown',
            confidence: 0,
            video: null,
            canvas: null,
            context: null,
            detectionInterval: null,
            features: {
                faceWidth: 0,
                faceHeight: 0,
                jawWidth: 0,
                eyebrowDistance: 0,
                noseWidth: 0,
                lipThickness: 0
            }
        };
        
        // Inicializar sistema de reconhecimento de gênero
        async initGenderRecognition() {
            console.log('🔬 Inicializando reconhecimento de gênero...');
            
            try {
                // Configurar elementos de vídeo
                this.genderRecognition.video = document.getElementById('cameraVideo');
                this.genderRecognition.canvas = document.createElement('canvas');
                this.genderRecognition.context = this.genderRecognition.canvas.getContext('2d');
                
                // Solicitar acesso à câmera
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 640 },
                        height: { ideal: 480 },
                        facingMode: 'user'
                    }
                });
                
                this.genderRecognition.video.srcObject = stream;
                this.genderRecognition.isActive = true;
                
                // Iniciar detecção automática
                this.startGenderDetection();
                
                console.log('✅ Sistema de reconhecimento de gênero ativo');
                this.updateGenderStatus('👤 Sistema ativo - Detectando...');
                
            } catch (error) {
                console.error('❌ Erro ao inicializar reconhecimento de gênero:', error);
                this.updateGenderStatus('❌ Erro: Câmera não disponível');
            }
        }
        
        // Iniciar detecção contínua de gênero
        startGenderDetection() {
            if (this.genderRecognition.detectionInterval) {
                clearInterval(this.genderRecognition.detectionInterval);
            }
            
            this.genderRecognition.detectionInterval = setInterval(() => {
                this.detectGender();
            }, 2000); // Detectar a cada 2 segundos
        }
        
        // Detectar gênero usando análise facial
        detectGender() {
            if (!this.genderRecognition.isActive || !this.genderRecognition.video) return;
            
            try {
                const video = this.genderRecognition.video;
                const canvas = this.genderRecognition.canvas;
                const context = this.genderRecognition.context;
                
                // Configurar canvas
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                
                // Capturar frame atual
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                // Analisar características faciais
                const features = this.analyzeFacialFeatures(context, canvas);
                
                if (features.faceDetected) {
                    // Calcular probabilidade de gênero
                    const genderResult = this.calculateGenderProbability(features);
                    
                    // Atualizar estado
                    this.genderRecognition.currentGender = genderResult.gender;
                    this.genderRecognition.confidence = genderResult.confidence;
                    this.genderRecognition.features = features;
                    
                    // Atualizar interface
                    this.updateGenderDisplay(genderResult);
                    
                    // Configurar voz baseada no gênero
                    this.configureVoiceForGender(genderResult.gender);
                }
                
            } catch (error) {
                console.error('❌ Erro na detecção de gênero:', error);
            }
        }
        
        // Analisar características faciais usando ciência de dados
        analyzeFacialFeatures(context, canvas) {
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;
            
            // Detectar face usando análise de pixels
            const faceRegion = this.detectFaceRegion(data, canvas.width, canvas.height);
            
            if (!faceRegion.detected) {
                return { faceDetected: false };
            }
            
            // Extrair características biométricas
            const features = {
                faceDetected: true,
                faceWidth: faceRegion.width,
                faceHeight: faceRegion.height,
                faceRatio: faceRegion.width / faceRegion.height,
                
                // Características específicas por gênero
                jawWidth: this.estimateJawWidth(faceRegion),
                eyebrowDistance: this.estimateEyebrowDistance(faceRegion),
                noseWidth: this.estimateNoseWidth(faceRegion),
                lipThickness: this.estimateLipThickness(faceRegion),
                
                // Análise de cor e textura
                skinTone: this.analyzeSkinTone(data, faceRegion),
                hairLength: this.estimateHairLength(faceRegion)
            };
            
            return features;
        }
        
        // Detectar região facial
        detectFaceRegion(data, width, height) {
            // Algoritmo simplificado de detecção facial
            // Procura por regiões com tom de pele
            
            let minX = width, maxX = 0, minY = height, maxY = 0;
            let facePixels = 0;
            
            for (let y = 0; y < height; y += 4) {
                for (let x = 0; x < width; x += 4) {
                    const i = (y * width + x) * 4;
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    
                    // Detectar tom de pele
                    if (this.isSkinTone(r, g, b)) {
                        facePixels++;
                        minX = Math.min(minX, x);
                        maxX = Math.max(maxX, x);
                        minY = Math.min(minY, y);
                        maxY = Math.max(maxY, y);
                    }
                }
            }
            
            const detected = facePixels > 100; // Threshold mínimo
            
            return {
                detected,
                x: minX,
                y: minY,
                width: maxX - minX,
                height: maxY - minY,
                pixels: facePixels
            };
        }
        
        // Verificar se é tom de pele
        isSkinTone(r, g, b) {
            // Algoritmo para detectar tons de pele
            return (r > 95 && g > 40 && b > 20 &&
                    Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
                    Math.abs(r - g) > 15 && r > g && r > b);
        }
        
        // Calcular probabilidade de gênero usando machine learning simplificado
        calculateGenderProbability(features) {
            // Modelo baseado em características biométricas conhecidas
            let maleScore = 0;
            let femaleScore = 0;
            
            // Análise da proporção facial
            if (features.faceRatio > 0.75) {
                maleScore += 0.3; // Faces masculinas tendem a ser mais largas
            } else {
                femaleScore += 0.3;
            }
            
            // Análise da largura da mandíbula
            if (features.jawWidth > features.faceWidth * 0.8) {
                maleScore += 0.4; // Mandíbulas masculinas são mais largas
            } else {
                femaleScore += 0.4;
            }
            
            // Análise da distância entre sobrancelhas
            if (features.eyebrowDistance > features.faceWidth * 0.3) {
                maleScore += 0.2;
            } else {
                femaleScore += 0.2;
            }
            
            // Análise da largura do nariz
            if (features.noseWidth > features.faceWidth * 0.15) {
                maleScore += 0.1;
            } else {
                femaleScore += 0.1;
            }
            
            // Normalizar scores
            const total = maleScore + femaleScore;
            maleScore = maleScore / total;
            femaleScore = femaleScore / total;
            
            const gender = maleScore > femaleScore ? 'male' : 'female';
            const confidence = Math.max(maleScore, femaleScore);
            
            return {
                gender,
                confidence: Math.round(confidence * 100),
                scores: { male: Math.round(maleScore * 100), female: Math.round(femaleScore * 100) }
            };
        }
        
        // Métodos auxiliares para análise de características
        estimateJawWidth(faceRegion) {
            return faceRegion.width * 0.8; // Estimativa simplificada
        }
        
        estimateEyebrowDistance(faceRegion) {
            return faceRegion.width * 0.25; // Estimativa simplificada
        }
        
        estimateNoseWidth(faceRegion) {
            return faceRegion.width * 0.12; // Estimativa simplificada
        }
        
        estimateLipThickness(faceRegion) {
            return faceRegion.height * 0.05; // Estimativa simplificada
        }
        
        analyzeSkinTone(data, faceRegion) {
            // Análise simplificada do tom de pele
            return 'medium';
        }
        
        estimateHairLength(faceRegion) {
            // Estimativa simplificada do comprimento do cabelo
            return 'medium';
        }
        
        // Atualizar display de gênero
        updateGenderDisplay(result) {
            const genderIcon = result.gender === 'male' ? '👨' : '👩';
            const genderText = result.gender === 'male' ? 'Masculino' : 'Feminino';
            const status = `${genderIcon} ${genderText} (${result.confidence}%)`;
            
            this.updateGenderStatus(status);
            
            console.log(`🔬 Gênero detectado: ${genderText} com ${result.confidence}% de confiança`);
        }
        
        // Atualizar status na interface
        updateGenderStatus(status) {
            const genderStatus = document.getElementById('genderStatus');
            if (genderStatus) {
                genderStatus.textContent = status;
            }
        }
        
        this.voiceSystem = {
            recognition: null,
            synthesis: null,
            isListening: false,
            isAutoMode: true, // Modo automático ativado por padrão
            activationCommand: 'neuro traduza',
            currentGender: 'neutral',
            supportedLanguages: ['pt-BR', 'en-US'],
            continuousListening: true,
            autoTranslate: true
        };
        
        this.visionSystem = {
            stream: null,
            canvas: null,
            context: null,
            isActive: false,
            detectedGender: null,
            confidence: 0
        };

        // Configurações de tradução automática
        this.autoTranslateConfig = {
            enabled: true,
            minConfidence: 0.7,
            silenceTimeout: 2000, // 2 segundos de silêncio para processar
            lastSpeechTime: 0,
            processingTimeout: null
        };
        
        this.init();
    }

    async init() {
        console.log('🤖 Inicializando NeuroAI Voice & Vision...');
        
        try {
            await this.initVoiceSystem();
            await this.initVisionSystem();
            await this.);
            
        } catch (error) {
            console.error('❌ Erro na inicialização do NeuroAI:', error);
            this.dispatchEvent('neuro-ai-error', { error: error.message });
        }
    }

    async initVoiceSystem() {
        console.log('🎤 Inicializando sistema de voz...');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('❌ Reconhecimento de voz não suportado');
            this.updateVoiceStatus('Reconhecimento não suportado');
            return;
        }
        
        // Limpar qualquer reconhecimento anterior
        if (this.voiceSystem.recognition) {
            try {
                this.voiceSystem.recognition.stop();
                this.voiceSystem.recognition.abort();
            } catch (e) {
                console.log('⚠️ Limpeza de reconhecimento anterior:', e);
            }
            this.voiceSystem.recognition = null;
        }
        
        // Criar nova instância
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.voiceSystem.recognition = new SpeechRecognition();
        
        // Configurações básicas
        this.voiceSystem.recognition.continuous = true;
        this.voiceSystem.recognition.interimResults = true;
        this.voiceSystem.recognition.lang = 'pt-BR';
        this.voiceSystem.recognition.maxAlternatives = 1;
        
        // Estado inicial
        this.voiceSystem.isListening = false;
        this.voiceSystem.recognitionState = 'stopped';
        this.voiceSystem.restartAttempts = 0;
        this.voiceSystem.maxRestartAttempts = 3;
        
        // Configurar eventos
        this.voiceSystem.recognition.onstart = () => {
            console.log('🎤 Reconhecimento iniciado');
            this.voiceSystem.isListening = true;
            this.voiceSystem.recognitionState = 'active';
            this.voiceSystem.restartAttempts = 0;
            this.updateVoiceStatus('Escutando comando "Neuro, traduza"...');
        };

        this.voiceSystem.recognition.onresult = (event) => {
            this.handleVoiceResult(event);
        };

        this.voiceSystem.recognition.onerror = (event) => {
            console.error('❌ Erro de reconhecimento:', event.error);
            this.voiceSystem.isListening = false;
            this.voiceSystem.recognitionState = 'error';
            
            // Não tentar reiniciar em caso de permissão negada
            if (event.error === 'not-allowed') {
                this.updateVoiceStatus('Permissão de microfone necessária');
                return;
            }
            
            // Para outros erros, tentar reiniciar com limite
            if (this.voiceSystem.isAutoMode && this.voiceSystem.restartAttempts < this.voiceSystem.maxRestartAttempts) {
                this.voiceSystem.restartAttempts++;
                console.log(`🔄 Tentativa de reinício ${this.voiceSystem.restartAttempts}/${this.voiceSystem.maxRestartAttempts}`);
                
                setTimeout(() => {
                    this.safeStartRecognition();
                }, 2000 * this.voiceSystem.restartAttempts); // Delay progressivo
            } else {
                this.updateVoiceStatus('Erro no reconhecimento - modo manual ativado');
                this.voiceSystem.isAutoMode = false;
            }
        };

        this.voiceSystem.recognition.onend = () => {
            console.log('🎤 Reconhecimento finalizado');
            this.voiceSystem.isListening = false;
            
            if (this.voiceSystem.recognitionState !== 'error') {
                this.voiceSystem.recognitionState = 'stopped';
            }
            
            // Reiniciar apenas se estiver em modo auto e não houve muitos erros
            if (this.voiceSystem.isAutoMode && 
                this.voiceSystem.restartAttempts < this.voiceSystem.maxRestartAttempts) {
                
                setTimeout(() => {
                    this.safeStartRecognition();
                }, 1000);
            }
        };
        
        console.log('✅ Sistema de voz configurado');
    }
        
        // Configurar reconhecimento de voz
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.voiceSystem.recognition = new SpeechRecognition();
        
        // Configurações otimizadas para reconhecimento contínuo
        this.voiceSystem.recognition.continuous = true;
        this.voiceSystem.recognition.interimResults = true;
        this.voiceSystem.recognition.lang = 'pt-BR';
        this.voiceSystem.recognition.maxAlternatives = 1;
        
        // Adicionar controle de estado interno
        this.voiceSystem.recognitionState = 'stopped'; // stopped, starting, active, stopping
        
        // Event listeners para reconhecimento
        this.voiceSystem.recognition.onstart = () => {
            console.log('🎤 Reconhecimento de voz iniciado');
            this.voiceSystem.isListening = true;
            this.voiceSystem.recognitionState = 'active';
            this.updateVoiceStatus('Ouvindo...');
            this.dispatchEvent('voice-recognition-start');
        };
        
        this.voiceSystem.recognition.onresult = (event) => {
            this.handleVoiceResult(event);
        };
        
        this.voiceSystem.recognition.onerror = (event) => {
            console.error('❌ Erro no reconhecimento:', event.error);
            this.voiceSystem.recognitionState = 'stopped';
            this.voiceSystem.isListening = false;
            this.handleVoiceError(event);
        };
        
        this.voiceSystem.recognition.onend = () => {
            console.log('🎤 Reconhecimento finalizado');
            this.voiceSystem.isListening = false;
            this.voiceSystem.recognitionState = 'stopped';
            
            // Reiniciar automaticamente apenas se estiver em modo auto e não houve erro
            if (this.voiceSystem.isAutoMode && 
                this.voiceSystem.recognitionState === 'stopped') {
                console.log('🔄 Reiniciando reconhecimento automático...');
                setTimeout(() => {
                    if (this.voiceSystem.isAutoMode && 
                        this.voiceSystem.recognitionState === 'stopped') {
                        this.startVoiceActivation();
                    }
                }, 1000);
            }
        };
        
        // Configurar síntese de voz
        if ('speechSynthesis' in window) {
            this.voiceSystem.synthesis = window.speechSynthesis;
        }
        
        console.log('✅ Sistema de voz configurado');
    }

    // Recuperação de emergência para erros persistentes
    emergencyRecovery() {
        console.log('🚨 Iniciando recuperação de emergência...');
        
        try {
            // Parar qualquer reconhecimento ativo
            if (this.voiceSystem.recognition) {
                this.voiceSystem.recognition.stop();
                this.voiceSystem.recognition.abort();
            }
        } catch (error) {
            console.log('⚠️ Erro ao parar reconhecimento na recuperação:', error);
        }
        
        // Limpar estado
        this.voiceSystem.isListening = false;
        this.voiceSystem.recognitionState = 'stopped';
        
        // Recriar sistema de voz após delay
        setTimeout(() => {
            console.log('🔄 Recriando sistema de voz...');
            this.initVoiceSystem();
            
            if (this.voiceSystem.isAutoMode) {
                setTimeout(() => {
                    this.startVoiceActivation();
                }, 2000);
            }
        }, 1000);
    }

    // Validação robusta do estado do reconhecimento
    validateRecognitionState() {
        try {
            // Verificar se o reconhecimento existe
            if (!this.voiceSystem.recognition) {
                console.log('🔄 Reconhecimento não existe, recriando...');
                this.initVoiceSystem();
                return false;
            }
            
            // Verificar inconsistências de estado
            const actuallyListening = this.voiceSystem.recognition.readyState !== undefined;
            if (this.voiceSystem.isListening !== actuallyListening) {
                console.log('🔄 Estado inconsistente detectado, corrigindo...');
                this.voiceSystem.isListening = actuallyListening;
                this.voiceSystem.recognitionState = actuallyListening ? 'active' : 'stopped';
            }
            
            return true;
        } catch (error) {
            console.error('❌ Erro na validação de estado:', error);
            return false;
        }
    }

    async initVisionSystem() {
        console.log('👁️ Inicializando sistema de visão...');
        
        try {
            // Verificar suporte a getUserMedia
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('getUserMedia não suportado');
            }
            
            // Configurar canvas para processamento
            this.visionSystem.canvas = document.createElement('canvas');
            this.visionSystem.context = this.visionSystem.canvas.getContext('2d');
            
            console.log('✅ Sistema de visão configurado');
            
        } catch (error) {
            console.warn('⚠️ Sistema de visão não disponível:', error);
        }
    }

    async setupEventListeners() {
        console.log('🎧 Configurando event listeners...');
        
        // Escutar eventos de tradução
        document.addEventListener('translation-complete', (event) => {
            this.handleTranslationComplete(event.detail);
        });
        
        // Escutar eventos de detecção de gênero
        document.addEventListener('gender-detected', (event) => {
            this.handleGenderDetection(event.detail);
        });
        
        console.log('✅ Event listeners configurados');
    }

    // Método principal para ativação automática
    startAutoMode() {
        console.log('🚀 Iniciando modo automático de tradução por voz');
        
        this.voiceSystem.isAutoMode = true;
        this.autoTranslateConfig.enabled = true;
        
        // Atualizar interface
        this.updateVoiceStatus('Modo automático ativo - Diga "Neuro traduza" seguido da frase');
        
        // Iniciar reconhecimento contínuo
        this.startVoiceActivation();
        
        // Notificar outros componentes
        this.dispatchEvent('auto-mode-started');
    }

    stopAutoMode() {
        console.log('⏹️ Parando modo automático');
        
        this.voiceSystem.isAutoMode = false;
        this.autoTranslateConfig.enabled = false;
        
        if (this.voiceSystem.recognition && this.voiceSystem.isListening) {
            this.voiceSystem.recognition.stop();
        }
        
        this.updateVoiceStatus('Modo automático desativado');
        this.dispatchEvent('auto-mode-stopped');
    }

    // Método principal para ativação por comando de voz
    
    // Método seguro para iniciar reconhecimento
    safeStartRecognition() {
        if (!this.voiceSystem.recognition) {
            console.log('🔄 Reconhecimento não existe, recriando...');
            this.initVoiceSystem();
            return;
        }
        
        // Verificar se já está ativo
        if (this.voiceSystem.isListening) {
            console.log('🎤 Reconhecimento já está ativo');
            return;
        }
        
        try {
            this.voiceSystem.recognitionState = 'starting';
            this.voiceSystem.recognition.start();
        } catch (error) {
            console.error('❌ Erro ao iniciar reconhecimento:', error);
            
            if (error.name === 'InvalidStateError') {
                // Forçar parada e tentar novamente
                try {
                    this.voiceSystem.recognition.stop();
                    this.voiceSystem.recognition.abort();
                } catch (stopError) {
                    console.log('⚠️ Erro ao parar:', stopError);
                }
                
                // Recriar reconhecimento após erro de estado
                setTimeout(() => {
                    this.initVoiceSystem().then(() => {
                        if (this.voiceSystem.isAutoMode) {
                            setTimeout(() => this.safeStartRecognition(), 1000);
                        }
                    });
                }, 1000);
            }
        }
    }

    async startVoiceActivation() {
        if (!this.isInitialized) {
            console.warn('⚠️ NeuroAI não inicializado');
            return;
        }
        
        console.log('🎤 Iniciando escuta por comando de ativação...');
        this.safeStartRecognition();
    }
        
        // Verificar se já está ativo ou iniciando
        if (this.voiceSystem.recognitionState === 'active' || this.voiceSystem.recognitionState === 'starting') {
            console.log('🎤 Reconhecimento já está ativo ou iniciando');
            return;
        }
        
        console.log('🎤 Iniciando escuta por comando de ativação...');
        this.voiceSystem.recognitionState = 'starting';
        
        try {
            // Garantir que o reconhecimento está parado antes de iniciar
            if (this.voiceSystem.isListening) {
                this.voiceSystem.recognition.stop();
                await new Promise(resolve => setTimeout(resolve, 200));
            }
            
            this.voiceSystem.recognition.start();
        } catch (error) {
            console.error('❌ Erro ao iniciar reconhecimento:', error);
            this.voiceSystem.recognitionState = 'stopped';
            
            // Tratamento específico para diferentes tipos de erro
            if (error.name === 'InvalidStateError') {
                console.log('🔄 Estado inválido detectado, forçando parada e reinício...');
                try {
                    this.voiceSystem.recognition.stop();
                } catch (stopError) {
                    console.log('⚠️ Erro ao parar reconhecimento:', stopError);
                }
                
                // Aguardar mais tempo antes de tentar novamente
                if (this.voiceSystem.isAutoMode) {
                    setTimeout(() => {
                        if (this.voiceSystem.recognitionState === 'stopped') {
                            this.startVoiceActivation();
                        }
                    }, 1000);
                }
            } else if (error.name === 'NotAllowedError') {
                console.error('❌ Permissão de microfone negada');
                this.updateVoiceStatus('Permissão de microfone necessária');
            } else if (this.voiceSystem.isAutoMode) {
                // Para outros erros, tentar novamente após delay maior
                setTimeout(() => {
                    if (this.voiceSystem.recognitionState === 'stopped') {
                        this.startVoiceActivation();
                    }
                }, 2000);
            }
        }
    }

    stopVoiceActivation() {
        console.log('🛑 Parando reconhecimento de voz...');
        
        // Definir estado como parando para evitar conflitos
        this.voiceSystem.recognitionState = 'stopping';
        
        try {
            if (this.voiceSystem.recognition && this.voiceSystem.isListening) {
                this.voiceSystem.recognition.stop();
            }
        } catch (error) {
            console.warn('⚠️ Erro ao parar reconhecimento:', error);
        }
        
        // Garantir que o estado seja limpo
        setTimeout(() => {
            this.voiceSystem.isListening = false;
            this.voiceSystem.recognitionState = 'stopped';
            this.updateVoiceStatus('Reconhecimento parado');
        }, 100);
    }
    
    handleVoiceResult(event) {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            const confidence = event.results[i][0].confidence;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
                console.log(`🎯 Texto final reconhecido: "${transcript}" (confiança: ${confidence})`);
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Atualizar tempo da última fala
        this.autoTranslateConfig.lastSpeechTime = Date.now();
        
        // Verificar comando de ativação no texto final
        if (finalTranscript) {
            this.processVoiceCommand(finalTranscript);
        }
        
        // Atualizar interface com texto interim
        this.updateTranscription(interimTranscript, finalTranscript);
        
        // Configurar timeout para processar após silêncio
        if (this.autoTranslateConfig.enabled && finalTranscript) {
            this.scheduleAutoTranslation(finalTranscript);
        }
    }

    processVoiceCommand(text) {
        const lowerText = text.toLowerCase().trim();
        console.log(`🔍 Processando comando: "${lowerText}"`);
        
        // Verificar se contém o comando de ativação
        if (lowerText.includes(this.voiceSystem.activationCommand)) {
            console.log('🎯 Comando de ativação detectado!');
            
            // Extrair texto após o comando
            const commandIndex = lowerText.indexOf(this.voiceSystem.activationCommand);
            const textToTranslate = text.substring(commandIndex + this.voiceSystem.activationCommand.length).trim();
            
            if (textToTranslate.length > 0) {
                console.log(`📝 Texto para traduzir: "${textToTranslate}"`);
                this.triggerTranslation(textToTranslate);
            } else {
                console.log('⚠️ Nenhum texto encontrado após o comando');
                this.updateVoiceStatus('Comando detectado - aguardando texto para traduzir...');
            }
        }
    }

    scheduleAutoTranslation(text) {
        // Limpar timeout anterior
        if (this.autoTranslateConfig.processingTimeout) {
            clearTimeout(this.autoTranslateConfig.processingTimeout);
        }
        
        // Agendar processamento após silêncio
        this.autoTranslateConfig.processingTimeout = setTimeout(() => {
            const timeSinceLastSpeech = Date.now() - this.autoTranslateConfig.lastSpeechTime;
            
            if (timeSinceLastSpeech >= this.autoTranslateConfig.silenceTimeout) {
                console.log('🔄 Processando tradução automática após silêncio');
                this.processVoiceCommand(text);
            }
        }, this.autoTranslateConfig.silenceTimeout);
    }

    triggerTranslation(text) {
        console.log(`🌐 Iniciando tradução: "${text}"`);
        
        // Atualizar interface
        this.updateVoiceStatus('Traduzindo...');
        
        // Preencher campo de entrada
        const inputField = document.getElementById('inputText');
        if (inputField) {
            inputField.value = text;
            
            // Disparar evento de input para atualizar outros componentes
            inputField.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        // Ativar tradução automática se disponível
        const autoTranslateBtn = document.querySelector('.auto-translate-btn');
        if (autoTranslateBtn && !autoTranslateBtn.classList.contains('active')) {
            autoTranslateBtn.click();
        }
        
        // Disparar tradução
        const translateBtn = document.getElementById('translateBtn');
        if (translateBtn) {
            translateBtn.click();
        }
        
        // Notificar outros componentes
        this.dispatchEvent('voice-translation-triggered', { text });
    }

    handleTranslationComplete(data) {
        console.log('✅ Tradução concluída:', data);
        
        // Atualizar status
        this.updateVoiceStatus('Tradução concluída - aguardando próximo comando...');
        
        // Reiniciar escuta se estiver em modo automático
        if (this.voiceSystem.isAutoMode && !this.voiceSystem.isListening) {
            setTimeout(() => {
                this.startVoiceActivation();
            }, 1000);
        }
    }

    handleGenderDetection(data) {
        if (data && data.smoothed && data.smoothed.gender) {
            const detectedGender = data.smoothed.gender;
            
            if (this.voiceSystem.currentGender !== detectedGender) {
                console.log(`👤 Gênero detectado: ${detectedGender}`);
                this.voiceSystem.currentGender = detectedGender;
                
                // Notificar sistema de avatar
                this.dispatchEvent('voice-gender-detected', { gender: detectedGender });
            }
        }
    }

    updateGenderDisplay(gender) {
        const genderElement = document.querySelector('.gender-status');
        if (genderElement) {
            const genderText = gender === 'male' ? 'Masculino' : 
                              gender === 'female' ? 'Feminino' : 'Detectando...';
            genderElement.textContent = `Gênero: ${genderText}`;
        }
    }

    updateVoiceStatus(status) {
        console.log(`🎤 Status: ${status}`);
        
        // Atualizar elemento de status se existir
        const statusElement = document.querySelector('.voice-status') || 
                            document.querySelector('#voiceStatus') ||
                            document.querySelector('.ai-status');
        
        if (statusElement) {
            statusElement.textContent = status;
        }
        
        // Atualizar indicador visual
        const voiceIndicator = document.querySelector('.voice-indicator');
        if (voiceIndicator) {
            if (status.includes('Ouvindo') || status.includes('ativo')) {
                voiceIndicator.classList.add('active');
            } else {
                voiceIndicator.classList.remove('active');
            }
        }
    }

    updateTranscription(interim, final) {
        // Atualizar campo de transcrição se existir
        const transcriptionElement = document.querySelector('.voice-transcription') ||
                                   document.querySelector('#voiceTranscription');
        
        if (transcriptionElement) {
            transcriptionElement.innerHTML = `
                <span class="interim">${interim}</span>
                <span class="final">${final}</span>
            `;
        }
    }

    // Configurações e controles
    setActivationCommand(command) {
        this.voiceSystem.activationCommand = command.toLowerCase();
        console.log(`🎯 Comando de ativação definido: "${command}"`);
    }

    setLanguage(language) {
        if (this.voiceSystem.supportedLanguages.includes(language)) {
            this.voiceSystem.recognition.lang = language;
            console.log(`🌐 Idioma definido: ${language}`);
        }
    }

    toggleAutoMode() {
        if (this.voiceSystem.isAutoMode) {
            this.stopAutoMode();
        } else {
            this.startAutoMode();
        }
    }

    // Análise de voz para detecção de gênero
    analyzeVoiceForGender(audioData) {
        // Implementação básica de análise de frequência
        // Em uma implementação real, usaria ML para análise mais precisa
        
        try {
            const frequencies = this.extractFrequencies(audioData);
            const fundamentalFreq = this.getFundamentalFrequency(frequencies);
            
            // Classificação básica baseada em frequência fundamental
            let gender = 'neutral';
            let confidence = 0.5;
            
            if (fundamentalFreq < 165) {
                gender = 'male';
                confidence = Math.min(0.9, (165 - fundamentalFreq) / 80);
            } else if (fundamentalFreq > 200) {
                gender = 'female';
                confidence = Math.min(0.9, (fundamentalFreq - 200) / 100);
            }
            
            return { gender, confidence, frequency: fundamentalFreq };
            
        } catch (error) {
            console.warn('⚠️ Erro na análise de voz:', error);
            return { gender: 'neutral', confidence: 0, frequency: 0 };
        }
    }

    extractFrequencies(audioData) {
        // Implementação simplificada de FFT
        // Em produção, usaria uma biblioteca como fft.js
        return new Array(256).fill(0).map(() => Math.random() * 100);
    }

    getFundamentalFrequency(frequencies) {
        // Encontrar pico de frequência (simulado)
        let maxIndex = 0;
        let maxValue = 0;
        
        for (let i = 0; i < frequencies.length; i++) {
            if (frequencies[i] > maxValue) {
                maxValue = frequencies[i];
                maxIndex = i;
            }
        }
        
        // Converter índice para frequência (aproximação)
        return 80 + (maxIndex / frequencies.length) * 300;
    }

    handleVoiceError(event) {
        const error = event.error;
        console.error('❌ Erro de voz:', error);
        
        // Atualizar estado para parado
        this.voiceSystem.recognitionState = 'stopped';
        this.voiceSystem.isListening = false;
        
        // Tratamento específico por tipo de erro
        switch (error) {
            case 'no-speech':
                console.log('🔇 Nenhuma fala detectada');
                this.updateVoiceStatus('Aguardando comando...');
                break;
                
            case 'audio-capture':
                console.error('❌ Erro na captura de áudio');
                this.updateVoiceStatus('Erro no microfone');
                break;
                
            case 'not-allowed':
                console.error('❌ Permissão de microfone negada');
                this.updateVoiceStatus('Permissão necessária');
                return; // Não tentar reiniciar
                
            case 'network':
                console.error('❌ Erro de rede');
                this.updateVoiceStatus('Erro de conexão');
                break;
                
            case 'aborted':
                console.log('⏹️ Reconhecimento interrompido');
                this.updateVoiceStatus('Reconhecimento parado');
                break;
                
            case 'service-not-allowed':
                console.error('❌ Serviço não permitido');
                this.updateVoiceStatus('Serviço indisponível');
                return; // Não tentar reiniciar
                
            default:
                console.error('❌ Erro desconhecido:', error);
                this.updateVoiceStatus('Erro no reconhecimento');
        }
        
        // Reiniciar automaticamente apenas em modo auto e para erros recuperáveis
        if (this.voiceSystem.isAutoMode && 
            error !== 'not-allowed' && 
            error !== 'service-not-allowed') {
            
            console.log('🔄 Tentando reiniciar reconhecimento em 3 segundos...');
            setTimeout(() => {
                if (this.voiceSystem.isAutoMode && 
                    this.voiceSystem.recognitionState === 'stopped') {
                    this.startVoiceActivation();
                }
            }, 3000); // Aumentado para 3 segundos
        }
    }

    // Métodos de utilidade
    dispatchEvent(eventName, data = {}) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
        console.log(`📡 Evento disparado: ${eventName}`, data);
    }

    // Limpeza e destruição
    cleanup() {
        console.log('🧹 Limpando recursos do NeuroAI...');
        
        this.stopAutoMode();
        
        if (this.visionSystem.stream) {
            this.visionSystem.stream.getTracks().forEach(track => track.stop());
        }
        
        if (this.autoTranslateConfig.processingTimeout) {
            clearTimeout(this.autoTranslateConfig.processingTimeout);
        }
    }

    // Métodos de status e diagnóstico
    getStatus() {
        return {
            initialized: this.isInitialized,
            voice: {
                listening: this.voiceSystem.isListening,
                autoMode: this.voiceSystem.isAutoMode,
                language: this.voiceSystem.recognition?.lang,
                command: this.voiceSystem.activationCommand
            },
            vision: {
                active: this.visionSystem.isActive,
                gender: this.visionSystem.detectedGender,
                confidence: this.visionSystem.confidence
            },
            autoTranslate: {
                enabled: this.autoTranslateConfig.enabled,
                lastSpeech: this.autoTranslateConfig.lastSpeechTime
            }
        };
    }
}

// Exportar para uso global
window.NeuroAIVoiceVision = NeuroAIVoiceVision;

console.log('🤖 Módulo NeuroAI Voice & Vision carregado!');
        
        // Configurar voz baseada no gênero detectado
        configureVoiceForGender(gender) {
            if (!this.tts || !this.tts.synth) return;
            
            console.log(`🗣️ Configurando voz para gênero: ${gender}`);
            
            // Obter vozes disponíveis
            const voices = this.tts.synth.getVoices();
            let selectedVoice = null;
            
            if (gender === 'male') {
                // Procurar vozes masculinas em português
                selectedVoice = voices.find(voice => 
                    voice.lang.includes('pt') && 
                    (voice.name.toLowerCase().includes('male') || 
                     voice.name.toLowerCase().includes('masculin') ||
                     voice.name.toLowerCase().includes('homem') ||
                     voice.name.toLowerCase().includes('ricardo') ||
                     voice.name.toLowerCase().includes('felipe'))
                ) || voices.find(voice => 
                    voice.lang.includes('pt') && voice.name.toLowerCase().includes('google')
                );
            } else if (gender === 'female') {
                // Procurar vozes femininas em português
                selectedVoice = voices.find(voice => 
                    voice.lang.includes('pt') && 
                    (voice.name.toLowerCase().includes('female') || 
                     voice.name.toLowerCase().includes('feminin') ||
                     voice.name.toLowerCase().includes('mulher') ||
                     voice.name.toLowerCase().includes('maria') ||
                     voice.name.toLowerCase().includes('ana') ||
                     voice.name.toLowerCase().includes('lucia'))
                ) || voices.find(voice => 
                    voice.lang.includes('pt')
                );
            }
            
            // Aplicar voz selecionada
            if (selectedVoice) {
                this.tts.voice = selectedVoice;
                console.log(`✅ Voz configurada: ${selectedVoice.name} (${gender})`);
                
                // Ajustar parâmetros da voz
                if (gender === 'male') {
                    this.tts.pitch = 0.8; // Tom mais grave
                    this.tts.rate = 0.9;  // Velocidade ligeiramente mais lenta
                } else {
                    this.tts.pitch = 1.2; // Tom mais agudo
                    this.tts.rate = 1.0;  // Velocidade normal
                }
            } else {
                console.warn('⚠️ Nenhuma voz específica encontrada para o gênero detectado');
            }
        }
        
        // Método melhorado para síntese de voz
        async speakText(text, options = {}) {
            if (!this.tts || !this.tts.synth) {
                console.error('❌ Sistema TTS não disponível');
                return;
            }
            
            try {
                // Parar qualquer fala anterior
                this.tts.synth.cancel();
                
                // Criar utterance
                const utterance = new SpeechSynthesisUtterance(text);
                
                // Aplicar configurações baseadas no gênero
                if (this.genderRecognition.currentGender !== 'unknown') {
                    this.configureVoiceForGender(this.genderRecognition.currentGender);
                }
                
                // Configurar utterance
                utterance.voice = this.tts.voice;
                utterance.pitch = options.pitch || this.tts.pitch || 1.0;
                utterance.rate = options.rate || this.tts.rate || 1.0;
                utterance.volume = options.volume || 1.0;
                utterance.lang = options.lang || 'pt-BR';
                
                // Eventos
                utterance.onstart = () => {
                    console.log('🗣️ Iniciando síntese de voz');
                };
                
                utterance.onend = () => {
                    console.log('✅ Síntese de voz concluída');
                };
                
                utterance.onerror = (error) => {
                    console.error('❌ Erro na síntese de voz:', error);
                };
                
                // Falar
                this.tts.synth.speak(utterance);
                
            } catch (error) {
                console.error('❌ Erro ao sintetizar voz:', error);
            }
        }
        