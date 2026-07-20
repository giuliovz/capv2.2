#!/usr/bin/env python3
"""
Script para adicionar a logo da Arlete Galdino ao dashboard.

Opção 1: Salvar a imagem manualmente
- Salve a imagem PNG da Arlete Galdino como:
  /workspaces/capv2.2/painel/assets/logo.png

Opção 2: Usar este script com uma URL
- Use: python adicionar_logo.py <url_da_imagem>
- Exemplo: python adicionar_logo.py https://example.com/logo.png

Opção 3: Usar com arquivo local
- Use: python adicionar_logo.py /caminho/da/imagem.png
"""

import sys
import shutil
from pathlib import Path
from urllib.request import urlopen
import tempfile


def adicionar_logo(fonte):
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True, parents=True)
    destino = assets_dir / "logo.png"

    try:
        if fonte.startswith(("http://", "https://")):
            print(f"Baixando imagem de {fonte}...")
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                with urlopen(fonte) as response:
                    tmp.write(response.read())
                tmp_path = tmp.name
            shutil.copy(tmp_path, destino)
            Path(tmp_path).unlink()
        else:
            print(f"Copiando imagem de {fonte}...")
            shutil.copy(fonte, destino)

        print(f"Logo salva com sucesso em: {destino}")
        print("Regenere o dashboard com: python gerar_dashboard_html.py")
    except Exception as e:
        print(f"Erro ao adicionar logo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUso:")
        print("  python adicionar_logo.py <arquivo_ou_url>")
        print("\nExemplo:")
        print("  python adicionar_logo.py ~/Downloads/logo.png")
        sys.exit(1)

    adicionar_logo(sys.argv[1])
