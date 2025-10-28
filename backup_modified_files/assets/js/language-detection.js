// NeuroTranslator Language Detection Module
// Módulo avançado de detecção automática de idiomas
// Implementa algoritmos de Machine Learning para identificação precisa

class NeuroLanguageDetector {
    constructor() {
        this.isInitialized = false;
        this.models = {
            ngramModel: null,
            frequencyModel: null,
            patternModel: null
        };
        
        // Base de dados linguísticos
        this.languageProfiles = {
            'pt': {
                name: 'Português',
                code: 'pt-BR',
                commonWords: [
                    'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 
                    'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais',
                    'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à',
                    'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está',
                    'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era',
                    'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas', 'numa', 'nem', 'suas'
                ],
                patterns: [
                    /ção$/, /mente$/, /ando$/, /endo$/, /indo$/, /ado$/, /ido$/, /oso$/, /osa$/,
                    /^des/, /^re/, /^pre/, /^anti/, /^contra/, /nh/, /lh/, /ão$/, /ões$/
                ],
                trigrams: [
                    'que', 'ent', 'men', 'est', 'par', 'com', 'con', 'des', 'pro', 'pre',
                    'ant', 'int', 'res', 'ter', 'ado', 'ção', 'nte', 'sta', 'tra', 'ica'
                ],
                vowelPattern: /[aeiouáéíóúâêîôûãõ]/gi,
                consonantClusters: ['br', 'cr', 'dr', 'fr', 'gr', 'pr', 'tr', 'bl', 'cl', 'fl', 'gl', 'pl']
            },
            
            'en': {
                name: 'English',
                code: 'en-US',
                commonWords: [
                    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                    'this', 'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will',
                    'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
                    'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can'
                ],
                patterns: [
                    /ing$/, /ed$/, /er$/, /est$/, /ly$/, /tion$/, /sion$/, /ness$/, /ment$/,
                    /^un/, /^re/, /^pre/, /^dis/, /^mis/, /th/, /gh/, /ck/, /^wh/
                ],
                trigrams: [
                    'the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent',
                    'ion', 'ter', 'was', 'you', 'ith', 'ver', 'all', 'wit', 'thi', 'tio'
                ],
                vowelPattern: /[aeiou]/gi,
                consonantClusters: ['th', 'ch', 'sh', 'wh', 'ph', 'gh', 'ck', 'ng', 'st', 'nd']
            }
        };
        
        this.detectionHistory = [];
        this.confidenceThreshold = 0.7;
        
        this.init();
    }
    
    async init() {
        console.log('🧠 Inicializando NeuroLanguageDetector...');
        
        try {
            await this.buildNgramModel();
            await this.buildFrequencyModel();
            await this.buildPatternModel();
            
            this.isInitialized = true;
            console.log('✅ NeuroLanguageDetector inicializado com sucesso!');
            
        } catch (error) {
            console.error('❌ Erro ao inicializar detector de idiomas:', error);
        }
    }
    
    async buildNgramModel() {
        console.log('📊 Construindo modelo N-gram...');
        
        // Construir modelo baseado em trigramas
        this.models.ngramModel = {};
        
        Object.keys(this.languageProfiles).forEach(lang => {
            this.models.ngramModel[lang] = {
                trigrams: new Set(this.languageProfiles[lang].trigrams),
                score: 0
            };
        });
        
        console.log('✅ Modelo N-gram construído');
    }
    
    async buildFrequencyModel() {
        console.log('📈 Construindo modelo de frequência...');
        
        // Construir modelo baseado em frequência de palavras
        this.models.frequencyModel = {};
        
        Object.keys(this.languageProfiles).forEach(lang => {
            const words = this.languageProfiles[lang].commonWords;
            this.models.frequencyModel[lang] = new Map();
            
            words.forEach((word, index) => {
                // Peso inversamente proporcional à posição (palavras mais comuns têm peso maior)
                const weight = Math.max(1, words.length - index);
                this.models.frequencyModel[lang].set(word.toLowerCase(), weight);
            });
        });
        
        console.log('✅ Modelo de frequência construído');
    }
    
    async buildPatternModel() {
        console.log('🔍 Construindo modelo de padrões...');
        
        // Modelo baseado em padrões morfológicos e fonéticos
        this.models.patternModel = {};
        
        Object.keys(this.languageProfiles).forEach(lang => {
            this.models.patternModel[lang] = {
                patterns: this.languageProfiles[lang].patterns,
                vowelPattern: this.languageProfiles[lang].vowelPattern,
                consonantClusters: this.languageProfiles[lang].consonantClusters
            };
        });
        
        console.log('✅ Modelo de padrões construído');
    }
    
