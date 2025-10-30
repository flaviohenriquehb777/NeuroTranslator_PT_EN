#!/usr/bin/env python3
"""
Script completo para gerar todos os formatos de favicon necessários para GitHub Pages
"""

from PIL import Image
import os

def generate_complete_favicon():
    """Gera todos os formatos de favicon necessários"""
    
    # Caminhos dos arquivos
    input_path = "web/assets/images/Logo_linkedin_vazada.png"
    web_dir = "web"
    
    try:
        # Abrir a imagem original
        print(f"🎨 Abrindo imagem: {input_path}")
        img = Image.open(input_path)
        
        # Converter para RGBA se necessário
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        print(f"📐 Imagem original: {img.size} - Modo: {img.mode}")
        
        # 1. Gerar favicon.ico com múltiplos tamanhos
        print("\n🔧 Gerando favicon.ico...")
        sizes_ico = [(16, 16), (32, 32), (48, 48), (64, 64)]
        images_ico = []
        
        for size in sizes_ico:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images_ico.append(resized)
            print(f"   ✓ {size[0]}x{size[1]}")
        
        favicon_ico_path = os.path.join(web_dir, "favicon.ico")
        images_ico[0].save(
            favicon_ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images_ico],
            append_images=images_ico[1:]
        )
        print(f"   💾 Salvo: {favicon_ico_path}")
        
        # 2. Gerar PNGs individuais para diferentes tamanhos
        print("\n🖼️ Gerando PNGs individuais...")
        png_sizes = [16, 32, 48, 64, 96, 128, 192, 512]
        
        for size in png_sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            png_path = os.path.join(web_dir, f"favicon-{size}x{size}.png")
            resized.save(png_path, format='PNG', optimize=True)
            print(f"   ✓ favicon-{size}x{size}.png")
        
        # 3. Gerar apple-touch-icon específico
        print("\n🍎 Gerando Apple Touch Icons...")
        apple_sizes = [180, 192]
        for size in apple_sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            apple_path = os.path.join(web_dir, f"apple-touch-icon-{size}x{size}.png")
            resized.save(apple_path, format='PNG', optimize=True)
            print(f"   ✓ apple-touch-icon-{size}x{size}.png")
        
        # 4. Gerar SVG otimizado (se possível)
        print("\n🎯 Copiando logo original como favicon.png...")
        favicon_png_path = os.path.join(web_dir, "favicon.png")
        img.save(favicon_png_path, format='PNG', optimize=True)
        print(f"   ✓ favicon.png")
        
        print("\n✅ Todos os favicons gerados com sucesso!")
        
        # Listar arquivos gerados
        print("\n📋 Arquivos gerados:")
        favicon_files = [f for f in os.listdir(web_dir) if 'favicon' in f or 'apple-touch-icon' in f]
        for file in sorted(favicon_files):
            file_path = os.path.join(web_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"   📄 {file} ({size} bytes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar favicons: {e}")
        return False

def generate_html_favicon_tags():
    """Gera as tags HTML completas para favicon"""
    
    html_tags = '''    <!-- Favicon - Configuração completa para GitHub Pages -->
    <link rel="icon" type="image/x-icon" href="favicon.ico?v=2025-01-29">
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v=2025-01-29">
    
    <!-- PNG Favicons para diferentes tamanhos -->
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png?v=2025-01-29">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v=2025-01-29">
    <link rel="icon" type="image/png" sizes="48x48" href="favicon-48x48.png?v=2025-01-29">
    <link rel="icon" type="image/png" sizes="96x96" href="favicon-96x96.png?v=2025-01-29">
    <link rel="icon" type="image/png" sizes="192x192" href="favicon-192x192.png?v=2025-01-29">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon-180x180.png?v=2025-01-29">
    <link rel="apple-touch-icon" sizes="192x192" href="apple-touch-icon-192x192.png?v=2025-01-29">
    
    <!-- Fallback PNG -->
    <link rel="icon" type="image/png" href="favicon.png?v=2025-01-29">
    
    <!-- Microsoft Tiles -->
    <meta name="msapplication-TileImage" content="favicon-192x192.png?v=2025-01-29">
    <meta name="msapplication-TileColor" content="#1a1a1a">'''
    
    print("\n📝 Tags HTML geradas:")
    print(html_tags)
    
    return html_tags

if __name__ == "__main__":
    print("🚀 Gerando conjunto completo de favicons para GitHub Pages...")
    
    success = generate_complete_favicon()
    
    if success:
        print("\n" + "="*60)
        generate_html_favicon_tags()
        print("="*60)
        print("\n✅ Processo concluído! Próximos passos:")
        print("1. Atualizar o HTML com as novas tags")
        print("2. Fazer commit e push")
        print("3. Aguardar GitHub Pages atualizar (5-10 minutos)")
        print("4. Limpar cache do navegador se necessário")
    else:
        print("\n❌ Falha ao gerar favicons. Verifique os erros acima.")