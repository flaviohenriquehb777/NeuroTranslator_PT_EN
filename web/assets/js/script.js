// NeuroTranslator PT-EN - JavaScript Principal
// Implementação das funcionalidades web

class NeuroTranslatorWeb {
    constructor() {
        this.camera = {
            stream: null,
            active: false
        };
        
        this.speech = {
            recognition: null,
            active: false,
            supported: false
        };
        
        this.translation = {
            history: [],
            autoTranslate: true,
            liveMode: false
        };
        
        this.elements = {};
        this.init();
    }
    
    init() {
        this.initElements();
        this.initEventListeners();
        this.checkBrowserSupport();
        this.loadSettings();
        console.log('🚀 NeuroTranslator Web inicializado');
    }
    
    initElements() {
        // Elementos da câmera
        this.elements.videoElement = document.getElementById('videoElement');
        this.elements.canvasElement = document.getElementById('canvasElement');
        this.elements.toggleCamera = document.getElementById('toggleCamera');
        this.elements.cameraStatus = document.getElementById('cameraStatus');
        
        // Elementos de tradução
        this.elements.sourceLanguage = document.getElementById('sourceLanguage');
        this.elements.targetLanguage = document.getElementById('targetLanguage');
        this.elements.sourceText = document.getElementById('sourceText');
        this.elements.targetText = document.getElementById('targetText');
        this.elements.translateBtn = document.getElementById('translateBtn');
        this.elements.swapLanguages = document.getElementById('swapLanguages');
        
        // Elementos de fala
        this.elements.toggleSpeech = document.getElementById('toggleSpeech');
        this.elements.speechStatus = document.getElementById('speechStatus');
        
        // Elementos de controle
        this.elements.clearText = document.getElementById('clearText');
        this.elements.copyTranslation = document.getElementById('copyTranslation');
        this.elements.autoTranslate = document.getElementById('autoTranslate');
        this.elements.liveMode = document.getElementById('liveMode');
        
        // Elementos de histórico
        this.elements.historyContainer = document.getElementById('historyContainer');
        this.elements.clearHistory = document.getElementById('clearHistory');
        
        // Elementos de status
        this.elements.translationStatus = document.getElementById('translationStatus');
        this.elements.processingTime = document.getElementById('processingTime');
        this.elements.loadingOverlay = document.getElementById('loadingOverlay');
    }
    
    initEventListeners() {
        // Câmera
        this.elements.toggleCamera.addEventListener('click', () => this.toggleCamera());
        
        // Tradução
        this.elements.translateBtn.addEventListener('click', () => this.translateText());
        this.elements.swapLanguages.addEventListener('click', () => this.swapLanguages());
        this.elements.sourceText.addEventListener('input', () => this.onTextInput());
        
        // Fala
        this.elements.toggleSpeech.addEventListener('click', () => this.toggleSpeech());
        
        // Controles
        this.elements.clearText.addEventListener('click', () => this.clearText());
        this.elements.copyTranslation.addEventListener('click', () => this.copyTranslation());
        this.elements.clearHistory.addEventListener('click', () => this.clearHistory());
        
        // Configurações
        this.elements.autoTranslate.addEventListener('change', (e) => {
            this.translation.autoTranslate = e.target.checked;
            this.saveSettings();
        });
        
        this.elements.liveMode.addEventListener('change', (e) => {
            this.translation.liveMode = e.target.checked;
            this.saveSettings();
            if (e.target.checked) {
                this.startLiveMode();
            } else {
                this.stopLiveMode();
            }
        });
        
        // Teclas de atalho
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }
    
    checkBrowserSupport() {
        // Verificar suporte à câmera
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.warn('⚠️ Câmera não suportada neste navegador');
            this.elements.toggleCamera.disabled = true;
            this.elements.toggleCamera.innerHTML = '<i class="fas fa-video-slash"></i> Câmera não suportada';
        }
        