    // Método principal de detecção
    detectLanguage(text, options = {}) {
        if (!this.isInitialized) {
            console.warn('⚠️ Detector não inicializado');
            return { language: 'unknown', confidence: 0 };
        }
        
        if (!text || text.trim().length < 3) {
            return { language: 'unknown', confidence: 0 };
        }
        
        const cleanText = this.preprocessText(text);
        const scores = {};
        
        // Aplicar múltiplos algoritmos de detecção
        const ngramScores = this.analyzeNgrams(cleanText);
        const frequencyScores = this.analyzeWordFrequency(cleanText);
        const patternScores = this.analyzePatterns(cleanText);
        const statisticalScores = this.analyzeStatistics(cleanText);
        
        // Combinar scores com pesos
        Object.keys(this.languageProfiles).forEach(lang => {
            scores[lang] = (
                (ngramScores[lang] || 0) * 0.3 +
                (frequencyScores[lang] || 0) * 0.35 +
                (patternScores[lang] || 0) * 0.25 +
                (statisticalScores[lang] || 0) * 0.1
            );
        });
        
        // Encontrar idioma com maior score
        const detectedLang = Object.keys(scores).reduce((a, b) => 
            scores[a] > scores[b] ? a : b
        );
        
        const confidence = scores[detectedLang];
        const result = {
            language: detectedLang,
            confidence: confidence,
            scores: scores,
            details: {
                ngram: ngramScores,
                frequency: frequencyScores,
                pattern: patternScores,
                statistical: statisticalScores
            }
        };
        
        // Adicionar ao histórico
        this.addToHistory(text, result);
        
        console.log(`🎯 Idioma detectado: ${detectedLang} (${(confidence * 100).toFixed(1)}%)`);
        
        return result;
    }
    
