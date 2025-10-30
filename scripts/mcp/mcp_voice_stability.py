#!/usr/bin/env python3
"""
MCP Voice Stability - Correção de Erros de Reconhecimento de Voz
Corrige problemas de InvalidStateError e aborted no reconhecimento contínuo
"""

import os
import re
import json
from datetime import datetime

class VoiceStabilityMCP:
    def __init__(self):
        self.web_dir = "web"
        self.js_file = os.path.join(self.web_dir, "assets", "js", "ai-voice-vision.js")
        self.fixes_applied = []
        
    def apply_voice_stability_fixes(self):
        """Aplica correções para estabilidade do reconhecimento de voz"""
        print("🔧 Aplicando correções de estabilidade de voz...")
        
        if not os.path.exists(self.js_file):
            print(f"❌ Arquivo não encontrado: {self.js_file}")
            return
            
        with open(self.js_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Aplicar correções específicas
        content = self._fix_recognition_cleanup(content)
        content = self._add_state_validation(content)
        content = self._improve_error_recovery(content)
        
        # Salvar arquivo corrigido
        with open(self.js_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Correções de estabilidade aplicadas com sucesso!")
        
    def _fix_recognition_cleanup(self, content):
        """Adiciona limpeza adequada do reconhecimento"""
        
        # Procurar pela função stopVoiceActivation e melhorá-la
        stop_function_pattern = r'(stopVoiceActivation\(\)\s*\{[^}]*\})'
        
        new_stop_function = '''stopVoiceActivation() {
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
    }'''
        
        if re.search(stop_function_pattern, content, re.DOTALL):
            content = re.sub(stop_function_pattern, new_stop_function, content, flags=re.DOTALL)
            self.fixes_applied.append("Melhorada função stopVoiceActivation")
        else:
            # Se não encontrar, adicionar a função
            insert_pos = content.find('startVoiceActivation()')
            if insert_pos > 0:
                content = content[:insert_pos] + new_stop_function + '\n\n    ' + content[insert_pos:]
                self.fixes_applied.append("Adicionada função stopVoiceActivation melhorada")
        
        return content
        
    def _add_state_validation(self, content):
        """Adiciona validação de estado mais robusta"""
        
        # Adicionar método de validação de estado
        validation_method = '''
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
'''
        
        # Inserir antes da função startVoiceActivation
        insert_pos = content.find('startVoiceActivation()')
        if insert_pos > 0:
            content = content[:insert_pos] + validation_method + '\n    ' + content[insert_pos:]
            self.fixes_applied.append("Adicionado método de validação de estado")
            
        return content
        
    def _improve_error_recovery(self, content):
        """Melhora a recuperação de erros"""
        
        # Adicionar método de recuperação de emergência
        recovery_method = '''
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
'''
        
        # Inserir antes da função handleVoiceError
        insert_pos = content.find('handleVoiceError(')
        if insert_pos > 0:
            content = content[:insert_pos] + recovery_method + '\n    ' + content[insert_pos:]
            self.fixes_applied.append("Adicionado método de recuperação de emergência")
            
        return content
        
    def generate_report(self):
        """Gera relatório das correções aplicadas"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "mcp": "Voice Stability",
            "fixes_applied": self.fixes_applied,
            "status": "completed" if self.fixes_applied else "no_changes_needed"
        }
        
        print("\n📊 RELATÓRIO DE CORREÇÕES DE ESTABILIDADE DE VOZ")
        print("=" * 50)
        for fix in self.fixes_applied:
            print(f"✅ {fix}")
        print(f"\n🕒 Aplicado em: {report['timestamp']}")
        
        return report

def main():
    print("🎤 MCP Voice Stability - Iniciando correções...")
    
    mcp = VoiceStabilityMCP()
    mcp.apply_voice_stability_fixes()
    report = mcp.generate_report()
    
    print("\n🎯 Correções de estabilidade de voz concluídas!")
    return report

if __name__ == "__main__":
    main()