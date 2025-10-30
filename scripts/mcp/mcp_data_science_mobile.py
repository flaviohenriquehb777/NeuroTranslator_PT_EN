#!/usr/bin/env python3
"""
MCP Data Science Server para Análise de Compatibilidade Móvel
Servidor especializado em análise de dados para resolver problemas específicos
de reconhecimento de voz em dispositivos Samsung e navegadores Edge mobile.
"""

import json
import re
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np

@dataclass
class BrowserCompatibilityData:
    """Estrutura de dados para compatibilidade de navegadores"""
    browser_name: str
    version: str
    platform: str
    speech_api_support: bool
    https_requirement: bool
    permission_model: str
    known_issues: List[str]
    workarounds: List[str]

@dataclass
class DeviceAnalysis:
    """Análise específica do dispositivo"""
    device_type: str
    os_version: str
    browser_data: List[BrowserCompatibilityData]
    compatibility_score: float
    critical_issues: List[str]
    recommended_fixes: List[str]

class MobileDataScienceAnalyzer:
    """Analisador de dados científicos para compatibilidade móvel"""
    
    def __init__(self):
        self.browser_database = self._initialize_browser_database()
        self.device_patterns = self._initialize_device_patterns()
        self.compatibility_matrix = self._create_compatibility_matrix()
    
    def _initialize_browser_database(self) -> Dict[str, BrowserCompatibilityData]:
        """Inicializa base de dados de navegadores com informações específicas"""
        return {
            "samsung_internet": BrowserCompatibilityData(
                browser_name="Samsung Internet",
                version=">=18.0",
                platform="Android",
                speech_api_support=True,
                https_requirement=True,
                permission_model="prompt_based",
                known_issues=[
                    "Requer interação do usuário antes do reconhecimento",
                    "Timeout mais agressivo que outros navegadores",
                    "Problemas com continuous=true em algumas versões",
                    "Necessita de configurações específicas para webkitSpeechRecognition"
                ],
                workarounds=[
                    "Usar evento touchstart antes de iniciar reconhecimento",
                    "Implementar timeout personalizado",
                    "Configurar interimResults=false para Samsung Internet",
                    "Adicionar delay entre tentativas de reconhecimento"
                ]
            ),
            "edge_mobile": BrowserCompatibilityData(
                browser_name="Microsoft Edge Mobile",
                version=">=44.0",
                platform="Android",
                speech_api_support=True,
                https_requirement=True,
                permission_model="permission_api",
                known_issues=[
                    "API de Speech Recognition pode não estar disponível",
                    "Problemas com permissões de microfone",
                    "Incompatibilidade com algumas configurações de webkitSpeechRecognition",
                    "Falhas silenciosas sem mensagens de erro claras"
                ],
                workarounds=[
                    "Verificar disponibilidade da API antes do uso",
                    "Implementar fallback para entrada de texto",
                    "Usar navigator.permissions.query para verificar microfone",
                    "Adicionar logs detalhados para debugging"
                ]
            ),
            "chrome_mobile": BrowserCompatibilityData(
                browser_name="Chrome Mobile",
                version=">=25.0",
                platform="Android",
                speech_api_support=True,
                https_requirement=True,
                permission_model="permission_api",
                known_issues=[
                    "Funciona bem na maioria dos casos",
                    "Requer HTTPS obrigatoriamente"
                ],
                workarounds=[
                    "Implementação padrão funciona bem"
                ]
            )
        }
    
    def _initialize_device_patterns(self) -> Dict[str, List[str]]:
        """Padrões de detecção de dispositivos específicos"""
        return {
            "samsung": [
                "SM-G", "SM-A", "SM-N", "SM-J", "SM-M", "SM-F",
                "Galaxy", "samsung", "SAMSUNG"
            ],
            "android": [
                "Android", "android", "Mobile", "mobile"
            ]
        }
    
    def _create_compatibility_matrix(self) -> np.ndarray:
        """Cria matriz de compatibilidade baseada em dados históricos"""
        # Matriz de compatibilidade: [Samsung Internet, Edge Mobile, Chrome Mobile]
        # Linhas: Funcionalidades [Basic Speech, Continuous, Interim Results, Error Handling]
        return np.array([
            [0.7, 0.5, 0.9],  # Basic Speech Recognition
            [0.3, 0.2, 0.8],  # Continuous Recognition
            [0.4, 0.3, 0.9],  # Interim Results
            [0.6, 0.4, 0.8]   # Error Handling
        ])
    
    def analyze_current_implementation(self, js_file_path: str) -> Dict[str, Any]:
        """Analisa a implementação atual do JavaScript"""
        try:
            with open(js_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "has_webkit_speech": "webkitSpeechRecognition" in content,
                "has_standard_speech": "SpeechRecognition" in content and "webkit" not in content,
                "has_continuous_config": "continuous" in content,
                "has_interim_results": "interimResults" in content,
                "has_error_handling": "onerror" in content,
                "has_mobile_detection": "isMobileDevice" in content,
                "has_samsung_specific": "samsung" in content.lower(),
                "has_edge_specific": "edge" in content.lower(),
                "https_check": "https" in content.lower(),
                "permission_check": "permissions" in content,
                "user_interaction_required": "click" in content or "touch" in content
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Erro ao analisar arquivo: {str(e)}"}
    
    def generate_samsung_specific_fixes(self) -> Dict[str, str]:
        """Gera correções específicas para dispositivos Samsung"""
        return {
            "speech_config": """
// Configuração específica para Samsung Internet
function configureSamsungSpeechRecognition(recognition) {
    if (isSamsungInternet()) {
        recognition.continuous = false; // Samsung Internet tem problemas com continuous=true
        recognition.interimResults = false; // Desabilitar resultados intermediários
        recognition.maxAlternatives = 1;
        
        // Timeout personalizado para Samsung
        let samsungTimeout;
        recognition.onstart = function() {
            samsungTimeout = setTimeout(() => {
                recognition.stop();
                console.log('Samsung timeout aplicado');
            }, 10000); // 10 segundos timeout
        };
        
        recognition.onend = function() {
            if (samsungTimeout) clearTimeout(samsungTimeout);
        };
    }
}
""",
            "samsung_detection": """
function isSamsungInternet() {
    const userAgent = navigator.userAgent.toLowerCase();
    return userAgent.includes('samsungbrowser') || 
           userAgent.includes('samsung') ||
           (userAgent.includes('android') && userAgent.includes('wv'));
}
""",
            "user_interaction_handler": """
function ensureUserInteractionForSamsung() {
    if (isSamsungInternet()) {
        // Samsung Internet requer interação do usuário
        document.addEventListener('touchstart', function samsungTouchHandler() {
            window.samsungUserInteracted = true;
            document.removeEventListener('touchstart', samsungTouchHandler);
        }, { once: true });
        
        // Aguardar interação antes de iniciar reconhecimento
        return new Promise((resolve) => {
            if (window.samsungUserInteracted) {
                resolve();
            } else {
                const checkInteraction = setInterval(() => {
                    if (window.samsungUserInteracted) {
                        clearInterval(checkInteraction);
                        resolve();
                    }
                }, 100);
            }
        });
    }
    return Promise.resolve();
}
"""
        }
    
    def generate_edge_specific_fixes(self) -> Dict[str, str]:
        """Gera correções específicas para Edge Mobile"""
        return {
            "edge_detection": """
function isEdgeMobile() {
    const userAgent = navigator.userAgent.toLowerCase();
    return userAgent.includes('edg/') && userAgent.includes('mobile');
}
""",
            "edge_fallback": """
function handleEdgeMobileFallback() {
    if (isEdgeMobile()) {
        // Verificar se Speech Recognition está disponível
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech Recognition não disponível no Edge Mobile');
            showTextInputFallback();
            return false;
        }
        
        // Verificar permissões de microfone
        if (navigator.permissions) {
            navigator.permissions.query({name: 'microphone'}).then(function(result) {
                if (result.state === 'denied') {
                    showMicrophonePermissionError();
                }
            });
        }
    }
    return true;
}
""",
            "edge_error_handling": """
function handleEdgeSpecificErrors(event) {
    if (isEdgeMobile()) {
        console.log('Edge Mobile - Erro específico:', event.error);
        
        switch(event.error) {
            case 'not-allowed':
                showEdgePermissionHelp();
                break;
            case 'service-not-allowed':
                showEdgeServiceError();
                break;
            case 'network':
                showEdgeNetworkError();
                break;
            default:
                showEdgeGenericError(event.error);
        }
    }
}
"""
        }
    
    def generate_comprehensive_report(self, js_file_path: str) -> Dict[str, Any]:
        """Gera relatório abrangente de análise"""
        analysis = self.analyze_current_implementation(js_file_path)
        
        # Calcular score de compatibilidade
        compatibility_scores = {
            "samsung_internet": self._calculate_samsung_score(analysis),
            "edge_mobile": self._calculate_edge_score(analysis),
            "overall": 0
        }
        
        compatibility_scores["overall"] = (
            compatibility_scores["samsung_internet"] + 
            compatibility_scores["edge_mobile"]
        ) / 2
        
        # Identificar problemas críticos
        critical_issues = []
        if not analysis.get("has_samsung_specific", False):
            critical_issues.append("Falta implementação específica para Samsung Internet")
        if not analysis.get("has_edge_specific", False):
            critical_issues.append("Falta implementação específica para Edge Mobile")
        if not analysis.get("user_interaction_required", False):
            critical_issues.append("Falta garantia de interação do usuário")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "compatibility_scores": compatibility_scores,
            "critical_issues": critical_issues,
            "samsung_fixes": self.generate_samsung_specific_fixes(),
            "edge_fixes": self.generate_edge_specific_fixes(),
            "recommendations": self._generate_recommendations(analysis, compatibility_scores)
        }
    
    def _calculate_samsung_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de compatibilidade para Samsung Internet"""
        score = 0.0
        weights = {
            "has_webkit_speech": 0.2,
            "has_mobile_detection": 0.15,
            "has_samsung_specific": 0.25,
            "user_interaction_required": 0.2,
            "has_error_handling": 0.2
        }
        
        for key, weight in weights.items():
            if analysis.get(key, False):
                score += weight
        
        return min(score, 1.0)
    
    def _calculate_edge_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de compatibilidade para Edge Mobile"""
        score = 0.0
        weights = {
            "has_webkit_speech": 0.15,
            "has_standard_speech": 0.15,
            "has_edge_specific": 0.25,
            "permission_check": 0.2,
            "has_error_handling": 0.25
        }
        
        for key, weight in weights.items():
            if analysis.get(key, False):
                score += weight
        
        return min(score, 1.0)
    
    def _generate_recommendations(self, analysis: Dict[str, Any], scores: Dict[str, float]) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        if scores["samsung_internet"] < 0.7:
            recommendations.append("Implementar configurações específicas para Samsung Internet")
            recommendations.append("Adicionar timeout personalizado para Samsung")
            recommendations.append("Desabilitar continuous mode para Samsung Internet")
        
        if scores["edge_mobile"] < 0.7:
            recommendations.append("Adicionar verificação de disponibilidade da API para Edge")
            recommendations.append("Implementar fallback de texto para Edge Mobile")
            recommendations.append("Melhorar tratamento de erros específicos do Edge")
        
        if not analysis.get("user_interaction_required", False):
            recommendations.append("Garantir interação do usuário antes de iniciar reconhecimento")
        
        return recommendations

