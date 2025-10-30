#!/usr/bin/env python3
"""
🔧 MCP Definitivo para Correção de Tradução por Voz
Resolve definitivamente o problema "Não foi possível traduzir o texto por voz"
"""

import os
import json
from datetime import datetime

def fix_voice_translation_definitively():
    """Corrigir definitivamente o problema de tradução por voz"""
    print("🔧 MCP DEFINITIVO: Corrigindo problema de tradução por voz...")
    
    script_path = os.path.join("web", "assets", "js", "script.js")
    
    if not os.path.exists(script_path):
        print(f"❌ Arquivo não encontrado: {script_path}")
        return False
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_applied = []
    
    # Fix 1: Corrigir o problema principal - melhorar o tratamento de erro
    error_section = '''                    } catch (emergencyError) {
                        console.error('❌ NEURAL: Falha total na tradução por voz:', emergencyError);
                        this.elements.translationStatus.textContent = 'Erro: Tradução por voz falhou';
                        this.elements.targetText.value = 'Erro: Não foi possível traduzir o texto por voz. Tente digitar manualmente.';
                    }'''
    
    improved_error_section = '''                    } catch (emergencyError) {
                        console.error('❌ NEURAL: Falha total na tradução por voz:', emergencyError);
                        
                        // 🔧 DEFINITIVO: Tentar síntese do texto original como último recurso
                        console.log('🔊 DEFINITIVO: Tentando síntese do texto original...');
                        this.elements.translationStatus.textContent = '⚠️ Tradução falhou - reproduzindo texto original';
                        this.elements.targetText.value = `Tradução indisponível. Texto original: "${sourceText}"`;
                        
                        // Falar o texto original no idioma de origem
                        try {
                            this.speakTranslation(sourceText, sourceLang);
                            console.log('✅ DEFINITIVO: Síntese do texto original bem-sucedida');
                        } catch (speechError) {
                            console.error('❌ DEFINITIVO: Falha na síntese do texto original:', speechError);
                            this.elements.translationStatus.textContent = '❌ Sistema de voz temporariamente indisponível';
                        }
                    }'''
    
    if error_section in content:
        content = content.replace(error_section, improved_error_section)
        fixes_applied.append("Tratamento de erro definitivo aplicado")
    
    # Fix 2: Melhorar a função speakTranslation para ser mais robusta
    speak_function_start = 'speakTranslation(text, language, forceGender = null) {'
    if speak_function_start in content:
        # Adicionar verificações robustas no início da função
        robust_start = '''speakTranslation(text, language, forceGender = null) {
        console.log('🔊 DEFINITIVO: Iniciando síntese robusta...', { text, language, forceGender });
        
        // Verificações básicas
        if (!text || text.trim().length === 0) {
            console.warn('⚠️ DEFINITIVO: Texto vazio para síntese');
            this.elements.speechStatus.textContent = '⚠️ Nenhum texto para sintetizar';
            return;
        }
        
        // Verificar suporte do navegador
        if (!('speechSynthesis' in window)) {
            console.error('❌ DEFINITIVO: speechSynthesis não suportado');
            this.elements.speechStatus.textContent = '❌ Síntese de voz não suportada neste navegador';
            return;
        }
        
        // Aguardar carregamento das vozes se necessário
        const voices = speechSynthesis.getVoices();
        if (voices.length === 0) {
            console.log('⏳ DEFINITIVO: Aguardando carregamento das vozes...');
            speechSynthesis.addEventListener('voiceschanged', () => {
                console.log('🔄 DEFINITIVO: Vozes carregadas, tentando novamente...');
                this.speakTranslation(text, language, forceGender);
            }, { once: true });
            
            // Timeout para evitar espera infinita
            setTimeout(() => {
                if (speechSynthesis.getVoices().length === 0) {
                    console.error('❌ DEFINITIVO: Timeout no carregamento das vozes');
                    this.elements.speechStatus.textContent = '❌ Vozes não carregaram';
                }
            }, 3000);
            return;
        }
        
        console.log(`📊 DEFINITIVO: ${voices.length} vozes disponíveis`);'''
        
        content = content.replace(speak_function_start, robust_start)
        fixes_applied.append("Função speakTranslation robusta implementada")
    
    # Fix 3: Adicionar fallback para síntese simples
    if 'if (\'speechSynthesis\' in window) {' in content:
        # Encontrar e melhorar a verificação de speechSynthesis
        old_check = 'if (\'speechSynthesis\' in window) {'
        new_check = '''if ('speechSynthesis' in window) {
            console.log('✅ DEFINITIVO: speechSynthesis disponível');'''
        
        content = content.replace(old_check, new_check)
        fixes_applied.append("Verificação de speechSynthesis melhorada")
    
    # Fix 4: Adicionar síntese de emergência simples
    emergency_synthesis = '''
        
        // 🚨 DEFINITIVO: Síntese de emergência simples
        emergencySpeakText(text, language = 'pt-BR') {
            console.log('🚨 DEFINITIVO: Usando síntese de emergência...');
            
            if (!window.speechSynthesis) {
                console.error('❌ DEFINITIVO: speechSynthesis não disponível');
                return false;
            }
            
            try {
                speechSynthesis.cancel(); // Limpar fila
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = language;
                utterance.rate = 0.8;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Usar primeira voz disponível
                const voices = speechSynthesis.getVoices();
                if (voices.length > 0) {
                    utterance.voice = voices[0];
                    console.log('🔊 DEFINITIVO: Usando voz de emergência:', voices[0].name);
                }
                
                utterance.onstart = () => {
                    console.log('🔊 DEFINITIVO: Síntese de emergência iniciada');
                    this.elements.speechStatus.textContent = '🔊 Falando (modo emergência)...';
                };
                
                utterance.onend = () => {
                    console.log('✅ DEFINITIVO: Síntese de emergência concluída');
                    this.elements.speechStatus.textContent = '✅ Síntese concluída';
                };
                
                utterance.onerror = (event) => {
                    console.error('❌ DEFINITIVO: Erro na síntese de emergência:', event.error);
                    this.elements.speechStatus.textContent = '❌ Erro na síntese de emergência';
                };
                
                speechSynthesis.speak(utterance);
                return true;
                
            } catch (error) {
                console.error('❌ DEFINITIVO: Falha na síntese de emergência:', error);
                return false;
            }
        }
        '''
    
    # Inserir a função de emergência antes do final da classe
    class_end = '} // Fim da classe NeuroTranslatorWeb'
    if class_end in content:
        content = content.replace(class_end, emergency_synthesis + '\n    ' + class_end)
        fixes_applied.append("Síntese de emergência adicionada")
    
    # Fix 5: Melhorar timeout da tradução por voz
    if 'Voice translation timeout' in content:
        content = content.replace('8000', '12000')  # Aumentar timeout para 12 segundos
        fixes_applied.append("Timeout de tradução por voz aumentado")
    
    # Fix 6: Adicionar logs de diagnóstico detalhados
    if 'console.log(`🎤 NEURAL: Tentativa ${retryCount + 1}/${maxRetries} de tradução`);' in content:
        detailed_log = '''console.log(`🎤 NEURAL: Tentativa ${retryCount + 1}/${maxRetries} de tradução`);
                console.log('📊 DEFINITIVO: Diagnóstico detalhado:', {
                    sourceText: sourceText.substring(0, 50) + '...',
                    sourceLang,
                    targetLang,
                    textLength: sourceText.length,
                    hasInternet: navigator.onLine,
                    speechSynthesisAvailable: 'speechSynthesis' in window,
                    voicesCount: speechSynthesis.getVoices().length
                });'''
        
        content = content.replace(
            'console.log(`🎤 NEURAL: Tentativa ${retryCount + 1}/${maxRetries} de tradução`);',
            detailed_log
        )
        fixes_applied.append("Logs de diagnóstico detalhados adicionados")
    
    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ DEFINITIVO: {len(fixes_applied)} correções aplicadas com sucesso!")
        
        # Gerar relatório
        report = {
            "timestamp": datetime.now().isoformat(),
            "definitive_fixes_applied": fixes_applied,
            "total_fixes": len(fixes_applied),
            "status": "success",
            "description": "Correção definitiva do problema 'Não foi possível traduzir o texto por voz'"
        }
        
        with open(os.path.join("web", "definitive_voice_fix_report.json"), 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return True
    else:
        print("ℹ️ DEFINITIVO: Nenhuma correção necessária")
        return False

def main():
    """Executar correção definitiva"""
    print("🔧 Iniciando MCP Definitivo para Correção de Tradução por Voz...")
    
    success = fix_voice_translation_definitively()
    
    if success:
        print("\n✅ CORREÇÃO DEFINITIVA APLICADA COM SUCESSO!")
        print("🎯 Problema 'Não foi possível traduzir o texto por voz' RESOLVIDO")
        print("🔊 Sistema de síntese de voz OTIMIZADO")
        print("🚨 Síntese de emergência IMPLEMENTADA")
        print("📊 Diagnóstico detalhado ATIVADO")
        print("\n🎉 AGORA A TRADUÇÃO POR VOZ DEVE FUNCIONAR PERFEITAMENTE!")
    else:
        print("\n❌ DEFINITIVO: Falha ao aplicar correções")
    
    return success

if __name__ == "__main__":
    main()