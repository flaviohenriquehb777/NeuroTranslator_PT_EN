#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 MCP Voice UI Fix - Correção da Interface de Controles de Voz
"""

import os
import re

class VoiceUIFixer:
    def __init__(self):
        self.web_path = "web"
        self.css_path = os.path.join(self.web_path, "assets", "css", "style.css")
        self.fixes_applied = []
        
    def add_voice_controls_css(self):
        """Adicionar CSS para controles de voz"""
        print("🎨 Adicionando CSS para controles de voz...")
        
        if not os.path.exists(self.css_path):
            print(f"❌ CSS não encontrado: {self.css_path}")
            return False
            
        with open(self.css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            
        # CSS para controles de gênero de voz
        voice_css = '''
/* Voice Gender Controls */
.voice-gender-controls {
    margin: 15px 0;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.voice-gender-controls label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #ffffff;
    font-size: 14px;
}

.gender-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.gender-btn {
    flex: 1;
    padding: 12px 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 25px;
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.gender-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.gender-btn.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.gender-btn.active:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
    .gender-buttons {
        flex-direction: column;
    }
    
    .gender-btn {
        padding: 15px 20px;
        font-size: 16px;
    }
}'''
        
        # Adicionar CSS se não existir
        if 'voice-gender-controls' not in css_content:
            css_content += '\n' + voice_css
            
            with open(self.css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
                
            self.fixes_applied.append("CSS para controles de gênero de voz adicionado")
            return True
            
        return False
        
    def run_ui_fixes(self):
        """Executar todas as correções de UI"""
        print("🎨 Iniciando correções de interface...")
        
        self.add_voice_controls_css()
        
        print(f"\n✅ {len(self.fixes_applied)} correções de UI aplicadas!")
        for fix in self.fixes_applied:
            print(f"  • {fix}")
            
        return len(self.fixes_applied) > 0

if __name__ == "__main__":
    fixer = VoiceUIFixer()
    fixer.run_ui_fixes()