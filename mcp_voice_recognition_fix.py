#!/usr/bin/env python3
"""
MCP Voice Recognition Fix - Correção Definitiva de Erros de Reconhecimento
Resolve problemas persistentes de InvalidStateError e aborted
"""

import os
import re
import json
from datetime import datetime

class VoiceRecognitionFixMCP:
    def __init__(self):
        self.web_dir = "web"
        self.js_file = os.path.join(self.web_dir, "assets", "js", "ai-voice-vision.js")
        self.fixes_applied = []
        
    def apply_definitive_voice_fix(self):
        """Aplica correção definitiva para reconhecimento de voz"""
        print("🔧 Aplicando correção definitiva de reconhecimento de voz...")
        
        if not os.path.exists(self.js_file):
            print(f"❌ Arquivo não encontrado: {self.js_file}")
            return
            
        with open(self.js_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Reescrever completamente o sistema de reconhecimento
        content = self._rewrite_voice_system(content)
        
        # Salvar arquivo corrigido
        with open(self.js_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Correção definitiva aplicada com sucesso!")
        
    def _rewrite_voice_system(self, content):
        """Reescreve completamente o sistema de reconhecimento de voz"""
        
        # Encontrar e substituir o método initVoiceSystem
        init_voice_pattern = r'async initVoiceSystem\(\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        
        new_init_voice = '''async initVoiceSystem() {
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
    }'''
        
        content = re.sub(init_voice_pattern, new_init_voice, content, flags=re.DOTALL)
        self.fixes_applied.append("Sistema de reconhecimento de voz reescrito")
        
        # Adicionar método de início seguro
        safe_start_method = '''
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
'''
        
        # Inserir método antes de startVoiceActivation
        insert_pos = content.find('async startVoiceActivation()')
        if insert_pos > 0:
            content = content[:insert_pos] + safe_start_method + '\n    ' + content[insert_pos:]
            self.fixes_applied.append("Método de início seguro adicionado")
        
        # Substituir startVoiceActivation
        start_voice_pattern = r'async startVoiceActivation\(\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        
        new_start_voice = '''async startVoiceActivation() {
        if (!this.isInitialized) {
            console.warn('⚠️ NeuroAI não inicializado');
            return;
        }
        
        console.log('🎤 Iniciando escuta por comando de ativação...');
        this.safeStartRecognition();
    }'''
        
        content = re.sub(start_voice_pattern, new_start_voice, content, flags=re.DOTALL)
        self.fixes_applied.append("Método startVoiceActivation simplificado")
        
        return content
        
    def generate_report(self):
        """Gera relatório das correções aplicadas"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "mcp": "Voice Recognition Fix",
            "fixes_applied": self.fixes_applied,
            "status": "completed" if self.fixes_applied else "no_changes_needed"
        }
        
        print("\n📊 RELATÓRIO DE CORREÇÃO DEFINITIVA DE VOZ")
        print("=" * 50)
        for fix in self.fixes_applied:
            print(f"✅ {fix}")
        print(f"\n🕒 Aplicado em: {report['timestamp']}")
        
        return report

def main():
    print("🎤 MCP Voice Recognition Fix - Iniciando correção definitiva...")
    
    mcp = VoiceRecognitionFixMCP()
    mcp.apply_definitive_voice_fix()
    report = mcp.generate_report()
    
    print("\n🎯 Correção definitiva de reconhecimento de voz concluída!")
    return report

if __name__ == "__main__":
    main()