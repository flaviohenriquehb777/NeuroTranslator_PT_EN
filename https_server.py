#!/usr/bin/env python3
"""
Servidor HTTPS local para testar reconhecimento de voz em dispositivos móveis.
O reconhecimento de voz requer HTTPS em dispositivos móveis por questões de segurança.
"""

import http.server
import ssl
import socketserver
import os
import sys
from pathlib import Path

# Configurações do servidor
PORT = 8443
DIRECTORY = "web"

class HTTPSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Adicionar headers de segurança para HTTPS
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

def create_self_signed_cert():
    """Cria certificado auto-assinado para desenvolvimento local"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        import ipaddress
        
        print("📜 Criando certificado auto-assinado...")
        
        # Gerar chave privada
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Criar certificado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Development"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "NeuroTranslator"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Salvar certificado e chave
        with open("server.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("server.key", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Certificado criado com sucesso!")
        return True
        
    except ImportError:
        print("❌ Biblioteca 'cryptography' não encontrada.")
        print("💡 Instalando automaticamente...")
        
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
            print("✅ Biblioteca instalada! Reinicie o script.")
            return False
        except subprocess.CalledProcessError:
            print("❌ Falha ao instalar cryptography.")
            return False
    except Exception as e:
        print(f"❌ Erro ao criar certificado: {e}")
        return False

def start_https_server():
    """Inicia servidor HTTPS local"""
    
    # Verificar se o diretório web existe
    if not os.path.exists(DIRECTORY):
        print(f"❌ Diretório '{DIRECTORY}' não encontrado!")
        return False
    
    # Verificar/criar certificados
    if not (os.path.exists("server.crt") and os.path.exists("server.key")):
        print("🔐 Certificados não encontrados. Criando...")
        if not create_self_signed_cert():
            return False
    
    try:
        # Configurar servidor HTTPS
        with socketserver.TCPServer(("", PORT), HTTPSHandler) as httpd:
            # Configurar SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain("server.crt", "server.key")
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print("🚀 Servidor HTTPS iniciado!")
            print(f"📱 Acesse no smartphone: https://localhost:{PORT}")
            print(f"💻 Acesse no computador: https://127.0.0.1:{PORT}")
            print(f"📁 Servindo arquivos de: {os.path.abspath(DIRECTORY)}")
            print(f"🔍 Debug móvel: https://localhost:{PORT}/debug_mobile.html")
            print("\n⚠️  IMPORTANTE para smartphone:")
            print("   1. Conecte o smartphone na mesma rede Wi-Fi")
            print("   2. Descubra o IP local do computador")
            print("   3. Acesse https://[IP_DO_COMPUTADOR]:8443")
            print("   4. Aceite o certificado auto-assinado")
            print("\n🛑 Pressione Ctrl+C para parar o servidor")
            
            # Descobrir IP local
            try:
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                print(f"🌐 IP local detectado: {local_ip}")
                print(f"📱 URL para smartphone: https://{local_ip}:{PORT}")
            except:
                print("⚠️  Não foi possível detectar IP local automaticamente")
            
            httpd.serve_forever()
            
    except PermissionError:
        print(f"❌ Erro de permissão na porta {PORT}")
        print("💡 Tente executar como administrador ou use uma porta diferente")
        return False
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Porta {PORT} já está em uso")
            print("💡 Pare outros servidores ou use uma porta diferente")
        else:
            print(f"❌ Erro do sistema: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
        return True
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🔒 NeuroTranslator - Servidor HTTPS Local")
    print("=" * 50)
    
    if start_https_server():
        print("✅ Servidor finalizado com sucesso")
    else:
        print("❌ Falha ao iniciar servidor")
        sys.exit(1)