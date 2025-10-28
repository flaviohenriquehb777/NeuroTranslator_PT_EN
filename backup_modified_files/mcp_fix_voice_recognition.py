#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Fix Voice Recognition - Correção do Reconhecimento de Voz
Corrige os erros de reconhecimento de voz: aborted, InvalidStateError
"""

import os
import re
from datetime import datetime

class MCPFixVoiceRecognition:
    def __init__(self):
        self.name = "MCP Fix Voice Recognition"
        self.version = "1.0.0"
        self.description = "Corrige problemas de reconhecimento de voz"
        
    def fix_voice_recognition(self, file_path):
        """Corrige problemas de reconhecimento de voz"""
        
        print(f"🔧 Corrigindo reconhecimento de voz em: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Implementar correções para SpeechRecognition
            voice_recognition_fix = '''
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
'''
            
            # Inserir as correções no arquivo
            if 'initVoiceRecognition' not in content:
                # Encontrar local apropriado para inserir
                class_pattern = r'(class\s+\w+\s*\{[^}]*constructor[^}]*\})'
                match = re.search(class_pattern, content, re.DOTALL)
                
                if match:
                    insert_pos = match.end()
                    content = content[:insert_pos] + voice_recognition_fix + content[insert_pos:]
                else:
                    # Inserir no final do arquivo
                    content += voice_recognition_fix
            
            # Salvar apenas se houve mudanças
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ Correções aplicadas em: {file_path}")
                return True
            else:
                print(f"ℹ️ Nenhuma correção necessária em: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {str(e)}")
            return False
    
    def process_files(self):
        """Processa arquivos de reconhecimento de voz"""
        
        js_files = [
            "assets/js/ai-voice-vision.js",
            "assets/js/script.js"
        ]
        
        processed_files = []
        
        for js_file in js_files:
            if os.path.exists(js_file):
                if self.fix_voice_recognition(js_file):
                    processed_files.append(js_file)
            else:
                print(f"⚠️ Arquivo não encontrado: {js_file}")
        
        return processed_files
    
    def generate_report(self, processed_files):
        """Gera relatório das correções"""
        
        report = {
            "mcp_name": self.name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "processed_files": processed_files,
            "fixes_applied": [
                "Correção do erro 'aborted' no SpeechRecognition",
                "Correção do erro 'InvalidStateError: recognition has already started'",
                "Implementação de controle de estado do reconhecimento",
                "Adição de timeout de segurança",
                "Tratamento específico de diferentes tipos de erro",
                "Reinicialização automática em caso de falha",
                "Verificação de permissões de microfone",
                "Feedback visual de status do reconhecimento"
            ],
            "status": "success" if processed_files else "no_changes"
        }
        
        # Salvar relatório
        with open('mcp_voice_fix_report.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Relatório salvo: mcp_voice_fix_report.json")
        return report

# Executar MCP
if __name__ == "__main__":
    mcp = MCPFixVoiceRecognition()
    
    print(f"🚀 Iniciando {mcp.name}...")
    
    processed_files = mcp.process_files()
    report = mcp.generate_report(processed_files)
    
    if processed_files:
        print(f"🎉 {mcp.name} concluído com sucesso!")
        print(f"📁 Arquivos processados: {len(processed_files)}")
        for file in processed_files:
            print(f"   - {file}")
    else:
        print(f"ℹ️ {mcp.name} concluído - nenhuma alteração necessária")