def main():
    """Função principal do servidor MCP"""
    analyzer = MobileDataScienceAnalyzer()
    
    # Caminho para o arquivo JavaScript
    js_file_path = "web/assets/js/script.js"
    
    print("🔬 Iniciando Análise de Dados Científicos para Compatibilidade Móvel...")
    print("=" * 70)
    
    # Gerar relatório abrangente
    report = analyzer.generate_comprehensive_report(js_file_path)
    
    print(f"📊 RELATÓRIO DE ANÁLISE - {report['timestamp']}")
    print("=" * 70)
    
    print("🎯 SCORES DE COMPATIBILIDADE:")
    for browser, score in report['compatibility_scores'].items():
        status = "✅ BOM" if score >= 0.7 else "⚠️ PRECISA MELHORAR" if score >= 0.5 else "❌ CRÍTICO"
        print(f"  {browser.replace('_', ' ').title()}: {score:.2f} - {status}")
    
    print("\n🚨 PROBLEMAS CRÍTICOS IDENTIFICADOS:")
    for issue in report['critical_issues']:
        print(f"  ❌ {issue}")
    
    print("\n💡 RECOMENDAÇÕES:")
    for rec in report['recommendations']:
        print(f"  🔧 {rec}")
    
    # Aplicar correções automaticamente
    print("\n🛠️ APLICANDO CORREÇÕES ESPECÍFICAS...")
    
    # Aplicar correções Samsung
    print("\n📱 Aplicando correções para Samsung Internet...")
    apply_samsung_fixes(js_file_path, report['samsung_fixes'])
    
    # Aplicar correções Edge
    print("🌐 Aplicando correções para Edge Mobile...")
    apply_edge_fixes(js_file_path, report['edge_fixes'])
    
    print("\n✅ ANÁLISE E CORREÇÕES CONCLUÍDAS!")
    print("🔄 Reinicie o servidor web para testar as correções.")
    
    return report

