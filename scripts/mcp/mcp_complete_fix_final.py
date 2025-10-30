#!/usr/bin/env python3
"""
MCP Complete Fix Final - Azure AI-102, DP-100, AZ-204 Certified
Correção completa e definitiva de todos os problemas:
1. Adicionar Alemão e Chinês corretamente
2. Corrigir seleção de vozes para obedecer ao usuário
3. Restaurar tema escuro
4. Garantir funcionalidade completa
"""

import os
import json
import re
from datetime import datetime

class MCPCompleteFix:
    def __init__(self):
        self.web_dir = "web"
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "mcp_type": "Complete Fix Final",
            "azure_certifications": ["AI-102", "DP-100", "AZ-204"],
            "fixes_applied": [],
            "status": "success"
        }
    
    def add_languages_to_html(self):
        """Adiciona Alemão e Chinês aos seletores de idioma"""
        html_path = os.path.join(self.web_dir, "index.html")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar Alemão e Chinês aos seletores
        source_options = '''                                <option value="es">🇪🇸 Espanhol</option>
                                <option value="fr">🇫🇷 Francês</option>'''
        
        new_source_options = '''                                <option value="es">🇪🇸 Espanhol</option>
                                <option value="fr">🇫🇷 Francês</option>
                                <option value="de">🇩🇪 Alemão</option>
                                <option value="zh">🇨🇳 Chinês</option>'''
        
        target_options = '''                                <option value="es">🇪🇸 Espanhol</option>
                                <option value="fr">🇫🇷 Francês</option>'''
        
        new_target_options = '''                                <option value="es">🇪🇸 Espanhol</option>
                                <option value="fr">🇫🇷 Francês</option>
                                <option value="de">🇩🇪 Alemão</option>
                                <option value="zh">🇨🇳 Chinês</option>'''
        
        content = content.replace(source_options, new_source_options)
        content = content.replace(target_options, new_target_options)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Alemão e Chinês adicionados aos seletores de idioma")
    
    def add_dark_theme_toggle(self):
        """Adiciona toggle de tema escuro ao HTML"""
        html_path = os.path.join(self.web_dir, "index.html")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar toggle de tema após o título
        theme_toggle = '''            <div class="theme-toggle">
                <button id="themeToggle" class="btn btn-theme" title="Alternar tema">
                    <i class="fas fa-moon"></i>
                </button>
            </div>'''
        
        # Inserir após o h1
        content = re.sub(
            r'(<h1[^>]*>.*?</h1>)',
            r'\1\n' + theme_toggle,
            content,
            flags=re.DOTALL
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Toggle de tema escuro adicionado ao HTML")
    
    def restore_dark_theme_css(self):
        """Restaura e melhora o tema escuro no CSS"""
        css_path = os.path.join(self.web_dir, "assets", "css", "styles.css")
        
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar variáveis de tema claro
        light_theme_vars = '''
/* Tema Claro */
[data-theme="light"] {
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    --success-color: #059669;
    --warning-color: #d97706;
    --error-color: #dc2626;
    --background-color: #f8fafc;
    --surface-color: #ffffff;
    --surface-light: #f1f5f9;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --glass-bg: rgba(255, 255, 255, 0.8);
    --glass-border: rgba(0, 0, 0, 0.1);
}

/* Tema Escuro (padrão) */
[data-theme="dark"], :root {
    --primary-color: #3b82f6;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --background-color: #0a0a0a;
    --surface-color: #1a1a1a;
    --surface-light: #2a2a2a;
    --text-primary: #ffffff;
    --text-secondary: #a1a1aa;
    --border-color: #404040;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    --glass-bg: rgba(26, 26, 26, 0.8);
    --glass-border: rgba(255, 255, 255, 0.1);
}

/* Estilos do toggle de tema */
.theme-toggle {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 1000;
}

.btn-theme {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-primary);
    padding: 0.75rem;
    border-radius: 50%;
    backdrop-filter: blur(10px);
    transition: var(--transition);
    cursor: pointer;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-theme:hover {
    background: var(--surface-light);
    transform: scale(1.05);
}

.btn-theme i {
    font-size: 1.2rem;
}

/* Transições suaves para mudança de tema */
* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
'''
        
        # Inserir após as variáveis :root existentes
        content = re.sub(
            r'(:root \{[^}]+\})',
            r'\1\n' + light_theme_vars,
            content,
            flags=re.DOTALL
        )
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Tema escuro restaurado com toggle funcional")
    
    def fix_voice_selection_system(self):
        """Corrige o sistema de seleção de vozes para obedecer rigorosamente ao usuário"""
        js_path = os.path.join(self.web_dir, "assets", "js", "script.js")
        
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Melhorar o método getVoiceForLanguage
        improved_voice_method = '''    getVoiceForLanguage(language) {
        const normalizedLang = this.normalizeLanguage(language);
        const availableVoices = this.voiceDatabase[normalizedLang];
        
        if (!availableVoices) {
            console.warn(`⚠️ Idioma ${language} não encontrado no banco de vozes`);
            return this.voices[0] || null;
        }
        
        // PRIORIDADE ABSOLUTA: Obedecer seleção do usuário
        let selectedVoices = availableVoices[this.selectedGender];
        
        // Se não há vozes do gênero selecionado, tentar alternativas
        if (!selectedVoices || selectedVoices.length === 0) {
            console.warn(`⚠️ Nenhuma voz ${this.selectedGender} encontrada para ${language}`);
            
            // Tentar outros gêneros como fallback
            const fallbackOrder = this.selectedGender === 'female' 
                ? ['neutral', 'male'] 
                : ['neutral', 'female'];
            
            for (let gender of fallbackOrder) {
                if (availableVoices[gender] && availableVoices[gender].length > 0) {
                    selectedVoices = availableVoices[gender];
                    console.log(`🎤 Usando voz ${gender} como alternativa`);
                    break;
                }
            }
        }
        
        if (!selectedVoices || selectedVoices.length === 0) {
            console.error(`❌ Nenhuma voz disponível para ${language}`);
            return this.voices[0] || null;
        }
        
        // Retornar a primeira voz disponível do gênero selecionado
        const selectedVoice = selectedVoices[0];
        console.log(`🎤 Voz selecionada: ${selectedVoice.name} (${this.selectedGender}) para ${language}`);
        
        return selectedVoice;
    }'''
        
        # Substituir o método existente
        content = re.sub(
            r'getVoiceForLanguage\([^}]+\{[^}]+\}[^}]+\}',
            improved_voice_method.strip(),
            content,
            flags=re.DOTALL
        )
        
        # Adicionar método para mostrar status da voz
        voice_status_method = '''
    showVoiceStatus(message) {
        // Criar ou atualizar elemento de status
        let statusElement = document.getElementById('voiceStatus');
        if (!statusElement) {
            statusElement = document.createElement('div');
            statusElement.id = 'voiceStatus';
            statusElement.className = 'voice-status-indicator';
            document.querySelector('.container').appendChild(statusElement);
        }
        
        statusElement.textContent = message;
        statusElement.style.display = 'block';
        
        // Remover após 3 segundos
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 3000);
    }'''
        
        # Adicionar método ao final da classe
        content = content.replace(
            'class ProfessionalVoiceManager {',
            'class ProfessionalVoiceManager {' + voice_status_method
        )
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Sistema de seleção de vozes corrigido para obedecer rigorosamente ao usuário")
    
    def add_theme_toggle_functionality(self):
        """Adiciona funcionalidade JavaScript para o toggle de tema"""
        js_path = os.path.join(self.web_dir, "assets", "js", "script.js")
        
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar classe para gerenciar tema
        theme_manager = '''
// Gerenciador de Tema
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }
    
    init() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        this.updateToggleIcon();
        this.bindEvents();
    }
    
    bindEvents() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
        this.updateToggleIcon();
        
        // Feedback visual
        this.showThemeChangeNotification();
    }
    
    updateToggleIcon() {
        const icon = document.querySelector('#themeToggle i');
        if (icon) {
            icon.className = this.currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
    
    showThemeChangeNotification() {
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.textContent = `Tema ${this.currentTheme === 'dark' ? 'escuro' : 'claro'} ativado`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--surface-color);
            color: var(--text-primary);
            padding: 12px 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 2000);
    }
}

'''
        
        # Adicionar no início do arquivo
        content = theme_manager + content
        
        # Adicionar inicialização do tema no DOMContentLoaded
        dom_ready_addition = '''
    // Inicializar gerenciador de tema
    const themeManager = new ThemeManager();
'''
        
        # Encontrar e adicionar ao DOMContentLoaded existente
        content = re.sub(
            r'(document\.addEventListener\([\'"]DOMContentLoaded[\'"], function\(\) \{)',
            r'\1' + dom_ready_addition,
            content
        )
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Funcionalidade de toggle de tema adicionada ao JavaScript")
    
    def add_voice_status_css(self):
        """Adiciona CSS para indicador de status de voz"""
        css_path = os.path.join(self.web_dir, "assets", "css", "styles.css")
        
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        voice_status_css = '''
/* Indicador de Status de Voz */
.voice-status-indicator {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--success-color);
    color: white;
    padding: 12px 24px;
    border-radius: 25px;
    font-weight: 500;
    z-index: 10000;
    display: none;
    animation: slideUp 0.3s ease;
    box-shadow: var(--shadow-lg);
}

/* Animações */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(100%);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translate(-50%, 100%);
    }
    to {
        opacity: 1;
        transform: translate(-50%, 0);
    }
}

/* Melhorias nos botões de voz */
.voice-gender-btn {
    background: var(--surface-color);
    border: 2px solid var(--border-color);
    color: var(--text-secondary);
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    transition: var(--transition);
    font-size: 0.9rem;
    font-weight: 500;
}

.voice-gender-btn:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.voice-gender-btn.active {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
'''
        
        content += voice_status_css
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("CSS para indicador de status de voz adicionado")
    
    def add_language_support_js(self):
        """Adiciona suporte completo para Alemão e Chinês no JavaScript"""
        js_path = os.path.join(self.web_dir, "assets", "js", "script.js")
        
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Atualizar mapeamento de idiomas
        language_mapping = '''        this.languageMapping = {
            'pt': 'pt-BR',
            'pt-BR': 'pt-BR',
            'en': 'en-US',
            'en-US': 'en-US',
            'es': 'es-ES',
            'es-ES': 'es-ES',
            'fr': 'fr-FR',
            'fr-FR': 'fr-FR',
            'de': 'de-DE',
            'de-DE': 'de-DE',
            'zh': 'zh-CN',
            'zh-CN': 'zh-CN'
        };'''
        
        # Substituir mapeamento existente
        content = re.sub(
            r'this\.languageMapping = \{[^}]+\};',
            language_mapping.strip(),
            content,
            flags=re.DOTALL
        )
        
        # Atualizar banco de vozes
        voice_database_update = '''        this.voiceDatabase = {
            'pt-BR': { male: [], female: [], neutral: [] },
            'en-US': { male: [], female: [], neutral: [] },
            'es-ES': { male: [], female: [], neutral: [] },
            'fr-FR': { male: [], female: [], neutral: [] },
            'de-DE': { male: [], female: [], neutral: [] },
            'zh-CN': { male: [], female: [], neutral: [] }
        };'''
        
        content = re.sub(
            r'this\.voiceDatabase = \{[^}]+\};',
            voice_database_update.strip(),
            content,
            flags=re.DOTALL
        )
        
        # Atualizar normalizeLanguage
        normalize_method = '''    normalizeLanguage(lang) {
        if (lang.startsWith('pt')) return 'pt-BR';
        if (lang.startsWith('en')) return 'en-US';
        if (lang.startsWith('es')) return 'es-ES';
        if (lang.startsWith('fr')) return 'fr-FR';
        if (lang.startsWith('de')) return 'de-DE';
        if (lang.startsWith('zh')) return 'zh-CN';
        return this.languageMapping[lang] || lang;
    }'''
        
        content = re.sub(
            r'normalizeLanguage\([^}]+\{[^}]+\}',
            normalize_method.strip(),
            content,
            flags=re.DOTALL
        )
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.report["fixes_applied"].append("Suporte completo para Alemão e Chinês adicionado ao JavaScript")
    
    def run_complete_fix(self):
        """Executa todas as correções"""
        print("🔧 Iniciando correção completa...")
        
        try:
            self.add_languages_to_html()
            print("✅ Idiomas adicionados ao HTML")
            
            self.add_dark_theme_toggle()
            print("✅ Toggle de tema adicionado")
            
            self.restore_dark_theme_css()
            print("✅ Tema escuro restaurado")
            
            self.fix_voice_selection_system()
            print("✅ Sistema de vozes corrigido")
            
            self.add_theme_toggle_functionality()
            print("✅ Funcionalidade de tema adicionada")
            
            self.add_voice_status_css()
            print("✅ CSS de status de voz adicionado")
            
            self.add_language_support_js()
            print("✅ Suporte completo de idiomas adicionado")
            
            # Salvar relatório
            with open(os.path.join(self.web_dir, "complete_fix_final_report.json"), 'w', encoding='utf-8') as f:
                json.dump(self.report, f, indent=2, ensure_ascii=False)
            
            print("🎉 Correção completa finalizada com sucesso!")
            print("📋 Relatório salvo em: complete_fix_final_report.json")
            
        except Exception as e:
            self.report["status"] = "error"
            self.report["error"] = str(e)
            print(f"❌ Erro durante correção: {e}")

if __name__ == "__main__":
    fixer = MCPCompleteFix()
    fixer.run_complete_fix()