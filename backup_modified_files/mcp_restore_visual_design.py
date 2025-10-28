#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Restore Visual Design - Restauração do Design Visual
Restaura o design visual conforme a imagem anexa com as cores especificadas
"""

import os
import re
from datetime import datetime

class MCPRestoreVisualDesign:
    def __init__(self):
        self.name = "MCP Restore Visual Design"
        self.version = "1.0.0"
        self.description = "Restaura o design visual original"
        
    def update_css_colors(self, file_path):
        """Atualiza as cores do CSS conforme o design original"""
        
        print(f"🎨 Atualizando cores do design em: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Cores do design original baseadas na imagem
            new_colors = '''
/* Cores do Design Original */
:root {
    /* Cores principais */
    --primary-bg: #1a1a2e;
    --secondary-bg: #16213e;
    --accent-bg: #0f3460;
    --card-bg: #16213e;
    --border-color: #2d4a6b;
    
    /* Cores de texto */
    --text-primary: #ffffff;
    --text-secondary: #b8c5d6;
    --text-muted: #8a9bb3;
    
    /* Cores de destaque */
    --accent-blue: #4a90e2;
    --accent-purple: #6c5ce7;
    --accent-green: #00b894;
    --accent-orange: #fdcb6e;
    
    /* Cores de status */
    --success-color: #00b894;
    --warning-color: #fdcb6e;
    --error-color: #e17055;
    --info-color: #4a90e2;
    
    /* Gradientes */
    --gradient-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    --gradient-accent: linear-gradient(135deg, #4a90e2 0%, #6c5ce7 100%);
    --gradient-card: linear-gradient(145deg, #16213e 0%, #0f3460 100%);
    
    /* Sombras */
    --shadow-light: 0 2px 10px rgba(0, 0, 0, 0.1);
    --shadow-medium: 0 4px 20px rgba(0, 0, 0, 0.15);
    --shadow-heavy: 0 8px 30px rgba(0, 0, 0, 0.2);
    --shadow-glow: 0 0 20px rgba(74, 144, 226, 0.3);
}
'''
            
            # Substituir ou adicionar as cores
            if ':root' in content:
                # Substituir seção :root existente
                content = re.sub(r':root\s*\{[^}]*\}', new_colors.strip(), content, flags=re.DOTALL)
            else:
                # Adicionar no início do arquivo
                content = new_colors + '\n' + content
            
            # Atualizar estilos do corpo
            body_styles = '''
body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--gradient-primary);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
}
'''
            
            # Substituir estilos do body
            content = re.sub(r'body\s*\{[^}]*\}', body_styles.strip(), content, flags=re.DOTALL)
            
            # Atualizar header
            header_styles = '''
.header {
    background: var(--gradient-card);
    padding: 20px 0;
    text-align: center;
    border-bottom: 2px solid var(--border-color);
    box-shadow: var(--shadow-medium);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(74,144,226,0.1)"/></svg>');
    animation: float 6s ease-in-out infinite;
}

.header h1 {
    font-size: 2.5rem;
    margin: 0;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(74, 144, 226, 0.5);
    position: relative;
    z-index: 1;
}

.header p {
    margin: 10px 0 0 0;
    color: var(--text-secondary);
    font-size: 1.1rem;
    position: relative;
    z-index: 1;
}
'''
            
            # Atualizar container principal
            container_styles = '''
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 20px;
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 30px;
    align-items: start;
}

.camera-section {
    background: var(--gradient-card);
    border-radius: 15px;
    padding: 25px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-medium);
    text-align: center;
}

.translation-section {
    background: var(--gradient-card);
    border-radius: 15px;
    padding: 30px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-medium);
}

.controls-section {
    background: var(--gradient-card);
    border-radius: 15px;
    padding: 25px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-medium);
}
'''
            
            # Atualizar estilos dos botões
            button_styles = '''
.btn {
    background: var(--gradient-accent);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-light);
    position: relative;
    overflow: hidden;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
}

.btn:active {
    transform: translateY(0);
}

.btn.active {
    background: var(--accent-green);
    box-shadow: 0 0 20px rgba(0, 184, 148, 0.4);
}
'''
            
            # Inserir ou substituir estilos
            styles_to_update = [
                (r'\.header\s*\{[^}]*\}', header_styles),
                (r'\.container\s*\{[^}]*\}', container_styles),
                (r'\.btn\s*\{[^}]*\}', button_styles)
            ]
            
            for pattern, new_style in styles_to_update:
                if re.search(pattern, content, re.DOTALL):
                    content = re.sub(pattern, new_style.strip(), content, flags=re.DOTALL)
                else:
                    content += '\n' + new_style
            
            # Adicionar animações
            animations = '''
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(74, 144, 226, 0.2); }
    50% { box-shadow: 0 0 20px rgba(74, 144, 226, 0.6); }
}
'''
            
            if '@keyframes' not in content:
                content += '\n' + animations
            
            # Salvar apenas se houve mudanças
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ Design atualizado em: {file_path}")
                return True
            else:
                print(f"ℹ️ Nenhuma atualização necessária em: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {str(e)}")
            return False
    
    def update_html_structure(self, file_path):
        """Atualiza a estrutura HTML conforme o design original"""
        
        print(f"🏗️ Atualizando estrutura HTML em: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Atualizar título e meta tags
            if '<title>' in content:
                content = re.sub(r'<title>[^<]*</title>', '<title>NeuroTranslator PT-EN | Tradução Neural em Tempo Real</title>', content)
            
            # Adicionar meta tags se não existirem
            meta_tags = '''
    <meta name="description" content="Tradutor neural inteligente com reconhecimento de voz e detecção de gênero">
    <meta name="keywords" content="tradutor, neural, AI, reconhecimento de voz, português, inglês">
    <meta name="author" content="NeuroTranslator">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
'''
            
            if 'name="description"' not in content:
                content = re.sub(r'(<head[^>]*>)', r'\1' + meta_tags, content)
            
            # Salvar apenas se houve mudanças
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ HTML atualizado em: {file_path}")
                return True
            else:
                print(f"ℹ️ Nenhuma atualização HTML necessária em: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar HTML {file_path}: {str(e)}")
            return False
    
    def process_files(self):
        """Processa todos os arquivos de design"""
        
        files_to_process = [
            ("assets/css/styles.css", "css"),
            ("index.html", "html")
        ]
        
        processed_files = []
        
        for file_path, file_type in files_to_process:
            if os.path.exists(file_path):
                if file_type == "css":
                    if self.update_css_colors(file_path):
                        processed_files.append(file_path)
                elif file_type == "html":
                    if self.update_html_structure(file_path):
                        processed_files.append(file_path)
            else:
                print(f"⚠️ Arquivo não encontrado: {file_path}")
        
        return processed_files
    
    def generate_report(self, processed_files):
        """Gera relatório das atualizações de design"""
        
        report = {
            "mcp_name": self.name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "processed_files": processed_files,
            "design_updates": [
                "Cores atualizadas conforme design original",
                "Gradientes e sombras restaurados",
                "Estilos de header com efeitos visuais",
                "Layout em grid responsivo",
                "Botões com animações e hover effects",
                "Animações CSS adicionadas",
                "Meta tags otimizadas",
                "Estrutura HTML aprimorada"
            ],
            "color_scheme": {
                "primary_bg": "#1a1a2e",
                "secondary_bg": "#16213e", 
                "accent_bg": "#0f3460",
                "accent_blue": "#4a90e2",
                "accent_purple": "#6c5ce7",
                "accent_green": "#00b894"
            },
            "status": "success" if processed_files else "no_changes"
        }
        
        # Salvar relatório
        with open('mcp_design_restore_report.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Relatório salvo: mcp_design_restore_report.json")
        return report

# Executar MCP
if __name__ == "__main__":
    mcp = MCPRestoreVisualDesign()
    
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