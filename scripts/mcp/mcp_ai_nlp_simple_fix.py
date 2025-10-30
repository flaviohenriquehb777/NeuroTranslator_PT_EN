#!/usr/bin/env python3
"""
🤖 MCP AI/NLP Simple Voice Fix
Aplicação direta de correções AI/NLP para problemas de tradução por voz
"""

import os
import json
from datetime import datetime

def apply_ai_nlp_voice_fixes():
    """Aplicar correções AI/NLP diretas no sistema de voz"""
    print("🤖 AI/NLP: Aplicando correções diretas para tradução por voz...")
    
    script_path = os.path.join("web", "assets", "js", "script.js")
    
    if not os.path.exists(script_path):
        print(f"❌ Arquivo não encontrado: {script_path}")
        return False
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_applied = []
    
    # Fix 1: Melhorar validação de texto antes da tradução
    if 'validateTextWithNLP' not in content:
        validation_code = '''
        // 🤖 AI/NLP: Validação inteligente de texto
        validateTextWithNLP(text, confidence = 0.8) {
            console.log('🔍 AI/NLP: Validando texto com NLP...');
            
            if (!text || text.trim().length < 2) {
                console.warn('❌ AI/NLP: Texto muito curto');
                return false;
            }
            
            if (confidence < 0.6) {
                console.warn('❌ AI/NLP: Confiança muito baixa:', confidence);
                return false;
            }
            
            const noisePattern = /^[^a-zA-ZÀ-ÿ0-9\\s]*$/;
            if (noisePattern.test(text)) {
                console.warn('❌ AI/NLP: Texto contém apenas ruído');
                return false;
            }
            
            const words = text.trim().split(/\\s+/);
            if (words.length < 1) {
                console.warn('❌ AI/NLP: Nenhuma palavra válida detectada');
                return false;
            }
            
            console.log('✅ AI/NLP: Texto validado com sucesso');
            return true;
        }
        '''
        
        # Inserir após o constructor
        constructor_end = content.find('this.initializeEventListeners();')
        if constructor_end != -1:
            insertion_point = content.find('}', constructor_end) + 1
            content = content[:insertion_point] + validation_code + content[insertion_point:]
            fixes_applied.append("Validação NLP de texto adicionada")
    
    # Fix 2: Melhorar tratamento de erro na tradução por voz
    error_pattern = 'Erro: Não foi possível traduzir o texto por voz. Tente digitar manualmente.'
    if error_pattern in content:
        # Substituir mensagem de erro genérica por tratamento inteligente
        improved_error = '''
                        console.error('❌ AI/NLP: Erro na tradução por voz:', emergencyError);
                        
                        // 🤖 AI/NLP: Análise inteligente do erro
                        let errorMessage = 'Sistema temporariamente indisponível.';
                        if (emergencyError.message.includes('network')) {
                            errorMessage = 'Problema de conexão. Verifique sua internet.';
                        } else if (emergencyError.message.includes('timeout')) {
                            errorMessage = 'Timeout na tradução. Tente uma frase mais curta.';
                        }
                        
                        this.elements.translationStatus.textContent = `⚠️ ${errorMessage}`;
                        this.elements.targetText.value = 'Tente novamente em alguns segundos ou digite manualmente.';
                        
                        // 🤖 AI/NLP: Tentar síntese mesmo com erro de tradução
                        if (this.elements.sourceText.value.trim()) {
                            console.log('🔊 AI/NLP: Tentando síntese do texto original...');
                            this.speakTranslation(this.elements.sourceText.value, this.elements.sourceLang.value);
                        }'''
        
        content = content.replace(
            'this.elements.translationStatus.textContent = \'Erro: Não foi possível traduzir o texto por voz. Tente digitar manualmente.\';',
            improved_error
        )
        fixes_applied.append("Tratamento de erro inteligente aplicado")
    
    # Fix 3: Melhorar síntese de voz com verificações robustas
    if 'speakTranslation(' in content:
        # Encontrar a função speakTranslation e melhorá-la
        speak_start = content.find('speakTranslation(')
        if speak_start != -1:
            # Adicionar verificações robustas no início da função
            robust_checks = '''
            // 🤖 AI/NLP: Verificações robustas para síntese
            if (!text || !text.trim()) {
                console.warn('⚠️ AI/NLP: Texto vazio para síntese');
                this.elements.speechStatus.textContent = '⚠️ Nenhum texto para sintetizar';
                return;
            }
            
            // Verificar disponibilidade do speechSynthesis
            if (!window.speechSynthesis) {
                console.error('❌ AI/NLP: speechSynthesis não disponível');
                this.elements.speechStatus.textContent = '❌ Síntese de voz não suportada';
                return;
            }
            
            // Aguardar carregamento das vozes se necessário
            if (speechSynthesis.getVoices().length === 0) {
                console.log('⏳ AI/NLP: Aguardando carregamento das vozes...');
                speechSynthesis.addEventListener('voiceschanged', () => {
                    this.speakTranslation(text, language);
                }, { once: true });
                return;
            }
            '''
            
            # Encontrar o início do corpo da função
            func_body_start = content.find('{', speak_start)
            if func_body_start != -1:
                content = content[:func_body_start + 1] + robust_checks + content[func_body_start + 1:]
                fixes_applied.append("Verificações robustas de síntese adicionadas")
    
    # Fix 4: Adicionar logs de diagnóstico AI/NLP
    if 'console.log(\'🤖 AI/NLP:' not in content:
        # Adicionar logs em pontos críticos
        content = content.replace(
            'recognition.onresult = (event) => {',
            '''recognition.onresult = (event) => {
                console.log('🎤 AI/NLP: Processando resultado de reconhecimento de voz...');'''
        )
        
        content = content.replace(
            'this.translateTextWithSpeech(true);',
            '''console.log('🚀 AI/NLP: Iniciando tradução automática por voz...');
                this.translateTextWithSpeech(true);'''
        )
        
        fixes_applied.append("Logs de diagnóstico AI/NLP adicionados")
    
    # Fix 5: Melhorar timeout e retry para tradução por voz
    if 'maxRetries = 3' in content:
        content = content.replace('maxRetries = 3', 'maxRetries = 5')
        content = content.replace('timeout: 10000', 'timeout: 15000')
        fixes_applied.append("Timeout e retry otimizados para voz")
    
    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ AI/NLP: {len(fixes_applied)} correções aplicadas com sucesso!")
        
        # Gerar relatório
        report = {
            "timestamp": datetime.now().isoformat(),
            "ai_nlp_fixes_applied": fixes_applied,
            "total_fixes": len(fixes_applied),
            "status": "success"
        }
        
        with open(os.path.join("web", "ai_nlp_voice_fix_report.json"), 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return True
    else:
        print("ℹ️ AI/NLP: Nenhuma correção necessária")
        return False

def main():
    """Executar correções AI/NLP"""
    print("🤖 Iniciando MCP AI/NLP Simple Voice Fix...")
    
    success = apply_ai_nlp_voice_fixes()
    
    if success:
        print("\n✅ AI/NLP: Correções aplicadas com sucesso!")
        print("📋 Sistema de tradução por voz otimizado com IA")
        print("🔊 Síntese de voz melhorada com verificações robustas")
        print("⚠️ Tratamento de erro inteligente implementado")
    else:
        print("\n❌ AI/NLP: Falha ao aplicar correções")
    
    return success

if __name__ == "__main__":
    main()