        // Verificar protocolo HTTPS para recursos que requerem segurança
        const isSecure = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        
        // Verificar suporte ao reconhecimento de fala
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            if (!isSecure && location.protocol !== 'file:') {
                console.warn('⚠️ Reconhecimento de fala requer HTTPS em produção');
                this.elements.toggleSpeech.disabled = true;
                this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone-slash"></i> Requer HTTPS';
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Requer HTTPS';
                this.showSecurityWarning();
            } else {
                this.speech.supported = true;
                this.initSpeechRecognition();
            }
        } else {
            console.warn('⚠️ Reconhecimento de fala não suportado neste navegador');
            this.elements.toggleSpeech.disabled = true;
            this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone-slash"></i> Fala não suportada';
            this.elements.speechStatus.textContent = '🎤 Reconhecimento: Não suportado';
        }
    }
    
    showSecurityWarning() {
        // Criar aviso sobre HTTPS apenas uma vez
        if (!document.getElementById('httpsWarning')) {
            const warning = document.createElement('div');
            warning.id = 'httpsWarning';
            warning.className = 'security-warning';
            warning.innerHTML = `
                <div class="warning-content">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Aviso de Segurança:</strong> O reconhecimento de fala requer HTTPS para funcionar.
                    <br>Para testar localmente, use: <code>python -m http.server 8000 --bind 127.0.0.1</code>
                    <button onclick="this.parentElement.parentElement.remove()" class="close-warning">×</button>
                </div>
            `;
            document.body.appendChild(warning);
        }
    }
    
    initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.speech.recognition = new SpeechRecognition();
        
        // Configurações iniciais mais conservadoras
        this.speech.recognition.continuous = false; // Evita erros de rede prolongados
        this.speech.recognition.interimResults = true;
        this.speech.recognition.maxAlternatives = 1;
        this.speech.recognition.lang = this.getLanguageCode(this.elements.sourceLanguage.value);
        
        this.speech.recognition.onstart = () => {
            console.log('🎤 Reconhecimento de fala iniciado');
            this.elements.speechStatus.textContent = '🎤 Reconhecimento: Ouvindo...';
            this.elements.toggleSpeech.classList.add('active');
        };
        
        this.speech.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Mostrar resultado intermediário
            if (interimTranscript) {
                this.elements.speechStatus.textContent = `🎤 Ouvindo: "${interimTranscript}"`;
            }
            
            if (finalTranscript) {
                this.elements.sourceText.value += finalTranscript + ' ';
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Texto capturado!';
                
                if (this.translation.autoTranslate) {
                    this.translateText();
                }
                
                // Reiniciar automaticamente se continuous mode estiver ativo
                if (this.translation.liveMode && this.speech.active) {
                    setTimeout(() => {
                        if (this.speech.active) {
                            this.speech.recognition.start();
                        }
                    }, 1000);
                }
            }
        };
        
        this.speech.recognition.onerror = (event) => {
            console.error('❌ Erro no reconhecimento de fala:', event.error);
            
            let errorMessage = '';
            let shouldRestart = false;
            
            switch(event.error) {
                case 'network':
                    errorMessage = 'Erro de rede. Tentando novamente...';
                    shouldRestart = true;
                    break;
                case 'not-allowed':
                    errorMessage = 'Permissão negada. Permita o acesso ao microfone.';
                    break;
                case 'no-speech':
                    errorMessage = 'Nenhuma fala detectada. Tente falar mais alto.';
                    shouldRestart = true;
                    break;
                case 'audio-capture':
                    errorMessage = 'Erro no microfone. Verifique se está conectado.';
                    break;
                case 'service-not-allowed':
                    errorMessage = 'Serviço não permitido. Requer HTTPS.';
                    break;
                case 'aborted':
                    errorMessage = 'Reconhecimento interrompido.';
                    break;
                default:
                    errorMessage = `Erro: ${event.error}`;
            }
            
            this.elements.speechStatus.textContent = `🎤 ${errorMessage}`;
            
            // Tentar reiniciar automaticamente para alguns erros
            if (shouldRestart && this.speech.active && this.translation.liveMode) {
                setTimeout(() => {
                    if (this.speech.active) {
                        console.log('🔄 Tentando reiniciar reconhecimento...');
                        try {
                            this.speech.recognition.start();
                        } catch (e) {
                            console.error('Erro ao reiniciar:', e);
                            this.stopSpeech();
                        }
                    }
                }, 2000);
            } else if (['not-allowed', 'service-not-allowed', 'audio-capture'].includes(event.error)) {
                this.stopSpeech();
                alert(`Erro no reconhecimento de fala: ${errorMessage}`);
            }
        };
        
        this.speech.recognition.onend = () => {
            console.log('🎤 Reconhecimento de fala finalizado');
            if (this.speech.active && !this.translation.liveMode) {
                this.stopSpeech();
            }
        };
    }
    
    async toggleCamera() {
        if (this.camera.active) {
            this.stopCamera();
        } else {
            await this.startCamera();
        }
    }
    
    async startCamera() {
        try {
            this.elements.cameraStatus.textContent = '📷 Câmera: Iniciando...';
            
            const constraints = {
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            };
            
            this.camera.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.elements.videoElement.srcObject = this.camera.stream;
            
            this.camera.active = true;
            this.elements.toggleCamera.innerHTML = '<i class="fas fa-video-slash"></i> Desativar Câmera';
            this.elements.toggleCamera.classList.add('active');
            this.elements.cameraStatus.textContent = '📷 Câmera: Ativa';
            
            // Ocultar overlay
            const overlay = document.querySelector('.camera-overlay');
            if (overlay) overlay.classList.add('hidden');
            
            console.log('✅ Câmera ativada com sucesso');
            
        } catch (error) {
            console.error('❌ Erro ao ativar câmera:', error);
            this.elements.cameraStatus.textContent = '📷 Câmera: Erro de acesso';
            
            let errorMsg = 'Erro desconhecido';
            if (error.name === 'NotAllowedError') {
                errorMsg = 'Permissão negada. Permita o acesso à câmera.';
            } else if (error.name === 'NotFoundError') {
                errorMsg = 'Câmera não encontrada.';
            } else if (error.name === 'NotReadableError') {
                errorMsg = 'Câmera em uso por outro aplicativo.';
            }
            
            alert(`Erro ao acessar câmera: ${errorMsg}`);
        }
    }
    
    stopCamera() {
        if (this.camera.stream) {
            this.camera.stream.getTracks().forEach(track => track.stop());
            this.camera.stream = null;
        }
        
        this.elements.videoElement.srcObject = null;
        this.camera.active = false;
        this.elements.toggleCamera.innerHTML = '<i class="fas fa-video"></i> Ativar Câmera';
        this.elements.toggleCamera.classList.remove('active');
        this.elements.cameraStatus.textContent = '📷 Câmera: Desativada';
        
        // Mostrar overlay
        const overlay = document.querySelector('.camera-overlay');
        if (overlay) overlay.classList.remove('hidden');
        
        console.log('📷 Câmera desativada');
    }
    
    toggleSpeech() {
        if (this.speech.active) {
            this.stopSpeech();
        } else {
            this.startSpeech();
        }
    }
    
    async startSpeech() {
        if (!this.speech.supported) {
            alert('Reconhecimento de fala não suportado neste navegador.');
            return;
        }
        
        try {
            // Verificar e solicitar permissão do microfone primeiro
            console.log('🎤 Solicitando permissão do microfone...');
            await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log('✅ Permissão do microfone concedida');
            
            this.speech.active = true;
            this.elements.speechStatus.textContent = '🎤 Reconhecimento: Iniciando...';
            
            // Configurar idioma atual
            this.speech.recognition.lang = this.getLanguageCode(this.elements.sourceLanguage.value);
            
            // Iniciar reconhecimento
            this.speech.recognition.start();
            
        } catch (error) {
            console.error('❌ Erro ao acessar microfone:', error);
            
            let errorMessage = '';
            if (error.name === 'NotAllowedError') {
                errorMessage = 'Permissão do microfone negada. Por favor, permita o acesso ao microfone.';
            } else if (error.name === 'NotFoundError') {
                errorMessage = 'Microfone não encontrado. Verifique se está conectado.';
            } else if (error.name === 'NotSupportedError') {
                errorMessage = 'Microfone não suportado neste navegador.';
            } else {
                errorMessage = `Erro ao acessar microfone: ${error.message}`;
            }
            
            this.elements.speechStatus.textContent = `❌ ${errorMessage}`;
            alert(errorMessage);
            this.speech.active = false;
        }
    }
    
    stopSpeech() {
        if (this.speech.recognition && this.speech.active) {
            this.speech.recognition.stop();
        }
        
        this.speech.active = false;
        this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone"></i> Falar';
        this.elements.toggleSpeech.classList.remove('active');
        this.elements.speechStatus.textContent = '🎤 Reconhecimento: Desativado';
    }
    
    async translateText() {
        const sourceText = this.elements.sourceText.value.trim();
        if (!sourceText) {
            alert('Digite um texto para traduzir.');
            return;
        }
        
        const sourceLang = this.elements.sourceLanguage.value;
        const targetLang = this.elements.targetLanguage.value;
        
        if (sourceLang === targetLang) {
            alert('Selecione idiomas diferentes para tradução.');
            return;
        }
        
        this.showLoading(true);
        this.elements.translationStatus.textContent = 'Traduzindo...';
        
        const startTime = Date.now();
        
        try {
            // Usar Google Translate API (via MyMemory como fallback gratuito)
            const translation = await this.callTranslationAPI(sourceText, sourceLang, targetLang);
            
            const processingTime = Date.now() - startTime;
            
            this.elements.targetText.value = translation;
            this.elements.translationStatus.textContent = 'Tradução concluída';
            this.elements.processingTime.textContent = `${processingTime}ms`;
            
            // Adicionar ao histórico
            this.addToHistory(sourceText, translation, sourceLang, targetLang);
            
            console.log('✅ Tradução concluída:', translation);
            
        } catch (error) {
            console.error('❌ Erro na tradução:', error);
            this.elements.translationStatus.textContent = 'Erro na tradução';
            this.elements.targetText.value = 'Erro: Não foi possível traduzir o texto.';
            alert('Erro na tradução. Verifique sua conexão com a internet.');
        } finally {
            this.showLoading(false);
        }
    }
    
    async callTranslationAPI(text, sourceLang, targetLang) {
        // Usando MyMemory API (gratuita, sem necessidade de chave)
        const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang}|${targetLang}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.responseStatus === 200) {
            return data.responseData.translatedText;
        } else {
            throw new Error('Falha na API de tradução');
        }
    }
    
    swapLanguages() {
        const sourceLang = this.elements.sourceLanguage.value;
        const targetLang = this.elements.targetLanguage.value;
        const sourceText = this.elements.sourceText.value;
        const targetText = this.elements.targetText.value;
        
        // Trocar idiomas
        this.elements.sourceLanguage.value = targetLang;
        this.elements.targetLanguage.value = sourceLang;
        
        // Trocar textos
        this.elements.sourceText.value = targetText;
        this.elements.targetText.value = sourceText;
        
        // Atualizar idioma do reconhecimento de fala
        if (this.speech.recognition) {
            this.speech.recognition.lang = this.getLanguageCode(targetLang);
        }
        
        console.log('🔄 Idiomas trocados');
    }
    
    clearText() {
        this.elements.sourceText.value = '';
        this.elements.targetText.value = '';
        this.elements.translationStatus.textContent = 'Pronto para traduzir';
        this.elements.processingTime.textContent = '';
    }
    
    async copyTranslation() {
        const text = this.elements.targetText.value;
        if (!text) {
            alert('Nenhuma tradução para copiar.');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(text);
            
            // Feedback visual
            const originalText = this.elements.copyTranslation.innerHTML;
            this.elements.copyTranslation.innerHTML = '<i class="fas fa-check"></i> Copiado!';
            setTimeout(() => {
                this.elements.copyTranslation.innerHTML = originalText;
            }, 2000);
            
        } catch (error) {
            console.error('❌ Erro ao copiar:', error);
            alert('Erro ao copiar texto.');
        }
    }
    
    onTextInput() {
        if (this.translation.autoTranslate && this.elements.sourceText.value.trim()) {
            // Debounce para evitar muitas chamadas
            clearTimeout(this.translateTimeout);
            this.translateTimeout = setTimeout(() => {
                this.translateText();
            }, 1000);
        }
    }
    
    addToHistory(original, translation, sourceLang, targetLang) {
        const historyItem = {
            id: Date.now(),
            original,
            translation,
            sourceLang,
            targetLang,
            timestamp: new Date().toLocaleString('pt-BR')
        };
        
        this.translation.history.unshift(historyItem);
        
        // Limitar histórico a 50 itens
        if (this.translation.history.length > 50) {
            this.translation.history = this.translation.history.slice(0, 50);
        }
        
        this.updateHistoryDisplay();
        this.saveSettings();
    }
    
    updateHistoryDisplay() {
        const container = this.elements.historyContainer;
        
        if (this.translation.history.length === 0) {
            container.innerHTML = '<p class="no-history">Nenhuma tradução realizada ainda.</p>';
            return;
        }
        
        container.innerHTML = this.translation.history.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <span>${this.getLanguageName(item.sourceLang)} → ${this.getLanguageName(item.targetLang)}</span>
                    <span>${item.timestamp}</span>
                </div>
                <div class="history-item-content">
                    <div class="history-original">${item.original}</div>
                    <div class="history-translation">${item.translation}</div>
                </div>
            </div>
        `).join('');
    }
    
    clearHistory() {
        if (confirm('Deseja limpar todo o histórico de traduções?')) {
            this.translation.history = [];
            this.updateHistoryDisplay();
            this.saveSettings();
        }
    }
    
    startLiveMode() {
        console.log('🔴 Modo ao vivo ativado');
        // Ativar câmera e fala automaticamente
        if (!this.camera.active) {
            this.startCamera();
        }
        if (!this.speech.active && this.speech.supported) {
            this.startSpeech();
        }
    }
    
    stopLiveMode() {
        console.log('⏹️ Modo ao vivo desativado');
        // Manter câmera e fala como estão, apenas desativar modo automático
    }
    
    handleKeyboard(event) {
        // Ctrl/Cmd + Enter: Traduzir
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            event.preventDefault();
            this.translateText();
        }
        
        // Ctrl/Cmd + L: Limpar texto
        if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
            event.preventDefault();
            this.clearText();
        }
        
        // Ctrl/Cmd + Shift + S: Toggle fala
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'S') {
            event.preventDefault();
            this.toggleSpeech();
        }
    }
    
    getLanguageCode(lang) {
        const codes = {
            'pt': 'pt-BR',
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR'
        };
        return codes[lang] || 'pt-BR';
    }
    
    getLanguageName(code) {
        const names = {
            'pt': '🇧🇷 Português',
            'en': '🇺🇸 Inglês',
            'es': '🇪🇸 Espanhol',
            'fr': '🇫🇷 Francês'
        };
        return names[code] || code;
    }
    
    showLoading(show) {
        this.elements.loadingOverlay.style.display = show ? 'flex' : 'none';
    }
    
    saveSettings() {
        const settings = {
            autoTranslate: this.translation.autoTranslate,
            liveMode: this.translation.liveMode,
            history: this.translation.history,
            sourceLanguage: this.elements.sourceLanguage.value,
            targetLanguage: this.elements.targetLanguage.value
        };
        
        localStorage.setItem('neurotranslator-settings', JSON.stringify(settings));
    }
    
    loadSettings() {
        try {
            const settings = JSON.parse(localStorage.getItem('neurotranslator-settings') || '{}');
            
            if (settings.autoTranslate !== undefined) {
                this.translation.autoTranslate = settings.autoTranslate;
                this.elements.autoTranslate.checked = settings.autoTranslate;
            }
            
            if (settings.liveMode !== undefined) {
                this.translation.liveMode = settings.liveMode;
                this.elements.liveMode.checked = settings.liveMode;
            }
            
            if (settings.history) {
                this.translation.history = settings.history;
                this.updateHistoryDisplay();
            }
            
            if (settings.sourceLanguage) {
                this.elements.sourceLanguage.value = settings.sourceLanguage;
            }
            
            if (settings.targetLanguage) {
                this.elements.targetLanguage.value = settings.targetLanguage;
            }
            
        } catch (error) {
            console.warn('⚠️ Erro ao carregar configurações:', error);
        }
    }
}

// Inicializar aplicação quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.neuroTranslator = new NeuroTranslatorWeb();
});

// Service Worker para PWA (opcional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('✅ Service Worker registrado:', registration);
            })
            .catch(error => {
                console.log('❌ Falha ao registrar Service Worker:', error);
            });
    });
}