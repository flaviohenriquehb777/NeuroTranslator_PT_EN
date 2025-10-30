#!/usr/bin/env python3
"""
MCP Especializado - Correção de Sintaxe JavaScript
Corrige erros de sintaxe no arquivo script.js
"""

import os
import re

def fix_javascript_syntax():
    """Corrige erros de sintaxe no arquivo JavaScript"""
    
    script_path = "web/assets/js/script.js"
    
    if not os.path.exists(script_path):
        print(f"❌ Arquivo não encontrado: {script_path}")
        return False
    
    print("🔧 Iniciando correção de sintaxe JavaScript...")
    
    # Ler o arquivo atual
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrigir problemas de sintaxe conhecidos
    fixes_applied = []
    
    # 1. Remover pontos e vírgulas soltos
    if ';\n        \n        this.speech = {' in content:
        content = content.replace(';\n        \n        this.speech = {', '\n        \n        this.speech = {')
        fixes_applied.append("Removido ponto e vírgula solto")
    
    # 2. Corrigir estrutura da classe NeuroTranslatorWeb
    # Procurar por código fora da classe que deveria estar dentro
    pattern = r'(class NeuroTranslatorWeb \{[\s\S]*?constructor\(\) \{[\s\S]*?\})\s*([\s\S]*?)(    init\(\))'
    match = re.search(pattern, content)
    
    if match:
        class_start = match.group(1)
        misplaced_code = match.group(2)
        init_method = match.group(3)
        
        # Se há código mal posicionado, reorganizar
        if 'this.speech = {' in misplaced_code or 'this.translation = {' in misplaced_code:
            # Extrair apenas as propriedades necessárias
            speech_match = re.search(r'this\.speech = \{[^}]+\};', misplaced_code)
            translation_match = re.search(r'this\.translation = \{[^}]+\};', misplaced_code)
            elements_match = re.search(r'this\.elements = \{\};', misplaced_code)
            ai_match = re.search(r'this\.aiIntegration = null;', misplaced_code)
            init_match = re.search(r'this\.init\(\);', misplaced_code)
            
            # Reconstruir o construtor corretamente
            new_constructor = """class NeuroTranslatorWeb {
    constructor() {
        this.camera = {
            stream: null,
            active: false,
            supported: false
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
        
        // Inicializar sistema de IA integrado
        this.aiIntegration = null;
        
        this.init();
    }"""
            
            # Substituir a parte problemática
            content = re.sub(
                r'class NeuroTranslatorWeb \{[\s\S]*?this\.init\(\);\s*\}',
                new_constructor,
                content,
                count=1
            )
            fixes_applied.append("Corrigida estrutura da classe NeuroTranslatorWeb")
    
    # 3. Remover métodos duplicados ou mal posicionados
    # Procurar por métodos que estão fora da classe
    methods_outside_class = []
    
    # Padrão para encontrar métodos fora da classe
    after_class_pattern = r'(\}\s*document\.addEventListener.*)'
    after_class_match = re.search(after_class_pattern, content, re.DOTALL)
    
    if after_class_match:
        after_class_content = after_class_match.group(1)
        
        # Procurar por métodos que não deveriam estar aqui
        method_patterns = [
            r'initVoiceRecognition\(\)[\s\S]*?\}',
            r'startVoiceRecognition\(\)[\s\S]*?\}',
            r'stopVoiceRecognition\(\)[\s\S]*?\}',
            r'updateVoiceStatus\([\s\S]*?\}',
            r'getStatusText\([\s\S]*?\}',
            r'processVoiceCommand\([\s\S]*?\}',
            r'activateTranslation\(\)[\s\S]*?\}',
            r'processTranslation\([\s\S]*?\}'
        ]
        
        for pattern in method_patterns:
            if re.search(pattern, after_class_content):
                # Remover esses métodos duplicados
                content = re.sub(pattern, '', content)
                fixes_applied.append(f"Removido método duplicado: {pattern.split('\\(')[0]}")
    
    # 4. Corrigir chaves desbalanceadas
    open_braces = content.count('{')
    close_braces = content.count('}')
    
    if open_braces != close_braces:
        print(f"⚠️ Chaves desbalanceadas: {open_braces} abertas, {close_braces} fechadas")
        
        # Tentar balancear removendo chaves extras no final
        if close_braces > open_braces:
            extra_braces = close_braces - open_braces
            # Remover chaves extras do final
            for _ in range(extra_braces):
                content = content.rstrip()
                if content.endswith('}'):
                    content = content[:-1].rstrip()
            fixes_applied.append(f"Removidas {extra_braces} chaves extras")
    
    # 5. Verificar e corrigir sintaxe básica
    # Remover linhas vazias excessivas
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Corrigir espaçamento
    content = re.sub(r'    \n        ', '\n        ', content)
    
    # Salvar o arquivo corrigido
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Correções aplicadas:")
    for fix in fixes_applied:
        print(f"   • {fix}")
    
    print(f"✅ Arquivo JavaScript corrigido: {script_path}")
    return True

if __name__ == "__main__":
    try:
        success = fix_javascript_syntax()
        if success:
            print("\n🎉 Correção de sintaxe JavaScript concluída com sucesso!")
        else:
            print("\n❌ Falha na correção de sintaxe JavaScript")
    except Exception as e:
        print(f"\n❌ Erro durante a correção: {e}")