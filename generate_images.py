#!/usr/bin/env python3
"""
Script para converter HTMLs gerados em imagens (JPG/PNG).

Requisitos:
    pip install playwright
    playwright install chromium
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

RESULTS_DIR = Path("resultados")


async def html_to_image(html_path: Path, output_path: Path):
    """Converte um arquivo HTML em imagem usando Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Carrega o HTML
        await page.goto(f"file://{html_path.absolute()}")
        
        # Espera o conteúdo carregar
        await page.wait_for_load_state("networkidle")
        
        # Tira screenshot
        await page.screenshot(path=str(output_path), full_page=True, type="jpeg", quality=90)
        
        await browser.close()
        print(f"✓ Imagem gerada: {output_path}")


async def main():
    """Converte todos os HTMLs em imagens."""
    html_files = list(RESULTS_DIR.glob("*.html"))
    
    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado em resultados/")
        print("   Execute primeiro: python generate_results.py")
        return
    
    print(f"🖼️  Convertendo {len(html_files)} arquivos HTML em imagens...\n")
    
    tasks = []
    for html_file in sorted(html_files):
        # Gera nome da imagem (v1-PR1.html -> v1-PR1.jpg)
        img_name = html_file.stem + ".jpg"
        img_path = RESULTS_DIR / img_name
        
        tasks.append(html_to_image(html_file, img_path))
    
    await asyncio.gather(*tasks)
    
    print(f"\n✅ {len(html_files)} imagens geradas em: {RESULTS_DIR}/")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ImportError:
        print("❌ Playwright não instalado!")
        print("\nPara instalar:")
        print("  pip install playwright")
        print("  playwright install chromium")
    except Exception as e:
        print(f"❌ Erro: {e}")
