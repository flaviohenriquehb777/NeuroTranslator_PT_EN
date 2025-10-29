#!/usr/bin/env python3
"""
Script para gerar favicon.ico a partir da Logo_linkedin_vazada.png
"""

from PIL import Image
import os

def generate_favicon():
    """Gera favicon.ico a partir da Logo_linkedin_vazada.png"""
    
    # Caminhos dos arquivos
    input_path = "web/assets/images/Logo_linkedin_vazada.png"
    output_path = "web/favicon.ico"
    
    try:
        # Abrir a imagem original
        print(f"Abrindo imagem: {input_path}")
        img = Image.open(input_path)
        
        # Converter para RGBA se necessário
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Tamanhos padrão para favicon.ico
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        
        # Lista para armazenar as imagens redimensionadas
        images = []
        
        for size in sizes:
            # Redimensionar mantendo a proporção
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
            print(f"Criada imagem {size[0]}x{size[1]}")
        
        # Salvar como favicon.ico
        print(f"Salvando favicon.ico em: {output_path}")
        images[0].save(
            output_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print("✅ Favicon.ico gerado com sucesso!")
        print(f"📁 Arquivo salvo em: {os.path.abspath(output_path)}")
        
        # Verificar o tamanho do arquivo
        file_size = os.path.getsize(output_path)
        print(f"📊 Tamanho do arquivo: {file_size} bytes ({file_size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"❌ Erro ao gerar favicon: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎨 Gerando favicon.ico para NeuroTranslator...")
    success = generate_favicon()
    
    if success:
        print("\n🚀 Favicon gerado! Agora você pode:")
        print("1. Fazer commit das alterações")
        print("2. Fazer push para o GitHub")
        print("3. Aguardar o GitHub Pages atualizar (pode levar alguns minutos)")
    else:
        print("\n❌ Falha ao gerar favicon. Verifique os erros acima.")