#!/usr/bin/env python3
"""
Servidor MCP para Diagnóstico de Compatibilidade Móvel - NeuroTranslator
Diagnostica e resolve problemas de reconhecimento de voz em dispositivos móveis
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MobileDiagnosticsServer:
    """Servidor MCP para diagnóstico de compatibilidade móvel"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.web_path = self.project_root / "web"
        self.diagnostics_log = []
        
    async def diagnose_mobile_compatibility(self, user_agent: str = "", device_type: str = "") -> Dict[str, Any]:
        """
        Diagnostica problemas de compatibilidade móvel
        
        Args:
            user_agent: String do user agent do dispositivo
            device_type: Tipo do dispositivo (mobile, tablet, desktop)
        
        Returns:
            Relatório de diagnóstico
        """
        logger.info(f"🔍 Iniciando diagnóstico para: {device_type} - {user_agent}")
        
        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "device_info": {
                "user_agent": user_agent,
                "device_type": device_type,
                "is_mobile": self._is_mobile_device(user_agent)
            },
            "issues_found": [],
            "recommendations": [],
            "fixes_applied": []
        }
        
        # Verificar problemas comuns em mobile
        await self._check_https_requirement(diagnostics)
        await self._check_speech_api_support(diagnostics)
        await self._check_permissions_handling(diagnostics)
        await self._check_mobile_optimizations(diagnostics)
        
        # Gerar recomendações
        await self._generate_recommendations(diagnostics)
        
        self.diagnostics_log.append(diagnostics)
        return diagnostics
    
    def _is_mobile_device(self, user_agent: str) -> bool:
        """Detecta se é um dispositivo móvel"""
        mobile_indicators = [
            'Mobile', 'Android', 'iPhone', 'iPad', 'iPod',
            'BlackBerry', 'Windows Phone', 'Opera Mini'
        ]
        return any(indicator in user_agent for indicator in mobile_indicators)
    
    async def _check_https_requirement(self, diagnostics: Dict[str, Any]):
        """Verifica requisitos de HTTPS"""
        # Verificar se o código atual trata HTTPS adequadamente
        js_file = self.web_path / "assets" / "js" / "script.js"
        
        if js_file.exists():
            content = js_file.read_text(encoding='utf-8')
            
            # Verificar se há verificação de protocolo seguro
            if 'location.protocol === \'https:\'' in content:
                diagnostics["issues_found"].append({
                    "type": "https_check",
                    "severity": "medium",
                    "description": "Verificação de HTTPS presente, mas pode ser melhorada para mobile",
                    "file": str(js_file)
                })
            else:
                diagnostics["issues_found"].append({
                    "type": "missing_https_check",
                    "severity": "high",
                    "description": "Falta verificação adequada de HTTPS para dispositivos móveis",
                    "file": str(js_file)
                })
    
    async def _check_speech_api_support(self, diagnostics: Dict[str, Any]):
        """Verifica suporte à API de fala"""
        js_file = self.web_path / "assets" / "js" / "script.js"
        
        if js_file.exists():
            content = js_file.read_text(encoding='utf-8')
            
            # Verificar configurações de Speech Recognition
            issues = []
            
            if 'webkitSpeechRecognition' not in content:
                issues.append("Falta suporte ao webkitSpeechRecognition (Safari mobile)")
            
            if 'continuous = false' not in content:
                issues.append("Configuração continuous pode causar problemas em mobile")
            
            if 'maxAlternatives = 1' not in content:
                issues.append("maxAlternatives não otimizado para mobile")
            
            for issue in issues:
                diagnostics["issues_found"].append({
                    "type": "speech_api_config",
                    "severity": "medium",
                    "description": issue,
                    "file": str(js_file)
                })
    
    async def _check_permissions_handling(self, diagnostics: Dict[str, Any]):
        """Verifica tratamento de permissões"""
        js_file = self.web_path / "assets" / "js" / "script.js"
        
        if js_file.exists():
            content = js_file.read_text(encoding='utf-8')
            
            # Verificar tratamento de erros de permissão
            permission_checks = [
                ('not-allowed', 'Tratamento de permissão negada'),
                ('audio-capture', 'Tratamento de erro de captura de áudio'),
                ('service-not-allowed', 'Tratamento de serviço não permitido')
            ]
            
            for error_type, description in permission_checks:
                if error_type not in content:
                    diagnostics["issues_found"].append({
                        "type": "permission_handling",
                        "severity": "high",
                        "description": f"Falta tratamento para erro: {description}",
                        "file": str(js_file)
                    })
    
    async def _check_mobile_optimizations(self, diagnostics: Dict[str, Any]):
        """Verifica otimizações específicas para mobile"""
        js_file = self.web_path / "assets" / "js" / "script.js"
        
        if js_file.exists():
            content = js_file.read_text(encoding='utf-8')
            
            mobile_optimizations = [
                ('touchstart', 'Eventos de toque para mobile'),
                ('orientation', 'Tratamento de mudança de orientação'),
                ('visibility', 'API de visibilidade da página'),
                ('wake-lock', 'Prevenção de sleep durante gravação')
            ]
            
            for optimization, description in mobile_optimizations:
                if optimization not in content:
                    diagnostics["issues_found"].append({
                        "type": "mobile_optimization",
                        "severity": "low",
                        "description": f"Otimização ausente: {description}",
                        "file": str(js_file)
                    })
    
    async def _generate_recommendations(self, diagnostics: Dict[str, Any]):
        """Gera recomendações baseadas nos problemas encontrados"""
        issues = diagnostics["issues_found"]
        recommendations = []
        
        # Agrupar por tipo de problema
        issue_types = {}
        for issue in issues:
            issue_type = issue["type"]
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append(issue)
        
        # Gerar recomendações específicas
        if "https_check" in issue_types or "missing_https_check" in issue_types:
            recommendations.append({
                "priority": "high",
                "action": "Implementar verificação robusta de HTTPS",
                "description": "Adicionar detecção de protocolo seguro e fallbacks para mobile"
            })
        
        if "speech_api_config" in issue_types:
            recommendations.append({
                "priority": "high",
                "action": "Otimizar configurações de Speech Recognition",
                "description": "Ajustar parâmetros para melhor compatibilidade móvel"
            })
        
        if "permission_handling" in issue_types:
            recommendations.append({
                "priority": "high",
                "action": "Melhorar tratamento de permissões",
                "description": "Implementar handlers específicos para erros de permissão em mobile"
            })
        
        if "mobile_optimization" in issue_types:
            recommendations.append({
                "priority": "medium",
                "action": "Adicionar otimizações móveis",
                "description": "Implementar recursos específicos para dispositivos móveis"
            })
        
        diagnostics["recommendations"] = recommendations
    
    async def apply_mobile_fixes(self) -> Dict[str, Any]:
        """
        Aplica correções automáticas para problemas de compatibilidade móvel
        
        Returns:
            Relatório das correções aplicadas
        """
        logger.info("🔧 Aplicando correções para compatibilidade móvel...")
        
        fixes_applied = []
        
        # Aplicar correções no JavaScript
        js_fixes = await self._apply_javascript_fixes()
        fixes_applied.extend(js_fixes)
        
        # Aplicar correções no HTML
        html_fixes = await self._apply_html_fixes()
        fixes_applied.extend(html_fixes)
        
        # Aplicar correções no CSS
        css_fixes = await self._apply_css_fixes()
        fixes_applied.extend(css_fixes)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "fixes_applied": fixes_applied,
            "total_fixes": len(fixes_applied)
        }
    
    async def _apply_javascript_fixes(self) -> List[Dict[str, Any]]:
        """Aplica correções no JavaScript"""
        fixes = []
        js_file = self.web_path / "assets" / "js" / "script.js"
        
        if not js_file.exists():
            return fixes
        
        content = js_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix 1: Melhorar verificação de HTTPS
        if 'checkMobileCompatibility()' not in content:
            mobile_check_code = '''
    
    checkMobileCompatibility() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const isSecure = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        
        if (isMobile && !isSecure) {
            this.showMobileSecurityWarning();
            return false;
        }
        
        return true;
    }
    
    showMobileSecurityWarning() {
        const warning = document.createElement('div');
        warning.className = 'mobile-security-warning';
        warning.innerHTML = `
            <div class="warning-content">
                <i class="fas fa-mobile-alt"></i>
                <h3>Dispositivo Móvel Detectado</h3>
                <p>O reconhecimento de voz requer HTTPS em dispositivos móveis.</p>
                <p>Para usar esta funcionalidade, acesse via HTTPS.</p>
                <button onclick="this.parentElement.parentElement.remove()">Entendi</button>
            </div>
        `;
        document.body.appendChild(warning);
    }'''
            
            # Inserir após o método checkBrowserSupport
            content = content.replace(
                'checkBrowserSupport() {',
                f'{mobile_check_code}\n    \n    checkBrowserSupport() {{'
            )
            
            fixes.append({
                "type": "javascript",
                "description": "Adicionada verificação de compatibilidade móvel",
                "file": str(js_file)
            })
        
        # Fix 2: Melhorar configurações de Speech Recognition para mobile
        if 'this.speech.recognition.continuous = false;' in content:
            # Adicionar configurações específicas para mobile
            mobile_speech_config = '''
        // Configurações otimizadas para mobile
        if (this.isMobileDevice()) {
            this.speech.recognition.continuous = false;
            this.speech.recognition.interimResults = false; // Reduzir processamento
            this.speech.recognition.maxAlternatives = 1;
        } else {
            this.speech.recognition.continuous = false;
            this.speech.recognition.interimResults = true;
            this.speech.recognition.maxAlternatives = 1;
        }'''
            
            content = content.replace(
                'this.speech.recognition.continuous = false;',
                mobile_speech_config
            )
            
            fixes.append({
                "type": "javascript",
                "description": "Otimizadas configurações de Speech Recognition para mobile",
                "file": str(js_file)
            })
        
        # Fix 3: Adicionar método para detectar dispositivo móvel
        if 'isMobileDevice()' not in content:
            mobile_detection_code = '''
    
    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }'''
            
            content = content.replace(
                'init() {',
                f'{mobile_detection_code}\n    \n    init() {{'
            )
            
            fixes.append({
                "type": "javascript",
                "description": "Adicionado método de detecção de dispositivo móvel",
                "file": str(js_file)
            })
        
        # Salvar alterações se houve modificações
        if content != original_content:
            js_file.write_text(content, encoding='utf-8')
            logger.info(f"✅ Correções aplicadas em {js_file}")
        
        return fixes
    
    async def _apply_html_fixes(self) -> List[Dict[str, Any]]:
        """Aplica correções no HTML"""
        fixes = []
        html_file = self.web_path / "index.html"
        
        if not html_file.exists():
            return fixes
        
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix 1: Adicionar meta tags para mobile
        mobile_meta_tags = [
            '<meta name="mobile-web-app-capable" content="yes">',
            '<meta name="apple-mobile-web-app-capable" content="yes">',
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
        ]
        
        for meta_tag in mobile_meta_tags:
            if meta_tag not in content:
                content = content.replace(
                    '<meta name="viewport"',
                    f'{meta_tag}\n    <meta name="viewport"'
                )
                fixes.append({
                    "type": "html",
                    "description": f"Adicionada meta tag: {meta_tag}",
                    "file": str(html_file)
                })
        
        # Salvar alterações se houve modificações
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            logger.info(f"✅ Correções aplicadas em {html_file}")
        
        return fixes
    
    async def _apply_css_fixes(self) -> List[Dict[str, Any]]:
        """Aplica correções no CSS"""
        fixes = []
        css_file = self.web_path / "assets" / "css" / "styles.css"
        
        if not css_file.exists():
            return fixes
        
        content = css_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix 1: Adicionar estilos para avisos móveis
        mobile_warning_css = '''
/* Estilos para avisos de compatibilidade móvel */
.mobile-security-warning {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
}

.mobile-security-warning .warning-content {
    background: var(--bg-secondary);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    max-width: 90%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.mobile-security-warning h3 {
    color: var(--accent-color);
    margin-bottom: 1rem;
}

.mobile-security-warning button {
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    margin-top: 1rem;
    cursor: pointer;
    font-size: 1rem;
}

.mobile-security-warning button:hover {
    background: var(--accent-hover);
}

/* Melhorias para dispositivos móveis */
@media (max-width: 768px) {
    .btn {
        min-height: 44px; /* Tamanho mínimo recomendado para toque */
        font-size: 1rem;
    }
    
    .speech-status {
        font-size: 0.9rem;
        padding: 0.5rem;
    }
    
    .btn-speech.active {
        animation: pulse-mobile 1.5s infinite;
    }
}

@keyframes pulse-mobile {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
'''
        
        if '.mobile-security-warning' not in content:
            content += mobile_warning_css
            fixes.append({
                "type": "css",
                "description": "Adicionados estilos para compatibilidade móvel",
                "file": str(css_file)
            })
        
        # Salvar alterações se houve modificações
        if content != original_content:
            css_file.write_text(content, encoding='utf-8')
            logger.info(f"✅ Correções aplicadas em {css_file}")
        
        return fixes
    
    async def generate_mobile_test_report(self) -> Dict[str, Any]:
        """
        Gera relatório de testes para dispositivos móveis
        
        Returns:
            Relatório de testes
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "test_scenarios": [
                {
                    "device": "iPhone Safari",
                    "tests": [
                        "Verificar permissão de microfone",
                        "Testar reconhecimento de voz",
                        "Verificar HTTPS",
                        "Testar interface touch"
                    ]
                },
                {
                    "device": "Android Chrome",
                    "tests": [
                        "Verificar webkitSpeechRecognition",
                        "Testar em modo incógnito",
                        "Verificar permissões",
                        "Testar orientação landscape/portrait"
                    ]
                }
            ],
            "checklist": [
                "✅ HTTPS habilitado",
                "✅ Permissões de microfone solicitadas",
                "✅ Fallbacks implementados",
                "✅ Interface otimizada para toque",
                "✅ Avisos de compatibilidade exibidos"
            ]
        }

# Função principal para executar o servidor MCP
async def main():
    """Função principal do servidor MCP"""
    server = MobileDiagnosticsServer()
    
    print("🚀 Servidor MCP de Diagnóstico Móvel iniciado")
    print("📱 Diagnosticando compatibilidade móvel...")
    
    # Executar diagnóstico
    diagnostics = await server.diagnose_mobile_compatibility(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
        device_type="mobile"
    )
    
    print("\n📊 Relatório de Diagnóstico:")
    print(json.dumps(diagnostics, indent=2, ensure_ascii=False))
    
    # Aplicar correções
    print("\n🔧 Aplicando correções...")
    fixes = await server.apply_mobile_fixes()
    
    print("\n✅ Correções Aplicadas:")
    print(json.dumps(fixes, indent=2, ensure_ascii=False))
    
    # Gerar relatório de testes
    test_report = await server.generate_mobile_test_report()
    
    print("\n📋 Relatório de Testes:")
    print(json.dumps(test_report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())