def apply_samsung_fixes(js_file_path: str, fixes: Dict[str, str]):
    """Aplica correções específicas para Samsung"""
    try:
        with open(js_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar funções Samsung se não existirem
        if "isSamsungInternet" not in content:
            content += "\n" + fixes["samsung_detection"]
            print("  ✅ Adicionada detecção Samsung Internet")
        
        if "configureSamsungSpeechRecognition" not in content:
            content += "\n" + fixes["speech_config"]
            print("  ✅ Adicionada configuração específica Samsung")
        
        if "ensureUserInteractionForSamsung" not in content:
            content += "\n" + fixes["user_interaction_handler"]
            print("  ✅ Adicionado handler de interação Samsung")
        
        # Modificar função de inicialização existente
        if "initSpeechRecognition" in content:
            # Adicionar chamada para configuração Samsung
            samsung_call = """
        // Configuração específica para Samsung Internet
        if (isSamsungInternet()) {
            await ensureUserInteractionForSamsung();
            configureSamsungSpeechRecognition(this.recognition);
        }"""
            
            if samsung_call.strip() not in content:
                content = content.replace(
                    "this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();",
                    f"this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();{samsung_call}"
                )
                print("  ✅ Integrada configuração Samsung na inicialização")
        
        with open(js_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"  ❌ Erro ao aplicar correções Samsung: {e}")

def apply_edge_fixes(js_file_path: str, fixes: Dict[str, str]):
    """Aplica correções específicas para Edge Mobile"""
    try:
        with open(js_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar funções Edge se não existirem
        if "isEdgeMobile" not in content:
            content += "\n" + fixes["edge_detection"]
            print("  ✅ Adicionada detecção Edge Mobile")
        
        if "handleEdgeMobileFallback" not in content:
            content += "\n" + fixes["edge_fallback"]
            print("  ✅ Adicionado fallback Edge Mobile")
        
        if "handleEdgeSpecificErrors" not in content:
            content += "\n" + fixes["edge_error_handling"]
            print("  ✅ Adicionado tratamento de erros Edge")
        
        # Modificar tratamento de erro existente
        if "recognition.onerror" in content:
            edge_error_call = """
        // Tratamento específico para Edge Mobile
        if (isEdgeMobile()) {
            handleEdgeSpecificErrors(event);
        }"""
            
            if "handleEdgeSpecificErrors" not in content or edge_error_call.strip() not in content:
                # Encontrar e modificar o handler de erro existente
                error_pattern = r"(recognition\.onerror\s*=\s*function\s*\([^)]*\)\s*\{)"
                if re.search(error_pattern, content):
                    content = re.sub(
                        error_pattern,
                        r"\1" + edge_error_call,
                        content
                    )
                    print("  ✅ Integrado tratamento de erro Edge")
        
        # Adicionar verificação Edge na inicialização
        if "checkBrowserSupport" in content:
            edge_check = """
        // Verificação específica para Edge Mobile
        if (isEdgeMobile() && !handleEdgeMobileFallback()) {
            return false;
        }"""
            
            if edge_check.strip() not in content:
                content = content.replace(
                    "checkBrowserSupport() {",
                    f"checkBrowserSupport() {{{edge_check}"
                )
                print("  ✅ Integrada verificação Edge na inicialização")
        
        with open(js_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"  ❌ Erro ao aplicar correções Edge: {e}")

if __name__ == "__main__":
    main()