    preprocessText(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\sáéíóúâêîôûãõç]/g, ' ') // Manter acentos portugueses
            .replace(/\s+/g, ' ')
            .trim();
    }
    
    analyzeNgrams(text) {
        const scores = {};
        const textTrigrams = this.extractTrigrams(text);
        
        Object.keys(this.languageProfiles).forEach(lang => {
            let matches = 0;
            const langTrigrams = this.models.ngramModel[lang].trigrams;
            
            textTrigrams.forEach(trigram => {
                if (langTrigrams.has(trigram)) {
                    matches++;
                }
            });
            
            scores[lang] = textTrigrams.length > 0 ? matches / textTrigrams.length : 0;
        });
        
        return scores;
    }
    
    extractTrigrams(text) {
        const trigrams = [];
        const cleanText = text.replace(/\s+/g, '');
        
        for (let i = 0; i <= cleanText.length - 3; i++) {
            trigrams.push(cleanText.substring(i, i + 3));
        }
        
        return trigrams;
    }
    
    analyzeWordFrequency(text) {
        const scores = {};
        const words = text.split(/\s+/).filter(word => word.length > 1);
        
        Object.keys(this.languageProfiles).forEach(lang => {
            let totalScore = 0;
            let wordCount = 0;
            
            words.forEach(word => {
                const weight = this.models.frequencyModel[lang].get(word.toLowerCase());
                if (weight) {
                    totalScore += weight;
                    wordCount++;
                }
            });
            
            scores[lang] = words.length > 0 ? (totalScore / words.length) / 100 : 0;
        });
        
        return scores;
    }
    
    analyzePatterns(text) {
        const scores = {};
        
        Object.keys(this.languageProfiles).forEach(lang => {
            const profile = this.languageProfiles[lang];
            let patternMatches = 0;
            let totalPatterns = profile.patterns.length;
            
            // Verificar padrões morfológicos
            profile.patterns.forEach(pattern => {
                if (pattern.test(text)) {
                    patternMatches++;
                }
            });
            
            // Verificar clusters consonantais
            let clusterMatches = 0;
            profile.consonantClusters.forEach(cluster => {
                const regex = new RegExp(cluster, 'gi');
                const matches = text.match(regex);
                if (matches) {
                    clusterMatches += matches.length;
                }
            });
            
            const patternScore = totalPatterns > 0 ? patternMatches / totalPatterns : 0;
            const clusterScore = Math.min(clusterMatches / 10, 1); // Normalizar
            
            scores[lang] = (patternScore + clusterScore) / 2;
        });
        
        return scores;
    }
    
    analyzeStatistics(text) {
        const scores = {};
        
        Object.keys(this.languageProfiles).forEach(lang => {
            const profile = this.languageProfiles[lang];
            
            // Análise de vogais
            const vowelMatches = text.match(profile.vowelPattern) || [];
            const vowelRatio = vowelMatches.length / text.length;
            
            // Análise de comprimento médio de palavras
            const words = text.split(/\s+/).filter(word => word.length > 0);
            const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length;
            
            // Scores baseados em características estatísticas conhecidas
            let statisticalScore = 0;
            
            if (lang === 'pt') {
                // Português tem mais vogais e palavras ligeiramente mais longas
                statisticalScore = (vowelRatio > 0.4 ? 0.6 : 0.2) + 
                                 (avgWordLength > 4.5 ? 0.4 : 0.1);
            } else if (lang === 'en') {
                // Inglês tem proporção diferente de vogais
                statisticalScore = (vowelRatio < 0.45 ? 0.6 : 0.2) + 
                                 (avgWordLength < 5 ? 0.4 : 0.1);
            }
            
            scores[lang] = Math.min(statisticalScore, 1);
        });
        
        return scores;
    }
    
    // Detecção em tempo real para áudio
    detectLanguageRealTime(audioTranscript, callback) {
        if (!audioTranscript || audioTranscript.length < 10) {
            return;
        }
        
        const result = this.detectLanguage(audioTranscript);
        
        if (result.confidence > this.confidenceThreshold) {
            callback(result);
        }
    }
    
    // Método para melhorar detecção com contexto
    detectWithContext(text, previousDetections = []) {
        const currentResult = this.detectLanguage(text);
        
        if (previousDetections.length === 0) {
            return currentResult;
        }
        
        // Aplicar peso ao contexto histórico
        const contextWeight = 0.3;
        const currentWeight = 0.7;
        
        const contextScores = {};
        Object.keys(this.languageProfiles).forEach(lang => {
            const contextScore = previousDetections
                .filter(det => det.language === lang)
                .reduce((sum, det) => sum + det.confidence, 0) / previousDetections.length;
            
            contextScores[lang] = (currentResult.scores[lang] * currentWeight) + 
                                 (contextScore * contextWeight);
        });
        
        const bestLang = Object.keys(contextScores).reduce((a, b) => 
            contextScores[a] > contextScores[b] ? a : b
        );
        
        return {
            language: bestLang,
            confidence: contextScores[bestLang],
            scores: contextScores,
            contextApplied: true
        };
    }
    
    addToHistory(text, result) {
        this.detectionHistory.push({
            timestamp: Date.now(),
            text: text.substring(0, 100), // Primeiros 100 caracteres
            result: result
        });
        
        // Manter apenas últimas 50 detecções
        if (this.detectionHistory.length > 50) {
            this.detectionHistory.shift();
        }
    }
    
    getDetectionHistory() {
        return this.detectionHistory;
    }
    
    // Método para treinar/ajustar modelo com feedback
    provideFeedback(text, actualLanguage, detectedResult) {
        console.log(`📚 Feedback recebido: ${detectedResult.language} -> ${actualLanguage}`);
        
        // Em uma implementação completa, isso atualizaria os modelos
        // Por enquanto, apenas registrar para análise
        this.detectionHistory.push({
            timestamp: Date.now(),
            text: text.substring(0, 100),
            detected: detectedResult.language,
            actual: actualLanguage,
            feedback: true
        });
    }
    
    // Método para obter estatísticas de performance
    getPerformanceStats() {
        const feedbackEntries = this.detectionHistory.filter(entry => entry.feedback);
        
        if (feedbackEntries.length === 0) {
            return { accuracy: 'N/A', totalFeedback: 0 };
        }
        
        const correct = feedbackEntries.filter(entry => 
            entry.detected === entry.actual
        ).length;
        
        return {
            accuracy: (correct / feedbackEntries.length * 100).toFixed(1) + '%',
            totalFeedback: feedbackEntries.length,
            correct: correct,
            incorrect: feedbackEntries.length - correct
        };
    }
    
    // Método para detectar idioma de comando de voz
    detectVoiceCommand(transcript) {
        // Procurar por comandos específicos
        const commands = {
            'pt': ['neuro traduza', 'neuro traduz', 'traduza para', 'traduzir'],
            'en': ['neuro translate', 'translate to', 'translate this']
        };
        
        const lowerTranscript = transcript.toLowerCase();
        
        for (const [lang, commandList] of Object.entries(commands)) {
            for (const command of commandList) {
                if (lowerTranscript.includes(command)) {
                    const textAfterCommand = lowerTranscript.split(command)[1]?.trim();
                    if (textAfterCommand) {
                        const detection = this.detectLanguage(textAfterCommand);
                        return {
                            commandLanguage: lang,
                            textLanguage: detection.language,
                            text: textAfterCommand,
                            confidence: detection.confidence,
                            command: command
                        };
                    }
                }
            }
        }
        
        return null;
    }
}

// Exportar para uso global
window.NeuroLanguageDetector = NeuroLanguageDetector;

console.log('🧠 Módulo NeuroLanguageDetector carregado!');