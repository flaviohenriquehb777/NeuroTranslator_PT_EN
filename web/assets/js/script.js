// NeuroTranslator PT-EN - JavaScript Principal
// Implementação das funcionalidades web

class NeuroTranslatorWeb {
    constructor() {
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
        
        // Neuro Assistant
        this.neuroAssistant = {
            active: false,
            listening: false,
            wakeWordDetected: false
        };
        
        this.elements = {};
        this.init();
    }
    
    init() {
        this.initElements();
        this.initEventListeners();
        this.checkMobileCompatibility(); // Verificar compatibilidade móvel primeiro
        this.checkBrowserSupport();
        this.loadSettings();
        console.log('🚀 NeuroTranslator Web inicializado');
    }
    
    initElements() {
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
        
        // Elementos do Assistente Neuro - REMOVIDO
        // this.elements.toggleNeuroAssistant = document.getElementById('toggleNeuroAssistant');
        // this.elements.neuroStatus = document.getElementById('neuroStatus');
        
        // Elementos de status
        this.elements.translationStatus = document.getElementById('translationStatus');
        this.elements.processingTime = document.getElementById('processingTime');
    }
    
    initEventListeners() {
        // Tradução
        this.elements.translateBtn.addEventListener('click', () => this.translateText());
        this.elements.swapLanguages.addEventListener('click', () => this.swapLanguages());
        this.elements.sourceText.addEventListener('input', () => this.onTextInput());
        
        // Fala
        this.elements.toggleSpeech.addEventListener('click', () => this.toggleSpeech());
        
        // Assistente Neuro - REMOVIDO
        /*
        if (this.elements.toggleNeuroAssistant) {
            console.log('✅ Botão Neuro Assistant encontrado, adicionando event listener');
            this.elements.toggleNeuroAssistant.addEventListener('click', () => {
                console.log('🔘 Clique no botão Neuro detectado!');
                this.toggleNeuroAssistant();
            });
        } else {
            console.error('❌ Botão toggleNeuroAssistant não encontrado!');
        }
        */
        
        // Controles
        this.elements.clearText.addEventListener('click', () => this.clearText());
        this.elements.copyTranslation.addEventListener('click', () => this.copyTranslation());
        this.elements.clearHistory.addEventListener('click', () => this.clearHistory());
        
        // Controles de voz
        const repeatSpeechBtn = document.getElementById('repeatSpeech');
        if (repeatSpeechBtn) {
            repeatSpeechBtn.addEventListener('click', () => this.repeatLastTranslation());
        }
        
        const voiceGenderSelect = document.getElementById('voiceGender');
        if (voiceGenderSelect) {
            voiceGenderSelect.addEventListener('change', (e) => {
                console.log('🎤 Gênero de voz alterado para:', e.target.value);
                this.saveSettings();
            });
        }
        
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
    
    
    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    checkMobileCompatibility() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const isSecure = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        
        if (isMobile && !isSecure) {
            this.showMobileSecurityWarning();
            return false;
        }
        
        return true;
    }
    
    showMobileSecurityWarning() {
        const warning = document.createElement('div');
        warning.className = 'mobile-security-warning';
        warning.innerHTML = `
            <div class="warning-content">
                <i class="fas fa-mobile-alt"></i>
                <h3>Dispositivo Móvel Detectado</h3>
                <p>O reconhecimento de voz requer HTTPS em dispositivos móveis.</p>
                <p>Para usar esta funcionalidade, acesse via HTTPS.</p>
                <button onclick="this.parentElement.parentElement.remove()">Entendi</button>
            </div>
        `;
        document.body.appendChild(warning);
    }
    
    checkBrowserSupport() {
        // Verificação específica para Edge Mobile
        if (isEdgeMobile() && !handleEdgeMobileFallback()) {
            return false;
        }
        // Verificar suporte à câmera
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
        
        // Verificar suporte a Speech Synthesis
        if ('speechSynthesis' in window) {
            console.log('✅ Síntese de voz suportada');
            this.loadAvailableVoices();
        } else {
            console.warn('⚠️ Síntese de voz não suportada');
        }
    }
    
    loadAvailableVoices() {
        // Aguardar carregamento das vozes
        const loadVoices = () => {
            const voices = speechSynthesis.getVoices();
            if (voices.length > 0) {
                console.log('🎯 Vozes disponíveis:', voices.length);
                voices.forEach(voice => {
                    console.log(`- ${voice.name} (${voice.lang})`);
                });
            }
        };
        
        // Carregar vozes imediatamente se disponíveis
        loadVoices();
        
        // Aguardar evento de carregamento das vozes (alguns navegadores)
        speechSynthesis.onvoiceschanged = loadVoices;
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
        
        // Configurações otimizadas para Samsung Internet
        this.speech.recognition.continuous = false;
        this.speech.recognition.interimResults = false;
        this.speech.recognition.maxAlternatives = 1;
        this.speech.recognition.lang = this.getLanguageCode(this.elements.sourceLanguage.value);
        
        // Configurações específicas para mobile com melhor tratamento de erros
        this.speech.recognition.onstart = () => {
            console.log('🎤 Reconhecimento de fala iniciado');
            this.elements.speechStatus.textContent = '🎤 Reconhecimento: Ouvindo...';
            this.elements.toggleSpeech.classList.add('active');
            this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone-alt"></i> Ouvindo...';
        };
        
        this.speech.recognition.onresult = async (event) => {
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                }
            }
            
