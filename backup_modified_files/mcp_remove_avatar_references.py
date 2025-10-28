#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Remove Avatar References - Remoção de Referências do Avatar
Remove completamente todas as referências ao sistema de avatar dos arquivos JavaScript
"""

import os
import re
from datetime import datetime

class MCPRemoveAvatarReferences:
    def __init__(self):
        self.name = "MCP Remove Avatar References"
        self.version = "1.0.0"
        self.description = "Remove todas as referências ao sistema de avatar"
        
    def remove_avatar_references(self, file_path):
        """Remove todas as referências ao avatar de um arquivo JavaScript"""
        
        print(f"🧹 Removendo referências do avatar de: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Remover inicialização do avatar system
            content = re.sub(r'if\s*\(\s*window\.NeuroAvatarSystem\s*\)\s*\{[^}]*await\s+this\.initModule\([^}]*\}', '', content, flags=re.DOTALL)
            
            # Remover event listeners do avatar
            content = re.sub(r"document\.addEventListener\(\s*['\"]avatar-system-initialized['\"][^}]*\};?\s*\);?", '', content, flags=re.DOTALL)
            
            # Remover métodos do avatar
            avatar_methods = [
                'handleAvatarReady',
                'activateAvatar', 
                'deactivateAvatar',
                'setupAvatarSync'
            ]
            
            for method in avatar_methods:
                # Remover definição do método
                pattern = rf'{method}\s*\([^{{]*\{{[^}}]*\}}'
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                # Remover chamadas do método
                pattern = rf'this\.{method}\([^;]*\);?'
                content = re.sub(pattern, '', content)
            
            # Remover condicionais do avatar
            content = re.sub(r'if\s*\(\s*this\.modules\.avatarSystem[^}]*\}', '', content, flags=re.DOTALL)
            content = re.sub(r'if\s*\(\s*this\.modules\.avatarSystem[^;]*;', '', content)
            
            # Remover configurações do avatar
            content = re.sub(r'if\s*\(\s*this\.config\.autoActivateAvatar[^}]*\}', '', content, flags=re.DOTALL)
            
            # Remover chamadas específicas do avatar
            content = re.sub(r'this\.modules\.avatarSystem\.[^;]*;', '', content)
            content = re.sub(r'this\.state\.avatarActive[^;]*;', '', content)
            
            # Remover testes do avatar
            content = re.sub(r'if\s*\(\s*this\.modules\.avatarSystem\s*\)\s*\{[^}]*results\.avatarTest[^}]*\}', '', content, flags=re.DOTALL)
            
            # Remover linhas vazias extras
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = re.sub(r'\{\s*\n\s*\n\s*\}', '{}', content)
            
            # Salvar apenas se houve mudanças
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ Referências do avatar removidas de: {file_path}")
                return True
            else:
                print(f"ℹ️ Nenhuma referência do avatar encontrada em: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {str(e)}")
            return False
    
    def process_all_files(self):
        """Processa todos os arquivos JavaScript relevantes"""
        
        js_files = [
            "assets/js/ai-integration.js",
            "assets/js/ai-voice-vision.js",
            "assets/js/script.js"
        ]
        
        processed_files = []
        
        for js_file in js_files:
            if os.path.exists(js_file):
                if self.remove_avatar_references(js_file):
                    processed_files.append(js_file)
            else:
                print(f"⚠️ Arquivo não encontrado: {js_file}")
        
        return processed_files
    
    def generate_report(self, processed_files):
        """Gera relatório das modificações"""
        
        report = {
            "mcp_name": self.name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "processed_files": processed_files,
            "removed_references": [
                "window.NeuroAvatarSystem initialization",
                "avatar-system-initialized event listeners",
                "handleAvatarReady method",
                "activateAvatar method",
                "deactivateAvatar method", 
                "setupAvatarSync method",
                "avatarSystem module references",
                "avatarActive state references",
                "autoActivateAvatar config references",
                "Avatar test conditions"
            ],
            "status": "success" if processed_files else "no_changes"
        }
        
        # Salvar relatório
        with open('mcp_remove_avatar_report.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Relatório salvo: mcp_remove_avatar_report.json")
        return report

# Executar MCP
if __name__ == "__main__":
    mcp = MCPRemoveAvatarReferences()
    
    print(f"🚀 Iniciando {mcp.name}...")
    
    processed_files = mcp.process_all_files()
    report = mcp.generate_report(processed_files)
    
    if processed_files:
        print(f"🎉 {mcp.name} concluído com sucesso!")
        print(f"📁 Arquivos processados: {len(processed_files)}")
        for file in processed_files:
            print(f"   - {file}")
    else:
        print(f"ℹ️ {mcp.name} concluído - nenhuma alteração necessária")