            if (finalTranscript) {
                console.log('🎤 Texto reconhecido:', finalTranscript);
                this.elements.sourceText.value += finalTranscript + ' ';
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Texto capturado!';
                
                if (this.translation.autoTranslate) {
                    await this.translateTextWithSpeech();
                }
                
                // Parar o reconhecimento após capturar o texto
                this.stopSpeech();
            }
        };
        
        this.speech.recognition.onerror = (event) => {
            console.error('❌ Erro no reconhecimento de fala:', event.error);
            
            let errorMessage = '';
            
            switch(event.error) {
                case 'network':
                    errorMessage = 'Erro de rede. Verifique sua conexão.';
                    break;
                case 'not-allowed':
                    errorMessage = 'Permissão negada. Permita o acesso ao microfone.';
                    break;
                case 'no-speech':
                    errorMessage = 'Nenhuma fala detectada. Tente falar mais alto.';
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
            this.stopSpeech();
        };
        
        this.speech.recognition.onend = () => {
            console.log('🔄 Reconhecimento de fala finalizado');
            
            // Só atualizar status se não estiver mais ativo
            if (!this.speech.active) {
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Desativado';
                this.elements.toggleSpeech.classList.remove('active');
                this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone"></i> Falar';
            } else {
                // Se ainda está ativo, significa que terminou naturalmente
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Pronto para ouvir';
                this.speech.active = false;
                this.elements.toggleSpeech.classList.remove('active');
                this.elements.toggleSpeech.innerHTML = '<i class="fas fa-microphone"></i> Falar';
            }
        };
    }
    
    showMobilePermissionHelp(errorType) {
        // Evitar múltiplos avisos
        if (document.getElementById('mobilePermissionHelp')) {
            return;
        }
        
        let helpMessage = '';
        let instructions = '';
        
        switch(errorType) {
            case 'not-allowed':
                helpMessage = 'Permissão de Microfone Negada';
                instructions = `
                    <p><strong>Para permitir o acesso ao microfone:</strong></p>
                    <ul>
                        <li><strong>Safari (iOS):</strong> Toque no ícone "aA" na barra de endereços → Configurações do Site → Microfone → Permitir</li>
                        <li><strong>Chrome (Android):</strong> Toque no ícone do cadeado → Permissões → Microfone → Permitir</li>
                        <li><strong>Firefox:</strong> Toque no ícone do escudo → Permissões → Microfone → Permitir</li>
                    </ul>
                    <p>Após alterar as permissões, recarregue a página.</p>
                `;
                break;
            case 'audio-capture':
                helpMessage = 'Problema com o Microfone';
                instructions = `
                    <p><strong>Verifique:</strong></p>
                    <ul>
                        <li>Se o microfone não está sendo usado por outro aplicativo</li>
                        <li>Se o microfone não está silenciado nas configurações do dispositivo</li>
                        <li>Tente fechar outros aplicativos que podem estar usando o microfone</li>
                    </ul>
                `;
                break;
            case 'service-not-allowed':
                helpMessage = 'HTTPS Necessário';
                instructions = `
                    <p><strong>O reconhecimento de voz requer uma conexão segura (HTTPS).</strong></p>
                    <p>Certifique-se de que está acessando o site via HTTPS ou localhost.</p>
                `;
                break;
        }
        
        const helpDialog = document.createElement('div');
        helpDialog.id = 'mobilePermissionHelp';
        helpDialog.className = 'mobile-permission-help';
        helpDialog.innerHTML = `
            <div class="help-content">
                <div class="help-header">
                    <i class="fas fa-mobile-alt"></i>
                    <h3>${helpMessage}</h3>
                </div>
                <div class="help-body">
                    ${instructions}
                </div>
                <div class="help-footer">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="btn-help-close">
                        Entendi
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(helpDialog);
        
        // Auto-remover após 15 segundos
        setTimeout(() => {
            if (document.getElementById('mobilePermissionHelp')) {
                document.getElementById('mobilePermissionHelp').remove();
            }
        }, 15000);
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
            this.speech.active = true;
            this.elements.speechStatus.textContent = '🎤 Reconhecimento: Iniciando...';
            
            // Configurar idioma atual
            this.speech.recognition.lang = this.getLanguageCode(this.elements.sourceLanguage.value);
            
            // Iniciar reconhecimento diretamente (sem getUserMedia primeiro)
            this.speech.recognition.start();
            
        } catch (error) {
            console.error('❌ Erro ao iniciar reconhecimento:', error);
            
            let errorMessage = `Erro ao iniciar reconhecimento: ${error.message}`;
            this.elements.speechStatus.textContent = `❌ ${errorMessage}`;
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
    
    async translateTextWithSpeech() {
        const sourceText = this.elements.sourceText.value.trim();
        if (!sourceText) {
            return;
        }
        
        const sourceLang = this.elements.sourceLanguage.value;
        const targetLang = this.elements.targetLanguage.value;
        
        if (sourceLang === targetLang) {
            return;
        }
        
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
            
            // Falar a tradução automaticamente
            this.speakTranslation(translation, targetLang);
            
        } catch (error) {
            console.error('❌ Erro na tradução:', error);
            this.elements.translationStatus.textContent = 'Erro na tradução';
            this.elements.targetText.value = 'Erro: Não foi possível traduzir o texto.';
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
        // Ativar fala automaticamente
        if (!this.speech.active && this.speech.supported) {
            this.startSpeech();
        }
    }
    
    stopLiveMode() {
        console.log('⏹️ Modo ao vivo desativado');
        // Manter fala como está, apenas desativar modo automático
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
            'fr': 'fr-FR',
            'de': 'de-DE',
            'zh': 'zh-CN'
        };
        return codes[lang] || 'pt-BR';
    }
    
    getLanguageName(code) {
        const names = {
            'pt': '🇧🇷 Português',
            'en': '🇺🇸 Inglês',
            'es': '🇪🇸 Espanhol',
            'fr': '🇫🇷 Francês',
            'de': '🇩🇪 Alemão',
            'zh': '🇨🇳 Chinês'
        };
        return names[code] || code;
    }
    
    saveSettings() {
        const voiceGenderSelect = document.getElementById('voiceGender');
        const settings = {
            autoTranslate: this.translation.autoTranslate,
            liveMode: this.translation.liveMode,
            history: this.translation.history,
            sourceLanguage: this.elements.sourceLanguage.value,
            targetLanguage: this.elements.targetLanguage.value,
            voiceGender: voiceGenderSelect ? voiceGenderSelect.value : 'auto'
        };
        
        localStorage.setItem('neurotranslator-settings', JSON.stringify(settings));
    }
    
    loadSettings() {
        try {
            const settings = localStorage.getItem('neuroTranslatorSettings');
            if (settings) {
                const parsed = JSON.parse(settings);
                this.translation.autoTranslate = parsed.autoTranslate !== false;
                this.translation.liveMode = parsed.liveMode === true;
                
                // Aplicar configurações aos elementos
                if (this.elements.autoTranslate) {
                    this.elements.autoTranslate.checked = this.translation.autoTranslate;
                }
                if (this.elements.liveMode) {
                    this.elements.liveMode.checked = this.translation.liveMode;
                }
                
                // Aplicar configuração de gênero de voz
                const voiceGenderSelect = document.getElementById('voiceGender');
                if (voiceGenderSelect && parsed.voiceGender) {
                    voiceGenderSelect.value = parsed.voiceGender;
                }
                
                console.log('⚙️ Configurações carregadas:', parsed);
            }
        } catch (error) {
            console.error('❌ Erro ao carregar configurações:', error);
        }
    }
    
    // Métodos do Assistente Neuro
    toggleNeuroAssistant() {
        console.log('🔄 toggleNeuroAssistant chamado, estado atual:', this.neuroAssistant.active);
        console.log('🔍 Elementos disponíveis:', {
            toggleButton: !!this.elements.toggleNeuroAssistant,
            statusElement: !!this.elements.neuroStatus
        });
        
        if (this.neuroAssistant.active) {
            this.stopNeuroAssistant();
        } else {
            this.startNeuroAssistant();
        }
    }
    
    async startNeuroAssistant() {
        try {
            console.log('🤖 Iniciando Assistente Neuro...');
            console.log('🔍 Verificando elementos:', {
                toggleButton: this.elements.toggleNeuroAssistant,
                statusElement: this.elements.neuroStatus
            });
            
            // Verificar se os elementos existem
            if (!this.elements.toggleNeuroAssistant || !this.elements.neuroStatus) {
                console.error('❌ Elementos do Neuro Assistant não encontrados!');
                alert('❌ Erro: Elementos da interface não encontrados');
                return;
            }
            
            // Verificar protocolo de segurança
            const isSecure = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
            console.log('🔒 Protocolo seguro:', isSecure, 'Protocol:', location.protocol, 'Host:', location.hostname);
            
            if (!isSecure) {
                console.warn('⚠️ Protocolo não seguro detectado');
                alert('⚠️ O Assistente Neuro pode não funcionar corretamente sem HTTPS. Tente acessar via localhost.');
            }
            
            // Verificar suporte a reconhecimento de voz
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                console.error('❌ Reconhecimento de voz não suportado');
                alert('❌ Reconhecimento de voz não suportado neste navegador');
                return;
            }
            
            // Solicitar permissão do microfone explicitamente
            try {
                console.log('🎤 Solicitando permissão do microfone...');
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log('✅ Permissão do microfone concedida');
                stream.getTracks().forEach(track => track.stop()); // Parar o stream
            } catch (micError) {
                console.error('❌ Erro ao acessar microfone:', micError);
                alert('❌ Erro ao acessar o microfone. Verifique as permissões do navegador.');
                return;
            }
            
            // Resetar contador de tentativas de reconexão
        this.neuroReconnectAttempts = 0;
        
        // Remover modo fallback se estiver ativo
        this.removeNeuroFallback();
            
            // Inicializar reconhecimento de voz para wake word
            this.initNeuroSpeechRecognition();
            
            this.neuroAssistant.active = true;
            this.neuroAssistant.listening = true;
            
            // Atualizar interface
            this.elements.toggleNeuroAssistant.classList.add('active');
            this.elements.toggleNeuroAssistant.innerHTML = '<i class="fas fa-robot"></i><span>Neuro Ativo</span>';
            this.elements.neuroStatus.textContent = '🤖 Neuro: Ouvindo "Vamos, Neuro!"';
            
            console.log('✅ Assistente Neuro ativado com sucesso');
            
        } catch (error) {
            console.error('❌ Erro ao iniciar Assistente Neuro:', error);
            alert('Erro ao ativar o Assistente Neuro: ' + error.message);
        }
    }
    
    stopNeuroAssistant() {
        console.log('🤖 Parando Assistente Neuro...');
        
        if (this.neuroSpeechRecognition) {
            this.neuroSpeechRecognition.stop();
        }
        
        this.neuroAssistant.active = false;
        this.neuroAssistant.listening = false;
        this.neuroAssistant.wakeWordDetected = false;
        
        // Atualizar interface
        this.elements.toggleNeuroAssistant.classList.remove('active');
        this.elements.toggleNeuroAssistant.innerHTML = '<i class="fas fa-robot"></i><span>Assistente Neuro</span>';
        this.elements.neuroStatus.textContent = '🤖 Neuro: Desativado';
        
        console.log('✅ Assistente Neuro desativado');
    }
    
    initNeuroSpeechRecognition() {
        try {
            console.log('🎤 Inicializando reconhecimento de voz do Neuro...');
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.neuroSpeechRecognition = new SpeechRecognition();
            
            this.neuroSpeechRecognition.continuous = true;
            this.neuroSpeechRecognition.interimResults = true;
            this.neuroSpeechRecognition.lang = 'pt-BR';
            
            this.neuroSpeechRecognition.onstart = () => {
                console.log('🎤 Neuro: Reconhecimento iniciado');
            };
            
            this.neuroSpeechRecognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                
                console.log('🎤 Neuro ouviu:', transcript);
                
                // Detectar wake word "Vamos, Neuro!"
                if (transcript.toLowerCase().includes('vamos neuro') || 
                    transcript.toLowerCase().includes('vamos, neuro')) {
                    this.onWakeWordDetected(transcript);
                }
            };
            
            this.neuroSpeechRecognition.onerror = (event) => {
                console.error('❌ Erro no reconhecimento Neuro:', event.error);
                
                if (event.error === 'not-allowed') {
                    alert('❌ Permissão de microfone negada para o Assistente Neuro');
                    this.stopNeuroAssistant();
                } else if (event.error === 'no-speech') {
                    console.log('⚠️ Nenhuma fala detectada, continuando...');
                } else if (event.error === 'network') {
                    console.warn('⚠️ Erro de rede no reconhecimento de voz. Tentando reconectar...');
                    // Não parar o assistente, apenas tentar reconectar
                    setTimeout(() => {
                        if (this.neuroAssistant.active && this.neuroAssistant.listening) {
                            try {
                                console.log('🔄 Tentando reconectar reconhecimento de voz...');
                                this.neuroSpeechRecognition.start();
                            } catch (restartError) {
                                console.error('❌ Erro ao reconectar:', restartError);
                            }
                        }
                    }, 2000);
                } else if (event.error === 'service-not-allowed') {
                    console.error('❌ Serviço de reconhecimento não permitido');
                    alert('❌ Serviço de reconhecimento de voz não está disponível. Verifique sua conexão com a internet.');
                    this.stopNeuroAssistant();
                } else {
                    console.error('❌ Erro de reconhecimento:', event.error);
                    // Para outros erros, tentar reconectar após um delay
                    setTimeout(() => {
                        if (this.neuroAssistant.active && this.neuroAssistant.listening) {
                            try {
                                this.neuroSpeechRecognition.start();
                            } catch (restartError) {
                                console.error('❌ Erro ao reiniciar após erro:', restartError);
                            }
                        }
                    }, 1000);
                }
            };
            
            this.neuroSpeechRecognition.onend = () => {
                console.log('🎤 Reconhecimento Neuro finalizado');
                if (this.neuroAssistant.active && this.neuroAssistant.listening) {
                    // Reiniciar reconhecimento se ainda estiver ativo
                    console.log('🔄 Reiniciando reconhecimento Neuro...');
                    setTimeout(() => {
                        if (this.neuroAssistant.active && this.neuroAssistant.listening) {
                            try {
                                this.neuroSpeechRecognition.start();
                            } catch (error) {
                                console.error('❌ Erro ao reiniciar reconhecimento:', error);
                                // Se falhar várias vezes, mostrar aviso ao usuário
                                if (!this.neuroReconnectAttempts) {
                                    this.neuroReconnectAttempts = 0;
                                }
                                this.neuroReconnectAttempts++;
                                
                                if (this.neuroReconnectAttempts > 3) {
                                    console.warn('⚠️ Muitas tentativas de reconexão falharam');
                                    this.elements.neuroStatus.textContent = '🤖 Neuro: Problemas de conectividade - Clique para reativar';
                                    this.neuroAssistant.listening = false;
                                    // Mostrar modo fallback
                                    this.showNeuroFallback();
                                } else {
                                    // Tentar novamente após um delay maior
                                    setTimeout(() => {
                                        if (this.neuroAssistant.active) {
                                            try {
                                                this.neuroSpeechRecognition.start();
                                            } catch (retryError) {
                                                console.error('❌ Erro na nova tentativa:', retryError);
                                            }
                                        }
                                    }, 3000);
                                }
                            }
                        }
                    }, 100);
                }
            };
            
            console.log('🎤 Iniciando reconhecimento de voz...');
            this.neuroSpeechRecognition.start();
            
        } catch (error) {
            console.error('❌ Erro ao inicializar reconhecimento Neuro:', error);
            throw error;
        }
    }
    
    onWakeWordDetected(transcript) {
        console.log('🎯 Wake word detectada!');
        this.neuroAssistant.wakeWordDetected = true;
        
        // Atualizar status
        this.elements.neuroStatus.textContent = '🤖 Neuro: Wake word detectada! Processando comando...';
        
        // Processar comando após wake word
        this.processNeuroCommand(transcript);
    }
    
    async processNeuroCommand(fullTranscript) {
        try {
            console.log('🧠 Processando comando Neuro:', fullTranscript);
            
            // Extrair comando após "Vamos, Neuro!"
            const wakeWordIndex = fullTranscript.toLowerCase().search(/(vamos,?\s*neuro)/);
            if (wakeWordIndex === -1) return;
            
            const commandPart = fullTranscript.substring(wakeWordIndex).replace(/(vamos,?\s*neuro[!.]?\s*)/i, '').trim();
            
            if (!commandPart) {
                this.elements.neuroStatus.textContent = '🤖 Neuro: Aguardando comando...';
                return;
            }
            
            console.log('📝 Comando extraído:', commandPart);
            
            // Detectar idioma de destino e texto para traduzir
            const translationMatch = this.parseTranslationCommand(commandPart);
            
            if (translationMatch) {
                await this.executeNeuroTranslation(translationMatch);
            } else {
                this.elements.neuroStatus.textContent = '🤖 Neuro: Comando não reconhecido';
                console.log('❓ Comando não reconhecido:', commandPart);
            }
            
        } catch (error) {
            console.error('❌ Erro ao processar comando Neuro:', error);
            this.elements.neuroStatus.textContent = '🤖 Neuro: Erro ao processar comando';
        }
        
        // Resetar para ouvir novamente
        setTimeout(() => {
            if (this.neuroAssistant.active) {
                this.neuroAssistant.wakeWordDetected = false;
                this.elements.neuroStatus.textContent = '🤖 Neuro: Ouvindo "Vamos, Neuro!"';
            }
        }, 3000);
    }
    
    parseTranslationCommand(command) {
        // Padrões para detectar comandos de tradução
        const patterns = [
            /traduza?\s+para\s+o?\s*(inglês|english)\s+a?\s*frase[:\s]*(.*)/i,
            /traduza?\s+para\s+o?\s*(português|portuguese)\s+a?\s*frase[:\s]*(.*)/i,
            /traduza?\s+para\s+o?\s*(espanhol|spanish)\s+a?\s*frase[:\s]*(.*)/i,
            /traduza?\s+para\s+o?\s*(francês|french)\s+a?\s*frase[:\s]*(.*)/i,
            /translate\s+to\s+(portuguese|português|english|inglês|spanish|espanhol|french|francês)[:\s]*(.*)/i
        ];
        
        for (const pattern of patterns) {
            const match = command.match(pattern);
            if (match) {
                const targetLang = this.getLanguageCodeFromName(match[1]);
                const textToTranslate = match[2].trim();
                
                if (targetLang && textToTranslate) {
                    return {
                        targetLanguage: targetLang,
                        text: textToTranslate
                    };
                }
            }
        }
        
        return null;
    }
    
    getLanguageCodeFromName(langName) {
        const langMap = {
            'inglês': 'en',
            'english': 'en',
            'português': 'pt',
            'portuguese': 'pt',
            'espanhol': 'es',
            'spanish': 'es',
            'francês': 'fr',
            'french': 'fr',
            'alemão': 'de',
            'german': 'de',
            'chinês': 'zh',
            'chinese': 'zh'
        };
        
        return langMap[langName.toLowerCase()] || null;
    }
    
    async executeNeuroTranslation(translationData) {
        try {
            console.log('🔄 Executando tradução Neuro:', translationData);
            
            // Detectar idioma do texto original
            const sourceLang = this.detectLanguage(translationData.text);
            
            // Atualizar campos da interface
            this.elements.sourceText.value = translationData.text;
            this.elements.sourceLanguage.value = sourceLang;
            this.elements.targetLanguage.value = translationData.targetLanguage;
            
            // Atualizar status
            this.elements.neuroStatus.textContent = '🤖 Neuro: Traduzindo...';
            
            // Executar tradução
            await this.translateText();
            
            // Falar a tradução
            if (this.elements.targetText.value) {
                this.speakTranslation(this.elements.targetText.value, translationData.targetLanguage);
            }
            
            this.elements.neuroStatus.textContent = '🤖 Neuro: Tradução concluída!';
            
        } catch (error) {
            console.error('❌ Erro na tradução Neuro:', error);
            this.elements.neuroStatus.textContent = '🤖 Neuro: Erro na tradução';
        }
    }
    
    detectLanguage(text) {
        // Detecção simples baseada em padrões
        const portugueseWords = ['o', 'a', 'de', 'para', 'com', 'em', 'um', 'uma', 'que', 'não', 'é', 'do', 'da'];
        const englishWords = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for'];
        const spanishWords = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo'];
        
        const words = text.toLowerCase().split(/\s+/);
        
        let ptScore = 0, enScore = 0, esScore = 0;
        
        words.forEach(word => {
            if (portugueseWords.includes(word)) ptScore++;
            if (englishWords.includes(word)) enScore++;
            if (spanishWords.includes(word)) esScore++;
        });
        
        if (ptScore > enScore && ptScore > esScore) return 'pt';
        if (enScore > ptScore && enScore > esScore) return 'en';
        if (esScore > ptScore && esScore > enScore) return 'es';
        
        return 'pt'; // Default para português
    }
    
    // Sistema de vozes fixas para garantir consistência entre sistemas
    getFixedVoice(language, gender) {
        const voices = speechSynthesis.getVoices();
        
        // Configuração de vozes fixas por idioma e gênero
        const fixedVoices = {
            'pt': {
                'male': ['Microsoft Daniel - Portuguese (Brazil)', 'Google português do Brasil', 'Daniel', 'Ricardo'],
                'female': ['Microsoft Maria - Portuguese (Brazil)', 'Google português do Brasil', 'Maria', 'Fernanda', 'Luciana']
            },
            'en': {
                'male': ['Microsoft David - English (United States)', 'Google US English', 'David', 'Mark', 'Alex'],
                'female': ['Microsoft Zira - English (United States)', 'Google US English', 'Zira', 'Samantha', 'Victoria']
            },
            'es': {
                'male': ['Microsoft Pablo - Spanish (Spain)', 'Google español', 'Pablo', 'Diego', 'Carlos'],
                'female': ['Microsoft Helena - Spanish (Spain)', 'Google español', 'Helena', 'Paloma', 'Monica']
            },
            'fr': {
                'male': ['Microsoft Paul - French (France)', 'Google français', 'Paul', 'Thomas'],
                'female': ['Microsoft Hortense - French (France)', 'Google français', 'Hortense', 'Amelie']
            },
            'de': {
                'male': ['Microsoft Stefan - German (Germany)', 'Google Deutsch', 'Stefan', 'Hans'],
                'female': ['Microsoft Hedda - German (Germany)', 'Google Deutsch', 'Hedda', 'Anna']
            },
            'zh': {
                'male': ['Microsoft Kangkang - Chinese (Simplified, PRC)', 'Google 普通话（中国大陆）', 'Kangkang'],
                'female': ['Microsoft Yaoyao - Chinese (Simplified, PRC)', 'Google 普通话（中国大陆）', 'Yaoyao', 'Ting-Ting']
            }
        };

        const targetLang = this.getLanguageCode(language);
        const voiceOptions = fixedVoices[language];
        
        if (!voiceOptions) {
            return null;
        }

        const genderVoices = voiceOptions[gender] || voiceOptions['female'];
        
        // Tentar encontrar uma voz específica da lista
        for (const voiceName of genderVoices) {
            const voice = voices.find(v => 
                v.name.includes(voiceName) || 
                (v.lang === targetLang && v.name.toLowerCase().includes(voiceName.toLowerCase()))
            );
            if (voice) {
                return voice;
            }
        }

        // Fallback: procurar qualquer voz do idioma com indicadores de gênero
        const genderKeywords = {
            'male': ['male', 'masculin', 'homem', 'man', 'hombre', 'homme', 'mann', '男'],
            'female': ['female', 'feminin', 'mulher', 'woman', 'mujer', 'femme', 'frau', '女']
        };

        const keywords = genderKeywords[gender] || genderKeywords['female'];
        
        for (const keyword of keywords) {
            const voice = voices.find(v => 
                (v.lang === targetLang || v.lang.startsWith(language)) &&
                v.name.toLowerCase().includes(keyword)
            );
            if (voice) {
                return voice;
            }
        }

        // Último fallback: primeira voz disponível do idioma
        return voices.find(v => v.lang === targetLang || v.lang.startsWith(language));
    }

    speakTranslation(text, language, forceGender = null) {
        if ('speechSynthesis' in window) {
            // Parar qualquer síntese anterior
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Configurar idioma para síntese de voz
            const voiceLangMap = {
                'pt': 'pt-BR',
                'en': 'en-US',
                'es': 'es-ES',
                'fr': 'fr-FR',
                'de': 'de-DE',
                'zh': 'zh-CN'
            };
            
            utterance.lang = voiceLangMap[language] || 'pt-BR';
            utterance.rate = 0.9;
            utterance.volume = 1;
            
            // Obter preferência de gênero de voz
            const voiceGenderSelect = document.getElementById('voiceGender');
            const selectedGender = forceGender || (voiceGenderSelect ? voiceGenderSelect.value : 'auto');
            
            // Usar sistema de vozes fixas
            let selectedVoice = null;
            
            if (selectedGender === 'auto') {
                // No modo automático, alternar entre masculino e feminino
                const autoGender = Math.random() > 0.5 ? 'male' : 'female';
                selectedVoice = this.getFixedVoice(language, autoGender);
                utterance.pitch = autoGender === 'male' ? 0.8 : 1.2;
            } else {
                selectedVoice = this.getFixedVoice(language, selectedGender);
                utterance.pitch = selectedGender === 'male' ? 0.8 : 1.2;
            }
            
            if (selectedVoice) {
                utterance.voice = selectedVoice;
                console.log('🎯 Voz fixa selecionada:', selectedVoice.name, selectedVoice.lang, `(${selectedGender})`);
            } else {
                console.warn('⚠️ Nenhuma voz encontrada para', language, selectedGender);
            }
            
            // Armazenar última tradução para repetição
            this.lastTranslation = {
                text: text,
                language: language,
                gender: selectedGender
            };
            
            // Eventos de controle
            utterance.onstart = () => {
                console.log('🔊 Iniciando síntese de voz:', text);
                this.elements.speechStatus.textContent = '🔊 Falando tradução...';
                
                // Desabilitar botão de repetir durante a fala
                const repeatBtn = document.getElementById('repeatSpeech');
                if (repeatBtn) {
                    repeatBtn.disabled = true;
                    repeatBtn.style.opacity = '0.6';
                }
            };
            
            utterance.onend = () => {
                console.log('✅ Síntese de voz concluída');
                this.elements.speechStatus.textContent = '🎤 Reconhecimento: Pronto';
                
                // Reabilitar botão de repetir
                const repeatBtn = document.getElementById('repeatSpeech');
                if (repeatBtn) {
                    repeatBtn.disabled = false;
                    repeatBtn.style.opacity = '1';
                }
            };
            
            utterance.onerror = (event) => {
                console.error('❌ Erro na síntese de voz:', event.error);
                this.elements.speechStatus.textContent = '❌ Erro na síntese de voz';
                
                // Reabilitar botão de repetir em caso de erro
                const repeatBtn = document.getElementById('repeatSpeech');
                if (repeatBtn) {
                    repeatBtn.disabled = false;
                    repeatBtn.style.opacity = '1';
                }
            };
            
            console.log('🔊 Falando tradução:', text);
            speechSynthesis.speak(utterance);
        } else {
            console.warn('⚠️ Speech Synthesis não suportado');
            this.elements.speechStatus.textContent = '⚠️ Síntese de voz não suportada';
        }
    }
    
    // Método para repetir a última tradução
    repeatLastTranslation() {
        if (this.lastTranslation && this.lastTranslation.text) {
            console.log('🔄 Repetindo última tradução');
            this.speakTranslation(
                this.lastTranslation.text, 
                this.lastTranslation.language, 
                this.lastTranslation.gender
            );
        } else {
            console.warn('⚠️ Nenhuma tradução disponível para repetir');
            this.elements.speechStatus.textContent = '⚠️ Nenhuma tradução para repetir';
        }
    }
    
    // Método de fallback para problemas de conectividade
    showNeuroFallback() {
        console.log('🔄 Ativando modo fallback do Neuro');
        
        if (this.elements.neuroStatus) {
            this.elements.neuroStatus.innerHTML = `
                🤖 Neuro: Problemas de conectividade detectados<br>
                <small style="color: #666;">Clique no botão para reativar ou use o modo manual</small>
            `;
        }
        
        // Mostrar opção de entrada manual
        const fallbackDiv = document.createElement('div');
        fallbackDiv.id = 'neuro-fallback';
        fallbackDiv.style.cssText = `
            margin-top: 10px;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 5px;
            border-left: 4px solid #ff6b6b;
        `;
        
        fallbackDiv.innerHTML = `
            <div style="margin-bottom: 10px;">
                <strong>🔧 Modo Manual do Neuro</strong>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <input type="text" id="neuro-manual-input" placeholder="Digite seu comando aqui..." 
                       style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <button id="neuro-manual-send" style="padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Enviar
                </button>
            </div>
            <div style="margin-top: 5px; font-size: 12px; color: #666;">
                Exemplo: "traduzir hello para português"
            </div>
        `;
        
        // Remover fallback anterior se existir
        const existingFallback = document.getElementById('neuro-fallback');
        if (existingFallback) {
            existingFallback.remove();
        }
        
        // Adicionar após o status do Neuro
        if (this.elements.neuroStatus && this.elements.neuroStatus.parentNode) {
            this.elements.neuroStatus.parentNode.insertBefore(fallbackDiv, this.elements.neuroStatus.nextSibling);
            
            // Configurar eventos do modo manual
            const manualInput = document.getElementById('neuro-manual-input');
            const manualSend = document.getElementById('neuro-manual-send');
            
            const sendManualCommand = () => {
                const command = manualInput.value.trim();
                if (command) {
                    console.log('📝 Comando manual do Neuro:', command);
                    this.processNeuroCommand(command);
                    manualInput.value = '';
                }
            };
            
            manualSend.addEventListener('click', sendManualCommand);
            manualInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendManualCommand();
                }
            });
        }
    }
    
    // Remover modo fallback
    removeNeuroFallback() {
        const fallbackDiv = document.getElementById('neuro-fallback');
        if (fallbackDiv) {
            fallbackDiv.remove();
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

function isSamsungInternet() {
    const userAgent = navigator.userAgent.toLowerCase();
    return userAgent.includes('samsungbrowser') || 
           userAgent.includes('samsung') ||
           (userAgent.includes('android') && userAgent.includes('wv'));
}


// Configuração específica para Samsung Internet
function configureSamsungSpeechRecognition(recognition) {
    if (isSamsungInternet()) {
        recognition.continuous = false; // Samsung Internet tem problemas com continuous=true
        recognition.interimResults = false; // Desabilitar resultados intermediários
        recognition.maxAlternatives = 1;
        
        // Timeout personalizado para Samsung
        let samsungTimeout;
        recognition.onstart = function() {
            samsungTimeout = setTimeout(() => {
                recognition.stop();
                console.log('Samsung timeout aplicado');
            }, 10000); // 10 segundos timeout
        };
        
        recognition.onend = function() {
            if (samsungTimeout) clearTimeout(samsungTimeout);
        };
    }
}


function ensureUserInteractionForSamsung() {
    if (isSamsungInternet()) {
        // Samsung Internet requer interação do usuário
        document.addEventListener('touchstart', function samsungTouchHandler() {
            window.samsungUserInteracted = true;
            document.removeEventListener('touchstart', samsungTouchHandler);
        }, { once: true });
        
        // Aguardar interação antes de iniciar reconhecimento
        return new Promise((resolve) => {
            if (window.samsungUserInteracted) {
                resolve();
            } else {
                const checkInteraction = setInterval(() => {
                    if (window.samsungUserInteracted) {
                        clearInterval(checkInteraction);
                        resolve();
                    }
                }, 100);
            }
        });
    }
    return Promise.resolve();
}


function isEdgeMobile() {
    const userAgent = navigator.userAgent.toLowerCase();
    return userAgent.includes('edg/') && userAgent.includes('mobile');
}


function handleEdgeMobileFallback() {
    if (isEdgeMobile()) {
        // Verificar se Speech Recognition está disponível
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech Recognition não disponível no Edge Mobile');
            showTextInputFallback();
            return false;
        }
        
        // Verificar permissões de microfone
        if (navigator.permissions) {
            navigator.permissions.query({name: 'microphone'}).then(function(result) {
                if (result.state === 'denied') {
                    showMicrophonePermissionError();
                }
            });
        }
    }
    return true;
}


function handleEdgeSpecificErrors(event) {
    if (isEdgeMobile()) {
        console.log('Edge Mobile - Erro específico:', event.error);
        
        switch(event.error) {
            case 'not-allowed':
                showEdgePermissionHelp();
                break;
            case 'service-not-allowed':
                showEdgeServiceError();
                break;
            case 'network':
                showEdgeNetworkError();
                break;
            default:
                showEdgeGenericError(event.error);
        }
    }
}